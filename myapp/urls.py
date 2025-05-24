from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='A'),
    path('1/',views.foot),
    path('2/',views.home,name='home'),
    path('3/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
     path('cart/', views.view_cart, name='view_cart'),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout_view, name='checkout'),
   path('confirmation/<int:order_id>/', views.order_confirmation_view, name='order_confirmation'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

    
  
   
]