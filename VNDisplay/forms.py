from datetime import datetime
from django import forms
from .models import Post, Category
from django.db.models import Min, Max

class PostFilterForm(forms.Form):
    SORT_ORDER_CHOICES = [
        ('asc', 'Ascendente'),
        ('desc', 'Descendente'),
    ]

    SORT_FIELD_CHOICES = [
        ('date', 'Fecha'),
        ('name', 'Nombre'),
    ]


    sort_field = forms.ChoiceField(
        choices=SORT_FIELD_CHOICES, 
        initial='date', 
        widget=forms.Select(attrs={'class': 'custom-select', 'placeholder': 'Fecha', 'style': 'display: none;'}), 
        label=False
    )

    sort_order = forms.ChoiceField(
        choices=SORT_ORDER_CHOICES, 
        initial='asc', 
        widget=forms.Select(attrs={'class': 'custom-select', 'placeholder': 'Ascendente', 'style': 'display: none;'}), 
        label=False
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False, 
        widget=forms.Select(attrs={'class': 'custom-select', 'placeholder': 'Categoria', 'style': 'display: none;'}), 
        label=False,
        empty_label="Categoria"
    )
    current_year = datetime.now().year
    YEAR_CHOICES = [("", "Año")] + [(r,r) for r in range(2013, current_year + 1)]
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False, 
        widget=forms.Select(attrs={'class': 'custom-select', 'placeholder': 'Año', 'style': 'display: none;'}), 
        label=False,
    )