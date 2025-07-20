from django.shortcuts import render, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.views.decorators.http import require_POST
from django.http import JsonResponse

# Create your views here.
@require_POST
def cart_add(request,product_id):
    cart_id=request.session.get('cart_id')

    if cart_id:
        try:
            cart=Cart.objects.get(id=cart_id)
        except cart.DoesNotExist:
            cart=Cart.objects.create()
    else:
        cart=Cart.objects.create()
        request.session['cart_id']=cart.id

    product=get_object_or_404(Product, id=product_id)

    cart_item, created=CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity+=1
        cart_item.save()
    
    response_data={
        "success":True,
        'message':f"{product.name} added to cart successfully"
    }
    return JsonResponse(response_data)

def cart_detail(request):
    cart_id=request.session.get('cart_id')
    cart=None
    if cart_id:
        cart=get_object_or_404(Cart, id=cart_id)
    return render(request, 'cart/detail.html', {'cart':cart})

def cart_remove(request, product_id):
    product=get_object_or_404(Product, id=product_id)
    cart_id=request.session.get('cart_id')
    if cart_id:
        cart=get_object_or_404(Cart, id=cart_id)
    cart_item=get_object_or_404(CartItem, cart=cart, product=product)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    total_price = cart.get_total_price()
    response_data={
        'success':True,
        'message':f"{product.name} removed from cart successfully",
        'total_price': total_price,
    }
    return JsonResponse(response_data)    