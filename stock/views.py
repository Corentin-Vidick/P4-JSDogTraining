from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.contrib import messages
from .models import PackedStock, BulkStock, LabelStock
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import AddStockForm

def stock(request):
    """
    Display all stock available, grouped by stock name
    """
    packed_stock = PackedStock.objects.all()
    form = AddStockForm()
    context = {
        "stock": packed_stock,
        "form": form,
    }
    return render(request, "stock/stock.html", context)

def add_stock(request):
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

