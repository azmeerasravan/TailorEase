from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Cart, CartItem, UserProfile, Fabric, Garment, Order, Product, Fabric, Measurement
from .serializers import UserSerializer, UserProfileSerializer, FabricSerializer, GarmentSerializer, OrderSerializer, ProductSerializer
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.response import Response
from django.contrib import messages
from .forms import SignUpForm
import stripe
import json
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, UserProfileForm, MeasurementForm, FabricForm
from django.forms.models import model_to_dict

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class FabricViewSet(viewsets.ModelViewSet):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer

class GarmentViewSet(viewsets.ModelViewSet):
    queryset = Garment.objects.all()
    serializer_class = GarmentSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# Create your views here.

def home(request):
    return render(request, 'home.html')


# Signup view
# signup_view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user , address="Not Provided")  

            login(request, user)  
            return redirect('home')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


from django.core.exceptions import ObjectDoesNotExist

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to 'home' after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')


@login_required
def upgrade_to_vendor(request):
    # Ensure that the user has a userprofile, create one if not
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if created:
        # If a new profile was created, you can also set default values if needed
        user_profile.role = 'customer'  # Set default role if needed
        user_profile.save()

    if request.method == 'POST':
        brand_name = request.POST.get('brand_name')
        if brand_name:
            user_profile.brand_name = brand_name
            user_profile.role = 'vendor'
            user_profile.save()
            return redirect('vendor_dashboard')  # Redirect to the vendor dashboard
    
    return render(request, 'upgrade_to_vendor.html')


@login_required
def vendor_dashboard(request):
    if request.user.userprofile.role != "vendor":
        return redirect('home')  # Restrict access

    products = Product.objects.filter(vendor=request.user)
    return render(request, 'vendor_dashboard.html', {'products': products})


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home after logout

@login_required
def profile_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to prevent form resubmission
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, "profile.html", {"form": form, "user_profile": user_profile})


# class ClassAddProduct(viewsets.ModelViewSet):
#     serializer_class = ProductSerializer
#     parser_classes = [MultiPartParser, FormParser, JSONParser]

#     def create(self, request, *args, **kwargs):
#         data = request.data.copy()
#         serializer = self.get_serializer(data = data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Product added successfully", "product": serializer.data}, status=201)
#         return Response(serializer.errors, status=400)


@login_required
def add_product(request):
    if request.user.userprofile.role != "vendor":
        return redirect('home')
    try:
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.vendor = request.user
                product.save()
                # Get fabric IDs from the form data
                fabric_ids = request.POST.getlist('fabric')  # Extract fabric IDs from the form
                product.fabric.set(fabric_ids)
                return redirect('vendor_dashboard')
            else:
                print(f"Form is invalid", form.errors)
        else:
            form = ProductForm()
        
        return render(request, 'add_product.html', {'form': form})
    except Exception as e:
        print(f"Error creating product", str(e))

@login_required
def add_fabric(request):
    if request.user.userprofile.role != "vendor":
        return redirect('home')

    if request.method == "POST":
        form = FabricForm(request.POST, request.FILES)
        if form.is_valid():
            fabric = form.save(commit=False)
            fabric.user = request.user
            fabric.save()
            return redirect('vendor_dashboard')
    else:
        form = FabricForm()
    
    return render(request, 'add_fabric.html', {'form': form})



@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        fabric_ids = request.POST.getlist('fabric')
        if form.is_valid():
            product = form.save(commit=False)  # Save other fields first
            product.save()
            
            # Update the many-to-many relationship
            print(fabric_ids)
            try:
                product.fabric.set([int(fabric_id) for fabric_id in fabric_ids])
                product.save()
            except Exception as e:
                print(f'Error during saving fabric', str(e))

            print(product)
            return redirect('vendor_dashboard')  # Redirect after saving
        else:
            print(form.errors)
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        product.delete()
        return redirect('vendor_dashboard')  # Redirect after deletion

    return redirect('edit_product', product_id=product_id)  # If not deleted, go back


@login_required
def customer_dashboard(request):
    products = Product.objects.all()
    return render(request, 'customer_dashboard.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    sizes = product.size.split(",") if product.size else []
    fabrics = product.fabric.all()  # Fetch related fabrics
    print(fabrics)  # Debugging

    return render(request, 'product_detail.html', {'product': product, 'sizes': sizes, 'fabrics': fabrics})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Get selected size and fabric from POST request
    selected_size = request.POST.get("selected_size")
    selected_fabric_id = request.POST.get("selected_fabric")

    # Ensure fabric exists
    fabric = None
    if selected_fabric_id:
        fabric = get_object_or_404(Fabric, id=selected_fabric_id)

    print(selected_size, selected_fabric_id)
    # Check if the item with the same size and fabric already exists
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product, size=selected_size, fabric=fabric
    )

    if not item_created:
        cart_item.quantity += 1  # Increase quantity if already in cart
        cart_item.save()

    return redirect('cart')


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Decrease quantity
            cart_item.save()
        else:
            cart_item.delete()  # Remove if quantity reaches 0

    return redirect('cart')

@login_required
def process_payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "Your cart is empty. Please add the product to your cart first.")
        return redirect("product_detail", product_id=product_id)  # Redirect to product page

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if not cart_item:
        messages.error(request, "This product is not in your cart. Add it first before purchasing.")
        return redirect("product_detail", product_id=product_id)  # Redirect to product page

    # Calculate total price
    cart_price = product.price * cart_item.quantity

    # Render payment page with item details
    return render(request, 'payment.html', {
        'item': product,
        'quantity': cart_item.quantity,
        'fabric': cart_item.fabric,
        'size': cart_item.size,
        'amount': cart_price
    })

stripe.api_key = settings.STRIPE_SECRET_KEY
@login_required
def submit_payment(request, product_id):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = int(data.get("amount"))
        token = data.get("token")

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount * 100,
                currency="usd",
                payment_method_types=["card"],
                payment_method_data={
                    "type": "card",
                    "card": {"token": token}
                },
                confirm=True 
            )

            # Save order in the database
            product = get_object_or_404(Product, id=product_id)
            order = Order.objects.create(
                user = request.user,
                product=product,
                total_price=amount/100,  # Convert back to dollars
                payment_id=payment_intent.id
            )

            return JsonResponse({"status": "success", "payment_intent_id": payment_intent.id})
        except stripe.error.StripeError as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "invalid request"}, status=400)


@login_required
def place_order(request):
    cart_ids = request.session.get('cart', [])
    for product_id in cart_ids:
        Order.objects.create(customer=request.user, product_id=product_id)
    request.session['cart'] = []
    return redirect('orders')

@login_required
def success(request):
    return render(request, 'success_page.html')

# @login_required
# def vendor_orders(request):
#     orders = Order.objects.filter(product__vendor=request.user)
#     return render(request, 'vendor_orders.html', {'orders': orders})



@login_required
def customize_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Step 1: If user selected size and fabric, store them in session
    if request.method == 'POST' and "selected_size" in request.POST and "selected_fabric" in request.POST:
        request.session["selected_size"] = request.POST.get("selected_size")
        request.session["selected_fabric"] = request.POST.get("selected_fabric")

    measurement, created = Measurement.objects.get_or_create(user=request.user)

    # Step 2: Show the measurement form
    if request.method == 'POST' and "SaveOrder" in request.POST:  # Checking for form submission
        form = MeasurementForm(request.POST, instance=measurement)
        if form.is_valid():
            form.save()

            # Step 3: Retrieve stored size and fabric
            selected_size = request.session.get("selected_size")
            selected_fabric_id = request.session.get("selected_fabric")

            if not selected_size or not selected_fabric_id:
                return redirect("product_detail", product_id=product_id)  # Handle error

            # Ensure fabric exists
            fabric = get_object_or_404(Fabric, id=selected_fabric_id)

            # Add item to cart
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart, product=product, size=selected_size, fabric=fabric, measurements=model_to_dict(measurement, exclude=['id', 'user'])
            )

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

            # Clean up session data
            del request.session["selected_size"]
            del request.session["selected_fabric"]

            return redirect("cart")

    else:
        form = MeasurementForm(instance=measurement)

    return render(request, "customize_product.html", {"form": form, "product": product})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def purchase_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Add logic to handle purchase (e.g., create order, process payment)
    return redirect('product_detail', product_id=product.id)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('vendor_dashboard')  # Redirect back to the vendor dashboard

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "orders.html", {"orders": orders})

from django.shortcuts import render, redirect
from .models import Order

@login_required
def vendor_orders_view(request):
    vendor = request.user
    orders = Order.objects.filter(product__vendor=vendor)

    if request.method == "POST" and 'update_order' in request.POST:
        order_id = request.POST.get('update_order')
        new_status = request.POST.get(f'status_{order_id}')
        try:
            order = Order.objects.get(id=order_id, product__vendor=vendor)
            order.status = new_status
            order.save()
        except Order.DoesNotExist:
            pass
        return redirect('vendor_orders')  # Replace with your actual URL name

    return render(request, 'orders_vendors.html', {'orders': orders})
