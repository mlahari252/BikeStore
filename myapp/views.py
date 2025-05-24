from django.shortcuts import render,redirect, get_object_or_404
from .models import Product,CartItem
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem 



# Create your views here.
def index(request):
    return render(request,'nav.html')
def foot(request):
    return render(request,'foot.html')
def home(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Encrypt password
            user.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request,'sigup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace with your app's home page
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('view_cart')

@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    return redirect('view_cart')

@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, bike=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')
# def checkout_view(request):
#     cart_items = CartItem.objects.filter(user=request.user)
#     subtotal = sum(item.bike.price * item.quantity for item in cart_items)

#     if request.method == 'POST':
#         form = ShippingAddressForm(request.POST)
#         if form.is_valid():
#             shipping = form.save(commit=False)
#             shipping.user = request.user
#             shipping.save()

#             order = Order.objects.create(
#                 user=request.user,
#                 shipping_address=shipping,
#                 subtotal=subtotal,
#             )

#             # Save each cart item into order (optional, if you use OrderItem model)
#             for item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     bike=item.bike,
#                     quantity=item.quantity,
#                     price=item.bike.price,
#                 )

#             cart_items.delete()  # Clear cart after order

#             return redirect('order_confirmation', order_id=order.id)
#     else:
#         form = ShippingAddressForm()

#     return render(request, 'checkout.html', {
#         'form': form,
#         'subtotal': subtotal,
#         'items': cart_items,
#     })


def order_confirmation_view(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    items = order.orderitem_set.all()
    return render(request, 'order_confirmation.html', {'order': order, 'items': items})







from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ShippingAddressForm
from .models import CartItem, Order, OrderItem

def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.bike.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping = form.save(commit=False)
            shipping.user = request.user
            shipping.save()

            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping,
                subtotal=subtotal,
            )

            # Store each cart item in the order
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    bike=item.bike,
                    quantity=item.quantity,
                    price=item.bike.price,
                )

            # Compose email message
            message = f"""
Hello {request.user.username},

Thank you for your order from The BikeStore!

Order ID: {order.id}
Shipping To: {shipping.address}, {shipping.city}
Subtotal: ₹{subtotal:.2f}

Your Ordered Items:
"""
            for item in cart_items:
                message += f" - {item.bike.name} x {item.quantity} = ₹{item.total_price():.2f}\n"

            message += "\nWe'll notify you once your order is on the way.\n\nThanks,\nThe BikeStore Team"

            # Send email
            send_mail(
                subject="🛒 Order Confirmation - The BikeStore",
                message=message,
                from_email=None,  # uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[request.user.email],
                fail_silently=False,
            )

            cart_items.delete()  # Clear the cart after order

            return redirect('order_confirmation', order_id=order.id)
    else:
        form = ShippingAddressForm()

    return render(request, 'checkout.html', {
        'form': form,
        'subtotal': subtotal,
        'items': cart_items,
    })

def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})

