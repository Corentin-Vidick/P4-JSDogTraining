from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.contrib import messages
from .models import PackedStock, BulkStock, LabelStock
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import AddStockForm, AddStockDetailForm
from django.db.models import Sum, Max
from datetime import datetime

def stock(request):
    """
    Display all stock available, grouped by stock name
    """
    # Group the PackedStock by 'name' and calculate the total quantity for each
    grouped_stock = (
        PackedStock.objects
        .values('name', 'category', 'weight', 'label', 'origin_stock')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('name')
    )
    form = AddStockForm()
    return render(request, 'stock/stock.html', {'grouped_stock': grouped_stock, 'form': form})

def stock_detail(request, treat_name):
    """
    Displays a detailed view of the stock, quantity by expiry date/batch
    """
    print("DEBUG: treat_name in view:", treat_name)
    detailed_stock = (
        PackedStock.objects.filter(name=treat_name)
        .values('expiry_date', 'batch')
        .annotate(
            total_quantity=Sum('quantity'),
            name=Max('name'),
            category=Max('category'),
            weight=Max('weight'),
            label=Max('label'),
            origin_stock=Max('origin_stock'),
        )
        .order_by('expiry_date', 'batch')
    )
    form = AddStockDetailForm()
    return render(request, 'stock/stock_detail.html', {
        'treat_name': treat_name,
        'detailed_stock': detailed_stock,
        'form' : form
    })

def add_stock(request):
    """
    Add stock using the corresponding treat name, only the quantity, expiry date and batch are required as a user input,
    the name, category, weight label and origin stock are auto generated
    """
    if request.method == 'POST':
        form = AddStockForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            # Get required auto-populated fields from hidden inputs
            name = request.POST.get('name')
            category = request.POST.get('category')
            weight = request.POST.get('weight')
            label = request.POST.get('label')
            origin_stock = request.POST.get('origin_stock')
            
            # expiry_date and batch are now required:
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
            
            # Create a new stock record
            stock_item = PackedStock(
                name=name,
                category=category,
                weight=weight,
                label=label,
                origin_stock=origin_stock,
                quantity=new_quantity,
                expiry_date=expiry_date,
                batch=batch
            )
            stock_item.save()

            # Recalculate the total quantity for this treat (grouped by name)
            total = PackedStock.objects.filter(name=name).aggregate(total=Sum('quantity'))['total'] or 0
            return JsonResponse({
                'success': True,
                'message': 'Stock added successfully!',
                'total_quantity': total
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})

def add_stock_detail(request):
    """
    Overwrite stock using the corresponding treat name, expiry date and batch. Only the quantity is required as a user input,
    the name, category, weight label and origin stock are auto generated
    """
    if request.method == 'POST':
        form = AddStockDetailForm(request.POST)
        if form.is_valid():
            new_quantity = form.cleaned_data['quantity']
            # Assign the auto-populated fields
            name = request.POST.get('name')
            category = request.POST.get('category')
            weight = request.POST.get('weight')
            label = request.POST.get('label')
            origin_stock = request.POST.get('origin_stock')
            expiry_date_str = request.POST.get('expiry_date')
            # Convert expiry_date to a Python date object
            if expiry_date_str:
                try:
                    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                except ValueError as e:
                    return JsonResponse({'success': False, 'errors': {'expiry_date': str(e)}})
            else:
                expiry_date = None
            # Convert batch from string to integer
            batch_str = request.POST.get('batch')
            if batch_str:
                try:
                    batch = int(batch_str)
                except ValueError as e:
                    return JsonResponse({'success': False, 'errors': {'batch': str(e)}})
            else:
                batch = None

            # Try to fetch an existing record for this treat, expiry date, and batch.
            try:
                stock_item = PackedStock.objects.get(name=name, expiry_date=expiry_date, batch=batch)
                # Overwrite the quantity with the new value
                stock_item.quantity = new_quantity
                # Optionally, update the constant fields (if needed)
                stock_item.category = category
                stock_item.weight = weight
                stock_item.label = label
                stock_item.origin_stock = origin_stock
                stock_item.save()
            except PackedStock.DoesNotExist:
                # No matching record exists, so create a new one
                stock_item = PackedStock(
                    name=name,
                    category=category,
                    weight=weight,
                    label=label,
                    origin_stock=origin_stock,
                    quantity=new_quantity,
                    expiry_date=expiry_date,
                    batch=batch
                )
                stock_item.save()
            # Recalculate the total quantity for this group
            total = PackedStock.objects.filter(name=name, expiry_date=expiry_date, batch=batch).aggregate(total=Sum('quantity'))['total'] or 0
            return JsonResponse({'success': True, 'message': 'Stock added successfully!', 'total_quantity': total})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})
