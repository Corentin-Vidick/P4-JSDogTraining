from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic, View
from django.contrib import messages
from .models import PackedStock, BulkStock, LabelStock

def stock(request):
    """
    Display all stock available, grouped by stock name
    """
    packed_stock = PackedStock.objects.all()
    context = {
        "stock": packed_stock
    }
    return render(request, "stock/stock.html", context)
