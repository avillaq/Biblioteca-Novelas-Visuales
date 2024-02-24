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

    # Campo select para : fecha, nombre (por defecto fecha)
    sort_field = forms.ChoiceField(choices=SORT_FIELD_CHOICES, initial='date', widget=forms.Select())

    # Campo select para : ascendentemente o descendentemente
    sort_order = forms.ChoiceField(choices=SORT_ORDER_CHOICES, initial='asc', widget=forms.Select())

    # Campo select para : categoria ( sacados del modelo Category)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, widget=forms.Select())

    # Campo select para : año (es una lista de años de los post)
    YEAR_CHOICES = [(r,r) for r in range(2010, 2025)]
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=False, widget=forms.Select())