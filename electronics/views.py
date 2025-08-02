# electronics/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Order, Review
from .forms import ProductForm, OrderForm, ReviewForm
from django.contrib.auth import get_user_model
User = get_user_model()

def product_list(request, category_id=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(stock__gt=0)
    
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
    
    return render(request, 'electronics/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'electronics/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })

@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Product created successfully!')
            return redirect('electronics:product_detail', product_id=product.id)
    else:
        form = ProductForm()
    return render(request, 'electronics/product_form.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('electronics:product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'electronics/product_form.html', {'form': form})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('electronics:product_list')
    return render(request, 'electronics/product_confirm_delete.html', {'product': product})

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.seller == request.user:
        messages.error(request, "You can't order your own product!")
        return redirect('electronics:product_detail', product_id=product.id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.buyer = request.user
            order.product = product
            order.save()
            
            # Update product stock
            product.stock -= order.quantity
            product.save()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('electronics:user_orders')
    else:
        form = OrderForm(initial={'quantity': 1})
    
    return render(request, 'electronics/order_form.html', {
        'form': form,
        'product': product,
    })

@login_required
def user_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-order_date')
    return render(request, 'electronics/user_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        
        # Restore product stock
        order.product.stock += order.quantity
        order.product.save()
        
        messages.success(request, 'Order cancelled successfully!')
    else:
        messages.error(request, "This order can't be cancelled.")
    return redirect('electronics:user_orders')

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Check if user has purchased the product
    has_purchased = Order.objects.filter(
        buyer=request.user,
        product=product,
        status='completed'
    ).exists()
    
    if not has_purchased:
        messages.error(request, "You can only review products you've purchased!")
        return redirect('electronics:product_detail', product_id=product.id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('electronics:product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    
    return render(request, 'electronics/review_form.html', {
        'form': form,
        'product': product,
    })

@login_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    orders = Order.objects.filter(product__seller=request.user).order_by('-order_date')
    
    # Calculate total sales
    total_sales = sum(order.total_price for order in orders.filter(status='completed'))
    
    return render(request, 'electronics/seller_dashboard.html', {
        'products': products,
        'orders': orders,
        'total_sales': total_sales,
    })