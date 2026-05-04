from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('cart/',cart,name='cart'),
    path('addtocart/<int:id>',addtocart,name='addtocart'),
    path('remove/<int:id>',remove,name='remove'),
    path('increment<int:id>',increment,name='increment'),
    path('decrement<int:id>',decrement,name='decrement'),
    path('support/',support,name='support'),
    path('knownus/',knownus,name='knownus'),
    path('product/<int:id>/',product_detail, name='product_detail'),
    path('checkout/',checkout, name='checkout'),
    path('success/',success, name='success'),
    path('orders/', orders, name='orders'),
    path('success/',success, name='success')
]