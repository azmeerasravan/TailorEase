from django import forms
from django.contrib.auth.models import User
from .models import Product, Fabric, UserProfile, Measurement
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

# User signup form
class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# User login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address', 'contact', 'email', 'brand_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["address", "contact", "email", "brand_name"]
 # Include necessary fields



class ProductForm(forms.ModelForm):
    size = forms.TypedMultipleChoiceField(
        choices=Product.SIZE_CHOICES,
        coerce=str,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )

    fabric = forms.ModelMultipleChoiceField(
        queryset=Fabric.objects.all(),  
        widget=forms.CheckboxSelectMultiple,  # Allows multiple selections in UI
        required=False  
    )

    class Meta:
        model = Product
        fields = ['model', 'size', 'price', 'fabric', 'image']

    def clean_size(self):
        """Convert selected sizes into a comma-separated string before saving."""
        sizes = self.cleaned_data.get('size', [])
        return ",".join(sizes) if sizes else ""  # Convert list to string



class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['chest', 'waist', 'hips', 'length']
        widgets = {
            'chest': forms.NumberInput(attrs={'class': 'form-control'}),
            'waist': forms.NumberInput(attrs={'class': 'form-control'}),
            'hips': forms.NumberInput(attrs={'class': 'form-control'}),
            'length': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class FabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = ['name', 'image', 'price_per_meter']

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            img = Image.open(image)

            # Check image dimensions
            if img.width != 100 or img.height != 100:
                # Resize the image to 100x100
                img = img.resize((100, 100), Image.LANCZOS)
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                image = InMemoryUploadedFile(
                    buffer, 'ImageField', image.name, 'image/png', buffer.tell(), None
                )

        return image
