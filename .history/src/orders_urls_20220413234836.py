from django.urls import path
from src.order_view import *

urlpatterns = [
    path('create/', create_order, name='create_order'),
    path('', get_orders, name='get_orders'),
    path('get-order/<int:id>/', get_orderby_id, name='get_orderby_id'),
    path('getmy-orders/', get_myorders, name='get_myorders'),
    path('update-order/<int:id>/', update_order_topaid, name='update_order_topaid'),
    path('update-deliver/<int:id>/', update_order_todelivered, name='update_order_todelivered'),
]