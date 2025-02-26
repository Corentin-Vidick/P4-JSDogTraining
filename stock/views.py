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
            stock_item = form.save(commit=False)
            # Assign the auto-populated fields
            stock_item.name = request.POST.get('name')
            stock_item.category = request.POST.get('category')
            stock_item.weight = request.POST.get('weight')
            stock_item.label = request.POST.get('label')
            stock_item.origin_stock = request.POST.get('origin_stock')
            stock_item.save()
            return JsonResponse({'success': True, 'message': 'Stock added successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})

def add_stock_detail(request):
    """
    Add stock using the corresponding treat name, expiry date and batch. Only the quantity is required as a user input,
    the name, category, weight label and origin stock are auto generated
    """
    if request.method == 'POST':
        form = AddStockDetailForm(request.POST)
        if form.is_valid():
            stock_item = form.save(commit=False)
            # Assign the auto-populated fields
            stock_item.name = request.POST.get('name')
            stock_item.category = request.POST.get('category')
            stock_item.weight = request.POST.get('weight')
            stock_item.label = request.POST.get('label')
            stock_item.origin_stock = request.POST.get('origin_stock')
            expiry_date_str = request.POST.get('expiry_date')
            if expiry_date_str:
                try:
                    stock_item.expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
                except ValueError as e:
                    return JsonResponse({'success': False, 'errors': {'expiry_date': str(e)}})
            # Convert batch from string to integer
            batch_str = request.POST.get('batch')
            if batch_str:
                try:
                    stock_item.batch = int(batch_str)
                except ValueError as e:
                    return JsonResponse({'success': False, 'errors': {'batch': str(e)}})
            stock_item.save()
            return JsonResponse({'success': True, 'message': 'Stock updated successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Only POST method allowed'})
