from django import forms
from django.forms import TextInput

from mainScrapy.models import *

class SearchForm(forms.ModelForm):
    class Meta:
        model = Recherche
        fields = ['texte']
        labels = {'texte': ''}
        widgets = {'texte': TextInput(attrs = {'size': 80}), }

    """def clean_texte(self):
        texte = self.cleaned_data.get("texte")
        if not texte:
            raise forms.ValidationError("Ce champ est obligatoire !")
        return texte"""
