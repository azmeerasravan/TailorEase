from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, FabricViewSet, GarmentViewSet, OrderViewSet, my_orders
from django.urls import path
from . import views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'fabrics', FabricViewSet)
router.register(r'garments', GarmentViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', views.home, name=''),
    path('auth/signUp/', views.signup_view, name='signup'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/home/', views.home_view, name='home'),  
    path('auth/upgrade-to-vendor/', views.upgrade_to_vendor, name='upgrade_to_vendor'),
    path('auth/vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/profile/', views.profile_view, name='profile'),
    path('auth/vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('auth/vendor/add_product/', views.add_product, name='add_product'),
    path('auth/vendor/add_fabric/', views.add_fabric, name='add_fabric'),
    path('auth/vendor/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('auth/vendor/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('auth/customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('auth/product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('auth/cart/', views.cart, name='cart'),
    path('auth/add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('auth/remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('auth/payment/<int:product_id>/', views.process_payment, name='process_payment'),
    path('auth/submit_payment/<int:product_id>/', views.submit_payment, name='submit_payment'),
    path('auth/purchase/<int:product_id>/', views.purchase_product, name='purchase_product'),
    path('auth/place_order/', views.place_order, name='place_order'),
    path('auth/success_page/', views.success, name='success_page'),
    path("auth/orders/", my_orders, name="orders"),
    path('auth/vendor/orders/', views.vendor_orders_view, name='vendor_orders'),
    path('auth/customize/<int:product_id>/', views.customize_product, name='customize_product'),
]
