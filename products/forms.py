from django import forms
from .models import Review

class ProductFilterForm(forms.Form):
    name_search = forms.CharField(label="Name search", max_length=50, required=False)

class ReviewForm(forms.ModelForm):
  class Meta:
    model = Review
    fields = ['stars', 'review']