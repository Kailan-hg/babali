from django import forms
from .models import NewProductForm as ProductForm


class NewProductForm(forms.ModelForm):
    class Meta:
        model = ProductForm
        fields = "__all__"
