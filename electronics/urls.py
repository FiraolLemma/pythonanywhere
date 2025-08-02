# electronics/urls.py
from django.urls import path
from . import views

app_name = 'electronics'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<int:category_id>/', views.product_list, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/new/', views.create_product, name='create_product'),
    path('product/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('product/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('order/<int:product_id>/', views.create_order, name='create_order'),
    path('orders/', views.user_orders, name='user_orders'),
    path('order/<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
]
