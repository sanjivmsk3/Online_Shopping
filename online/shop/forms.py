from django import forms
from shop.models import Address

class AddForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ("user",)