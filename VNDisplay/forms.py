from datetime import datetime
from django import forms
from .models import Post, Category
from django.db.models import Min, Max

class PostFilterForm(forms.Form):
    ORDER_CHOICES = [
        ('asc', 'Ascendente'),
        ('desc', 'Descendente'),
    ]

    FIELD_CHOICES = [
        ('publication_date', 'Fecha'),
        ('title', 'Nombre'),
    ]


    field = forms.ChoiceField(
        choices=FIELD_CHOICES, 
        initial='publication_date', 
        widget=forms.Select(attrs={'class': 'custom-select', 'style': 'display: none;'}), 
        label=False
    )

    order = forms.ChoiceField(
        choices=ORDER_CHOICES, 
        initial='desc', 
        widget=forms.Select(attrs={'class': 'custom-select', 'style': 'display: none;'}), 
        label=False
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False, 
        widget=forms.Select(attrs={'class': 'custom-select', 'style': 'display: none;'}), 
        label=False,
        empty_label="Categoria"
    )
    current_year = datetime.now().year
    YEAR_CHOICES = [("", "Año")] + [(r,r) for r in range(2013, current_year + 1)]
    year = forms.ChoiceField(
        choices=YEAR_CHOICES,
        required=False, 
        widget=forms.Select(attrs={'class': 'custom-select', 'style': 'display: none;'}), 
        label=False,
    )