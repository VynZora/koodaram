from django import forms
from .models import  Blog, Testimonial, Category, GalleryImage, ContactMessage, Activity, CampingPackage, Booking


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["image", "title", "description"]


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "image", "review"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["category", "title", "image"]


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "phone", "email", "message"]

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["title", "description", "image", "duration"]


class CampingPackageForm(forms.ModelForm):
    class Meta:
        model = CampingPackage
        fields = [
            "name", "description", "main_image", "check_in", "check_out",
            "normal_price", "special_price", "extra_person_price",
            "package_items", "facilities"
        ]

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["name", "email", "phone", "check_in", "check_out", "camping_package", "guests", "message"]
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'camping_package': forms.Select(attrs={'class': 'form-control'}),
        }
