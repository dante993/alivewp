from alive.models import *
from django import forms
from django.forms import Form, CharField, TextInput
from django.contrib.auth import authenticate

class LoginForm(Form):
    cedula = CharField(max_length=10, widget=TextInput(attrs=
                                                          {"class": "validate black-text",
                                                           "type": "text"}))
    password = CharField(max_length=30, widget=TextInput(attrs=
                                                          {"class": "validate black-text",
                                                           "type": "password"}))

class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        widgets={
            'catg_nombre':forms.TextInput(attrs={
                'class':'validate black-text'
            }),
            'catg_descripcion':forms.Textarea(attrs={
                'class':'materialize-textarea black-text'
            }),
            'catg_estado':forms.Select(attrs={
                'class':''
            })
        }
        fields = '__all__'

class productosForm(forms.ModelForm):
    class Meta:
        model = Producto
        widgets={
            'prd_nombre':forms.TextInput(attrs={
                'class':'validate black-text'
            }),
            'prd_img':forms.FileInput(attrs={
                'class':'black-text',
                'accept':'image/*'
            }),
            'catg_id':forms.Select(attrs={
                'class':'browser-default black-text'
            }),
            'prd_precio_compra':forms.NumberInput(attrs={
                'class':'validate black-text'
            }),
            'prd_descripcion':forms.Textarea(attrs={
                'class':'materialize-textarea black-text',
            }),
            'prd_estado':forms.Select(attrs={
                'class':'browser-default'
            })
        }
        fields = '__all__'

class promosForm(forms.ModelForm):
    class Meta:
        model = Promociones
        widgets={
            'prm_nombre':forms.TextInput(attrs={
                'class':'validate black-text'
            }),
            'prm_img':forms.FileInput(attrs={
                'class':'black-text',
                'accept':'image/*'
            }),
            'prm_descripcion':forms.Textarea(attrs={
                'class':'materialize-textarea black-text',
            })
        }
        fields = '__all__'
