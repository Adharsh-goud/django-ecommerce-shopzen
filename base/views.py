from django.shortcuts import render, redirect
from .models import Product, CartModel, Order
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartModel, Order, OrderItem
from datetime import timedelta
from django.utils import timezone


# ================= HOME =================
def home(request):

    if request.user.is_authenticated:
        cartproducts_count = CartModel.objects.filter(host=request.user).count()
    else:
        cartproducts_count = 0

    no_match = False
    trending = False
    offer = False

    # SEARCH
    if 'search' in request.GET:
        q = request.GET['search']
        all_products = Product.objects.filter(
            Q(pname__icontains=q) | Q(pdesc__icontains=q)
        )
        if not all_products:
            no_match = True

    # CATEGORY
    elif 'cat' in request.GET:
        cat = request.GET['cat']
        all_products = Product.objects.filter(pcategory=cat)

    # TRENDING
    elif 'trending' in request.GET:
        all_products = Product.objects.filter(trending=True)
        trending = True

    # OFFER
    elif 'offer' in request.GET:
        all_products = Product.objects.filter(offer=True)
        offer = True

        # 🔥 FORCE 30% DISCOUNT
        for p in all_products:
            p.offer_price = int(p.price * 0.7)
            p.offer_save = p.price - p.offer_price

    # DEFAULT
    else:
        all_products = Product.objects.all()

    # CATEGORY LIST
    category = []
    for i in Product.objects.all():
        if i.pcategory not in category:
            category.append(i.pcategory)

    return render(request, 'home.html', {
        'all_product': all_products,
        'no_match': no_match,
        'category': category,
        'cartproducts_count': cartproducts_count,
        'trending': trending,
        'offer': offer,
        'page_type': 'main'
    })


# ================= CART =================
@login_required(login_url='login_')
def cart(request):
    cartproducts = CartModel.objects.filter(host=request.user)

    TA = 0
    for i in cartproducts:
        TA += i.totalprice

    cartproducts_count = cartproducts.count()

    return render(request, 'cart.html', {
        'cartproducts': cartproducts,
        'TA': TA,
        'cartproducts_count': cartproducts_count,
        'page_type': 'main'
        
    })


# ================= ADD TO CART =================
@login_required(login_url='login_')
def addtocart(request, id):

    product = Product.objects.get(id=id)

    try:
        item = CartModel.objects.get(pname=product.pname, host=request.user)

        item.quantity += 1
        item.totalprice = item.quantity * item.price
        item.save()

        messages.info(request, "Quantity updated in cart")

    except CartModel.DoesNotExist:

        CartModel.objects.create(
            pname=product.pname,
            price=product.final_price,  # uses model discount
            pcategory=product.pcategory,
            quantity=1,
            totalprice=product.final_price,
            host=request.user
        )

        messages.success(request, "Item added to cart")

    return redirect(request.META.get('HTTP_REFERER', 'home'))


# ================= REMOVE =================
def remove(request, id):
    product = CartModel.objects.get(id=id)
    product.delete()
    return redirect('cart')


# ================= INCREMENT =================
def increment(request, id):
    product = CartModel.objects.get(id=id)
    product.quantity += 1
    product.totalprice += product.price
    product.save()
    return redirect('cart')


# ================= DECREMENT =================
def decrement(request, id):
    product = CartModel.objects.get(id=id)

    if product.quantity > 1:
        product.quantity -= 1
        product.totalprice -= product.price
        product.save()
    else:
        product.delete()

    return redirect('cart')


# ================= PRODUCT DETAIL =================
def product_detail(request, id):

    product = Product.objects.get(id=id)

    if request.user.is_authenticated:
        cart_count = CartModel.objects.filter(host=request.user).count()
    else:
        cart_count = 0

    return render(request, 'product_detail.html', {
        'p': product,
        'cartproducts_count': cart_count
    })


# ================= CHECKOUT =================
@login_required(login_url='login_')

def checkout(request):

    # 🛒 get cart items
    cartproducts = CartModel.objects.filter(host=request.user)

    # 💰 calculations
    item_total = sum(i.totalprice for i in cartproducts)

    delivery = 0 if item_total > 1000 else 50
    platform = 5
    discount = int(item_total * 0.10)

    final_total = item_total + delivery + platform - discount

    # 🔥 PLACE ORDER
    if request.method == 'POST':

        for item in cartproducts:
            Order.objects.create(
                user=request.user,
                pname=item.pname,
                price=item.price,
                quantity=item.quantity,

                # ✅ IMPORTANT FIX
                totalprice=final_total,

                pimage=item.product.pimage if hasattr(item, 'product') else None
            )

        # 🧹 clear cart
        cartproducts.delete()

        return redirect('success')

    # 📄 show checkout page
    return render(request, 'checkout.html', {
        'cartproducts': cartproducts,
        'item_total': item_total,
        'delivery': delivery,
        'platform': platform,
        'discount': discount,
        'final_total': final_total,
        'page_type': 'main'
    })

# ================= SUCCESS =================
def success(request):
    return render(request, 'success.html')


# ================= STATIC PAGES =================
def support(request):
    return render(request, 'support.html')


def knownus(request):
    return render(request, 'knownus.html')



def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-id')

    return render(request, 'orders.html', {
        'orders': user_orders,
        'page_type': 'main'
    })

def success(request):
    return render(request, 'success.html', {
        'page_type': 'main'
    })

