from django.shortcuts import render
from django.views import generic, View
import datetime

from stock.models import Product, PackedStock, BulkStock


def home(request):
    """
    Displays short-dated stock for easy visualisation
    """
    print("Displaying short dated stock")
    packed_stock = PackedStock.objects.all().order_by('expiry_date')[:3]
    if packed_stock.exists():
        print(packed_stock)
    bulk_stock = BulkStock.objects.all().order_by('expiry_date')[:3]
    if bulk_stock.exists():
        print(bulk_stock)
    #         for stock in bulk_stock:
    #             if stock.quantity > 0:    
    #                 first_bulk_stock = stock
    #                 print(first_bulk_stock)
    #                 break
    return render(request, "home/home.html", {
        'first_packed_stock': packed_stock,
        'first_bulk_stock': bulk_stock,})
