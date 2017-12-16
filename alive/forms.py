from alive.models import *
from django import forms
from django.forms import Form, CharField, TextInput
from django.contrib.auth import authenticate

class LoginForm(Form):
    cedula = CharField(max_length=10, widget=TextInput(attrs=
                                                          {"class": "validate",
                                                           "type": "text"}))
    password = CharField(max_length=30, widget=TextInput(attrs=
                                                          {"class": "validate",
                                                           "type": "password"}))

class CategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        widgets={
            'catg_nombre':forms.TextInput(attrs={
                'class':'validate'
            }),
            'catg_descripcion':forms.Textarea(attrs={
                'class':'materialize-textarea'
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
                'class':'validate'
            }),
            'prd_img':forms.FileInput(attrs={
                'class':'',
                'accept':'image/*'
            }),
            'catg_id':forms.Select(attrs={
                'class':'browser-default'
            }),
            'prd_precio_compra':forms.NumberInput(attrs={
                'class':'validate'
            }),
            'prd_descripcion':forms.Textarea(attrs={
                'class':'materialize-textarea',
            }),
            'prd_estado':forms.Select(attrs={
                'class':'browser-default'
            })
        }
        fields = '__all__'
