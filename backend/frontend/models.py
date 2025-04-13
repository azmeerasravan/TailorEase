from django.db import models
from django.contrib.auth.models import User

# User Profile (to store measurements & preferences)

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True, default="")
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=[("customer", "Customer"), ("vendor", "Vendor")])
    brand_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

    
# Fabric Model
class Fabric(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='fabrics/')
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    price_per_meter = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Garment Model
class Garment(models.Model):
    CATEGORY_CHOICES = [('Shirt', 'Shirt'), ('Dress', 'Dress'), ('Suit', 'Suit')]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    MODEL_CHOICES = [
        ('shirt', 'Shirt'),
        ('jeans', 'Jeans'),
        ('jacket', 'Jacket'),
        ('tshirt', 'T-Shirt'),
        ('trackpant', 'Track Pant'),
        ('suit', 'Suit'),
    ]
    
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    ]

    vendor = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    model = models.CharField(max_length=50, choices=MODEL_CHOICES)
    fabric = models.ManyToManyField(Fabric, blank=True)
    size = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.model} - {self.size} - {self.vendor.username}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=20, blank=True, null=True)  # Store selected size
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True, blank=True)  # Store selected fabric

    def __str__(self):
        return f"{self.product.model} - {self.size} - {self.fabric.name if self.fabric else 'No Fabric'}"


# Order Model
class Order(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('frontend', 'frontend'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    garment = models.ForeignKey(Garment, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True)
    measurements = models.JSONField()  # Store measurements
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_id = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

from django.db import models
from django.contrib.auth.models import User

class Measurement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chest = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    hips = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Measurements for {self.user.username}"

class Order(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True)
    measurements = models.JSONField(default=dict)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    fabric = models.ForeignKey(Fabric, on_delete=models.SET_NULL, null=True)
    measurements = models.JSONField(default=dict)
    size = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # Track quantity

    def __str__(self):
        return f"{self.product.model} ({self.quantity}) in {self.cart.user.username}'s cart"
