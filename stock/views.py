from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.db.models import Sum, Max, F

from datetime import datetime

from .models import Product, PackedStock, BulkStock, LabelStock
from .forms import PackedStockForm, RemoveStockForm, AddStockDetailForm
from .forms import AddLabelStockForm
from .forms import AddBulkStockForm, AddBulkStockDetailForm


#
# PackedStock views
#

def stock(request):
    """
    Display all packed stock available, grouped by product.
    """
    # Group PackedStock by product and sum up the quantity for each product.
    grouped_stock = (
        PackedStock.objects
        .values('product__id', 'product__name', 'product__label_code')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('product__name')
    )
    return render(request, 'stock/stock.html', {
        'grouped_stock': grouped_stock,
        'form': PackedStockForm(),
        'remove_form': RemoveStockForm()
    })

def stock_detail(request, product_id):
    """
    Displays a detailed view of the stock, quantity by expiry date/batch
    """
    print("DEBUG: product_id in view:", product_id)
    # Retrieve the product instance
    product = Product.objects.get(id=product_id)
    detailed_stock = (
        PackedStock.objects.filter(product=product)
        .values('expiry_date', 'batch')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('expiry_date', 'batch')
    )
    form = AddStockDetailForm()
    return render(request, 'stock/stock_detail.html', {
        'product': product,
        'detailed_stock': detailed_stock,
        'form' : form
    })

def add_stock(request):
    """
    Add stock (packing) for a given product.
    The user provides quantity, expiry_date, and batch.
    The product is determined via a hidden field (e.g. product_id).
    After saving the new PackedStock record, the corresponding LabelStock
    is updated by subtracting the added quantity. The total weight is taken
    out of the corresponding BulkStock with the closest expiry date.
    """
    if request.method == 'POST':
        form = PackedStockForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            
            # Get hidden field: product_id (assumed to be sent in the POST data)
            product_id = request.POST.get('product_id')
            if not product_id:
                return JsonResponse({'success': False, 'errors': {'product': 'Product is required.'}})
            
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'errors': {'product': 'Invalid product.'}})
            
            # Get expiry date and batch from the POST data (both required)
            expiry_date_str = request.POST.get('expiry_date')
            batch_str = request.POST.get('batch')
            if not expiry_date_str:
                return JsonResponse({'success': False, 'errors': {'expiry_date': 'Expiry date is required.'}})
            if not batch_str:
                return JsonResponse({'success': False, 'errors': {'batch': 'Batch is required.'}})
            try:
                expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
            except ValueError as e:
                return JsonResponse({'success': False, 'errors': {'expiry_date': str(e)}})
            try:
                batch = int(batch_str)
            except ValueError as e:
                return JsonResponse({'success': False, 'errors': {'batch': str(e)}})
            
            # Delete any zero-quantity records for this product (if desired)
            PackedStock.objects.filter(product=product, quantity=0).delete()

            # Get the weight from pre-existing stock
            item = PackedStock.objects.filter(product=product).first()
            print("Item:", item)
            item_weight = item.weight
            print ("The weight of the item is: ", item_weight)
            
            # Create a new PackedStock record
            stock_item = PackedStock(
                product=product,
                quantity=new_quantity,
                expiry_date=expiry_date,
                batch=batch,
                weight=item_weight
            )
            stock_item.save()

            # Adjust LabelStock quantity for this product:
            try:
                label_stock = product.label_stock
                print("Corresponding label: ", label_stock)
                # Deduct the new quantity from the front label quantity
                label_stock.label_quantity_1 = max(0, label_stock.label_quantity_1 - new_quantity)
                # If product uses two labels, also deduct from the back label quantity
                if label_stock.has_two_labels:
                    label_stock.label_quantity_2 = max(0, label_stock.label_quantity_2 - new_quantity)
                label_stock.save()
            except LabelStock.DoesNotExist:
                # Optionally handle missing label stock (maybe log or ignore)
                print("Label stock not found")

            # Adjust corresponding BulkStock quantity:
            total_weight = new_quantity * stock_item.weight
            print("Total weight: ", total_weight)
            bulk_qs = BulkStock.objects.filter(products=product).order_by('expiry_date', 'batch')
            print("bulk_qs", bulk_qs)
            remaining = total_weight
            for bucket in bulk_qs:
                if remaining <= 0:
                    break
                if bucket.quantity <= remaining:
                    remaining -= bucket.quantity
                    bucket.quantity = 0
                    bucket.save(update_fields=['quantity'])
                else:
                    bucket.quantity -= remaining
                    bucket.save(update_fields=['quantity'])
                    remaining = 0

            if remaining > 0:
                # Not enough bulk stock to cover the weight used.
                # Warn the user
                messages.warning(request,
                f"Packed {new_quantity} units ({total_weight}g) but only "
                f"{total_weight-remaining}g of bulk was available."
                )

            # Recalculate the total quantity for this product
            total = PackedStock.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0

            return JsonResponse({
                'success': True,
                'message': 'Stock added successfully!',
                'total_quantity': total
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})

def remove_stock(request):
    """
    Remove stock for a given product (grouped view), following these rules:
      - Remove stock from PackedStock records in FIFO order (earliest expiry first).
      - If a record’s quantity falls to zero, delete that record.
      - If the removal quantity is greater than the total available and not confirmed,
        return a warning prompting for confirmation.
      - If confirmed, merge all records into one (keep the earliest record, set its quantity to zero, and delete the others).
    """
    if request.method == 'POST':
        form = RemoveStockForm(request.POST)
        if form.is_valid():
            removal_qty = form.cleaned_data['quantity']
            confirm = form.cleaned_data.get('confirm', False)
            # Get the product id from a hidden field:
            product_id = request.POST.get('product_id')
            if not product_id:
                return JsonResponse({'success': False, 'errors': {'product': 'Product is required.'}})
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'errors': {'product': 'Invalid product.'}})
            
            # Calculate total available stock for this product
            total = PackedStock.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0

            if removal_qty > total and not confirm:
                return JsonResponse({
                    'success': False,
                    'warning': True,
                    'message': 'Removal quantity exceeds total available. Please confirm removal.'
                })
            
            if removal_qty > total and confirm:
                # Over-removal confirmed: Merge all records into one.
                stocks = PackedStock.objects.filter(product=product).order_by('expiry_date')
                if stocks.exists():
                    first_stock = stocks.first()
                    first_stock.quantity = 0
                    first_stock.save()
                    stocks.exclude(pk=first_stock.pk).delete()
            else:
                # Normal removal: removal_qty <= total
                stocks = PackedStock.objects.filter(product=product).order_by('expiry_date')
                remaining = removal_qty
                for stock in stocks:
                    if remaining <= 0:
                        break
                    if stock.quantity <= remaining:
                        remaining -= stock.quantity
                        stock.delete()
                    else:
                        stock.quantity -= remaining
                        stock.save()
                        remaining = 0

            new_total = PackedStock.objects.filter(product=product).aggregate(total=Sum('quantity'))['total'] or 0
            return JsonResponse({
                'success': True,
                'message': 'Stock removed successfully!',
                'total_quantity': new_total
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})

def update_stock_detail(request):
    """
    Overwrite (update) stock for a given product, expiry date, and batch.
    The user provides a new quantity, while the product info is provided via hidden fields.
    If a record exists for the given product/expiry_date/batch, its quantity is overwritten.
    Otherwise, a new record is created.
    """
    if request.method == 'POST':
        form = AddStockDetailForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            
            # Retrieve hidden fields
            product_id = request.POST.get('product_id')
            expiry_date_str = request.POST.get('expiry_date')
            batch_str = request.POST.get('batch')
            
            if not product_id:
                return JsonResponse({'success': False, 'errors': {'product': 'Product is required.'}})
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'errors': {'product': 'Invalid product.'}})
            
            # Convert expiry_date
            if expiry_date_str:
                try:
                    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                except ValueError as e:
                    return JsonResponse({'success': False, 'errors': {'expiry_date': str(e)}})
            else:
                expiry_date = None
            
            # Convert batch
            if batch_str:
                try:
                    batch = int(batch_str)
                except ValueError as e:
                    return JsonResponse({'success': False, 'errors': {'batch': str(e)}})
            else:
                batch = None
            
            # Try to fetch an existing PackedStock record for this product, expiry_date, and batch.
            try:
                stock_item = PackedStock.objects.get(product=product, expiry_date=expiry_date, batch=batch)
                # Overwrite the quantity with the new value
                stock_item.quantity = new_quantity
                stock_item.save()
            except PackedStock.DoesNotExist:
                # No matching record exists, so create a new one.
                # Optionally, you might use a weight field from POST or default to product value.
                weight = request.POST.get('weight', 0)
                stock_item = PackedStock(
                    product=product,
                    quantity=new_quantity,
                    expiry_date=expiry_date,
                    batch=batch,
                    weight=weight
                )
                stock_item.save()
            
            # Recalculate the total quantity for this group (for the given product, expiry date, and batch)
            total = PackedStock.objects.filter(product=product, expiry_date=expiry_date, batch=batch)\
                        .aggregate(total=Sum('quantity'))['total'] or 0
            
            return JsonResponse({
                'success': True,
                'message': 'Stock updated successfully!',
                'total_quantity': total
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})

#
# LabelStock views
#

def label(request):
    """
    Display all label stock available, grouped by product.
    """
    # Group LabelStock by product fields.
    grouped_label_stock = (
        LabelStock.objects
        .values('product__id', 'product__name', 'product__label_code', 'has_two_labels')
        .annotate(
            total_quantity_1=Sum('label_quantity_1'),
            total_quantity_2=Sum('label_quantity_2')
        )
        .order_by('product__name')
    )
    # Default form
    label_form = AddLabelStockForm(initial={'has_two_labels': False})
    return render(request, 'stock/label_stock.html', {
        'grouped_label_stock': grouped_label_stock,
        'label_form': label_form,
    })

def get_label_stock_form(request):
    """
    Return the rendered AddLabelStockForm based on the provided has_two_labels parameter.
    """
    has_two_labels_str = request.GET.get('has_two_labels', 'false')
    has_two_labels = has_two_labels_str.lower() == 'true'
    form = AddLabelStockForm(has_two_labels=has_two_labels)
    # Ensure the partial template path is correct.
    html = render_to_string('partials/label_stock_form.html', {'label_form': form})
    return JsonResponse({'form_html': html})

def add_label_stock(request):
    """
    Add label stock for a given product.
    The user provides quantities, and the product is determined via a hidden field.
    """
    if request.method == 'POST':
        # Pass the has_two_labels parameter to the form constructor
        has_two_labels = request.POST.get('has_two_labels') == 'True'
        form = AddLabelStockForm(request.POST, has_two_labels=True)
        print("Form Data:", request.POST)
        if form.is_valid():
            print("Cleaned Data:", form.cleaned_data)
            new_quantity_1 = form.cleaned_data['label_quantity_1']
            new_quantity_2 = form.cleaned_data.get('label_quantity_2', 0)
            print("Quantity 1:", new_quantity_1)
            print("Quantity 2:", new_quantity_2)
            # Get the product from the hidden field (name "product" in the form)
            product_id = request.POST.get('product_id')
            if not product_id:
                return JsonResponse({'success': False, 'message': 'Product is required'})
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid product'})
            
            # Get or create the LabelStock for that product.
            stock_item, created = LabelStock.objects.get_or_create(
                product=product,
                defaults={
                    'has_two_labels': has_two_labels,
                    'label_quantity_1': new_quantity_1,
                    'label_quantity_2': new_quantity_2,
                }
            )
            if not created:
                # If it exists, update the quantities using F expressions.
                stock_item.label_quantity_1 = F('label_quantity_1') + new_quantity_1
                stock_item.label_quantity_2 = F('label_quantity_2') + new_quantity_2
                print("Updating quantities: ", new_quantity_1, new_quantity_2)
                stock_item.save()

            # Recalculate the total quantities for this product.
            total_1 = LabelStock.objects.filter(product=product).aggregate(total_1=Sum('label_quantity_1'))['total_1'] or 0
            total_2 = LabelStock.objects.filter(product=product).aggregate(total_2=Sum('label_quantity_2'))['total_2'] or 0
            return JsonResponse({
                'success': True,
                'message': 'Label stock added successfully!',
                'total_quantity_1': total_1,
                'total_quantity_2': total_2
            })
        else:
            print("Form Errors:", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})

#
# BulkStock views
#

def bulk_stock(request):
    """
    Display all bulk stock available, grouped by bulk stock name.
    Each line shows the bulk stock type (e.g. FTT, FF) and the aggregated quantity.
    """
    # Group BulkStock by name and sum up the quantity for each group.
    grouped_bulk_stock = (
        BulkStock.objects
        .values('name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('name')
    )

    # products = BulkStock.objects.filter(name='FTT').values('products__label_code')
    
    bulk_form = AddBulkStockForm()
    
    return render(request, 'stock/bulk_stock.html', {
        'grouped_bulk_stock': grouped_bulk_stock,
        'bulk_form': bulk_form,
    })

def add_bulk_stock(request):
    """
    Add bulk stock for a given bulk stock type.
    The user provides quantity, expiry_date, and batch via the form.
    The bulk stock type is determined via a hidden field 'bulk_stock_name'.
    """
    if request.method == 'POST':
        form = AddBulkStockForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            expiry_date = form.cleaned_data['expiry_date']
            batch = form.cleaned_data['batch']
            # Get the bulk stock type from the hidden field.
            bulk_stock_name = request.POST.get('bulk_stock_name')
            # Get one existing object from the same BulkStock
            related_bulk_stock = BulkStock.objects.filter(name=bulk_stock_name).first()
            # Get the products associated to that BulkStock
            associated_products = related_bulk_stock.products.all()
            if not bulk_stock_name:
                return JsonResponse({'success': False, 'message': 'Bulk stock name is required.'})
            
            # Create a new BulkStock record
            bulk_stock_item = BulkStock(
                name=bulk_stock_name,
                quantity=new_quantity,
                expiry_date=expiry_date,
                batch=batch,
            )
            bulk_stock_item.save()

            # Set the M2M values for the newly created BulkStock record
            bulk_stock_item.products.set(associated_products)
            
            # Recalculate the total quantity for this bulk stock type.
            total = BulkStock.objects.filter(name=bulk_stock_name).aggregate(total=Sum('quantity'))['total'] or 0
            
            return JsonResponse({
                'success': True,
                'message': 'Bulk stock added successfully!',
                'total_quantity': total
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})

def bulk_stock_detail(request, bulk_stock_name):
    """
    Displays a detailed view of the stock, quantity by expiry date/batch
    """
    print("DEBUG: bulk_stock_name in bulk view:", bulk_stock_name)
    detailed_bulk_stock = (
        BulkStock.objects.filter(name=bulk_stock_name)
        .values('expiry_date', 'batch', 'id')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('expiry_date', 'batch')
    )
    form = AddBulkStockDetailForm()
    return render(request, 'stock/bulk_stock_detail.html', {
        'bulk_stock_name': bulk_stock_name,
        'detailed_stock': detailed_bulk_stock,
        'form' : form
    })

def update_bulk_stock_detail(request):
    """
    Overwrite (update) stock for a given product, expiry date, and batch.
    The user provides a new quantity, while the product info is provided via hidden fields.
    If a record exists for the given product/expiry_date/batch, its quantity is overwritten.
    Otherwise, a new record is created.
    """
    if request.method == 'POST':
        form = AddBulkStockDetailForm(request.POST)
        print("Form Data:", request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            print("DEBUG: new_quantity in bulk view:", new_quantity)
            # Retrieve hidden fields
            product_id = request.POST.get('bulk_stock_id')
            expiry_date_str = request.POST.get('expiry_date')
            batch_str = request.POST.get('batch')
            
            if not product_id:
                return JsonResponse({'success': False, 'errors': {'product': 'Product is required.'}})
            try:
                bulk_product = BulkStock.objects.get(id=product_id)
                print("DEBUG: Product found:", bulk_product.name)
            except BulkStock.DoesNotExist:
                return JsonResponse({'success': False, 'errors': {'product': 'Invalid product.'}})
            
            # Convert expiry_date
            if expiry_date_str:
                try:
                    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                except ValueError as e:
                    return JsonResponse({'success': False, 'errors': {'expiry_date': str(e)}})
            else:
                expiry_date = None
            
            # Convert batch
            if batch_str:
                try:
                    batch = int(batch_str)
                except ValueError as e:
                    return JsonResponse({'success': False, 'errors': {'batch': str(e)}})
            else:
                batch = None
            
            # Try to fetch an existing BulkStock record for this product, expiry_date, and batch.
            try:
                stock_item = BulkStock.objects.get(name=bulk_product.name, expiry_date=expiry_date, batch=batch)
                print("BulkStock exists and found")
                # Overwrite the quantity with the new value
                stock_item.quantity = new_quantity
                stock_item.save()
            except BulkStock.DoesNotExist:
                # No matching record exists, so create a new one.
                print("BulkStock not found, creating new one")
                stock_item = BulkStock(
                    name=bulk_product.name,
                    quantity=new_quantity,
                    expiry_date=expiry_date,
                    batch=batch
                )
                stock_item.save()
            
            # Recalculate the total quantity for this group (for the given product, expiry date, and batch)
            total = BulkStock.objects.filter(name=bulk_product.name, expiry_date=expiry_date, batch=batch)\
                        .aggregate(total=Sum('quantity'))['total'] or 0
            
            return JsonResponse({
                'success': True,
                'message': 'Stock updated successfully!',
                'total_quantity': total
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})
