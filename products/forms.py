from django import forms

class ProductFilterForm(forms.Form):
    name = forms.CharField(required=False, label="Product Name")
    category = forms.CharField(required=False, label="Category")
