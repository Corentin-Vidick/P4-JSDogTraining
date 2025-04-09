from . import views
from django.urls import path

urlpatterns = [
    # Main stock page (displays all grouped stock items)
    path('stock/', views.stock, name='stock'),
    
    # Add stock (for creating new PackedStock entries)
    path('add_stock/', views.add_stock, name='add_stock'),
    
    # Stock detail (view for a specific product based on its ID)
    path('stock/<int:product_id>/', views.stock_detail, name='stock_detail'),
    
    # Add stock detail (for adding additional batch information)
    path('add_stock_detail/', views.update_stock_detail, name='add_stock_detail'),
    
    # Remove stock (for reducing or deleting PackedStock records)
    path('remove_stock/', views.remove_stock, name='remove_stock'),
    
    # Label management
    path('label/', views.label, name='label'),
    
    # Add label stock (for managing LabelStock entries)
    path('add_label_stock/', views.add_label_stock, name='add_label_stock'),
    
    # Fetch the form to add label stock (AJAX loading)
    path('get_label_stock_form/', views.get_label_stock_form, name='get_label_stock_form'),

    # Bulk stock management
    path('bulk_stock/', views.bulk_stock, name='bulk_stock'),

    # Add bulk stock
    path('add_bulk_stock', views.add_bulk_stock, name='add_bulk_stock'),

    #Bulk stock detail
    path('bulk_stock_detail/<str:bulk_stock_name>/', views.bulk_stock_detail, name='bulk_stock_detail'),

    # Add bulk stock detail
    path('add_bulk_stock_detail/', views.update_bulk_stock_detail, name='add_bulk_stock_detail'),
]
