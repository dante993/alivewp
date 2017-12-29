from __future__ import unicode_literals
from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager,models.Manager):
    def _create_user(self,cedula,nombres,apellidos,e_mail,password,is_staff,
                    is_superuser,**extra_fields):
        e_mail=self.normalize_email(e_mail)
        if not e_mail:
            raise ValueError('Debe Ingresar un e-mail Obligatoriamente!')
        user = self.model(cedula=cedula,nombres=nombres,apellidos=apellidos,e_mail=e_mail,is_staff=is_staff,
                            is_active=True,is_superuser=is_superuser,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,cedula,nombres,apellidos,e_mail,password=None,**extra_fields):
        return self._create_user(cedula,nombres,apellidos,e_mail,password,False,False,**extra_fields)

    def create_superuser(self,cedula,nombres,apellidos,e_mail,password=None,**extra_fields):
        return self._create_user(cedula,nombres,apellidos,e_mail,password,True,True,**extra_fields)

def validar_cedula(value):
        ced_cliente=value
        msg = "La Cedula introducida no es valida"
        if ced_cliente.isdigit():
            cant_num_cedula=len(ced_cliente.split()[0])
            msg = "La Cedula introducida no es valida"
            if cant_num_cedula == 10 :
                valores = [ int(ced_cliente[x]) * (2 - x % 2) for x in range(9) ]
                suma = sum(map(lambda x: x > 9 and x - 9 or x, valores))
                veri = 10 - (suma - (10 * (suma / 10)))
                if int(ced_cliente[9]) == 10 - int(str(suma)[-1:]):
                    return ced_cliente
                else:
                    raise forms.ValidationError(msg)
            else:raise forms.ValidationError(msg)
        else:raise forms.ValidationError("Esto no es un numero de cedula")

class User (AbstractBaseUser,PermissionsMixin):
    cedula = models.CharField(primary_key=True,max_length = 10,validators=[validar_cedula])
    nombres = models.CharField(max_length = 50)
    apellidos = models.CharField(max_length = 50)
    e_mail = models.EmailField()
    telefono = models.CharField(max_length = 25)
    direccion=models.CharField(max_length = 200)
    SEXO_CHOICES = (
        (u'm', u'Male'),
        (u'f', u'Female'),
    )
    sexo=models.CharField(max_length = 2,choices=SEXO_CHOICES,null=True)
    fecha_de_nacimiento=models.DateField(null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    object=UserManager()

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['e_mail','nombres','apellidos']
    def __str__(self):
        strgn=self.cedula
        return strgn
admin.site.register(User)

class Categorias(models.Model):
    catg_id = models.AutoField(primary_key=True)
    catg_nombre = models.CharField(max_length = 25,verbose_name="Nombre")
    catg_descripcion=models.TextField(verbose_name="Descripción",null=True)
    ESTADO_CHOICES =((u'activo',u'Activo'),
                    (u'inactivo',u'Inactivo'),)
    catg_estado = models.CharField(max_length = 8,choices=ESTADO_CHOICES, default='activo',verbose_name="Estado")
    def __str__(self):
        return self.catg_nombre

class Producto(models.Model):
    prd_id = models.AutoField(primary_key=True)
    prd_nombre = models.CharField(max_length = 30,verbose_name="Nombre")
    prd_img = models.ImageField(upload_to="prd_img")
    catg_id = models.ForeignKey(Categorias,verbose_name="Categoría")
    prd_precio_compra = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Precio de compra")
    prd_descripcion=models.TextField(verbose_name="Descripción",null=True)
    ESTADO_CHOICES =((u'activo',u'Activo'),
                    (u'inactivo',u'Inactivo'),)
    prd_estado = models.CharField(max_length = 8,choices=ESTADO_CHOICES, default='activo',verbose_name="Estado")
    def __str__(self):
        return self.prd_nombre

class Promociones(models.Model):
    prm_id = models.AutoField(primary_key=True)
    prm_img = models.ImageField(upload_to="prm_img",blank=True,null=True)
    prm_nombre = models.CharField(max_length = 50,verbose_name="Nombre",default='')
    prm_descripcion = models.TextField(verbose_name="Descripción",null=True)

class DetalleProm(models.Model):
    prm_id =models.ForeignKey(Producto,verbose_name="Producto",on_delete=models.CASCADE)
    prd_id=models.ForeignKey(Promociones,verbose_name="Promociones",on_delete=models.CASCADE)
