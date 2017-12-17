"""alive_wp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from alive.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # url(r'^admin/', admin.site.urls),(?P<pk>.*)

    url(r'^login/$', loginView, name='login'),
    url(r'^logout/$', logoutView, name='logout'),
    # url(r'^inicio/$', inicioView, name='inicio_view'),cargaCCreate

    url(r'^catalogo/$', usrView, name='catalogo'),
    url(r'^catalogo/filtro/(?P<pk>.*)/$', usrfView, name='catalogof'),

    url(r'^carga_categorias/$', cargaCView, name='categorias'),
    url(r'^carga_categorias/eliminados/$', cargaCViewin, name='categoriasin'),
    url(r'^carga_categorias/nuevo/$', cargaCCreate, name='categoriasadd'),
    url(r'^carga_categorias/editar/(?P<pk>.*)/$', cargaCUpdate, name='categoriasedd'),
    url(r'^carga_categorias/delete/(?P<pk>.*)/$', cargaCDelete, name='categoriasdel'),
    url(r'^carga_categorias/deletep/(?P<pk>.*)/$', cargaCDeleteP, name='categoriasdelp'),
    url(r'^carga_categorias/restore/(?P<pk>.*)/$', cargaCRestore, name='categoriasres'),


    url(r'^carga_productos/$', cargaView, name='productos'),
    url(r'^carga_productos/eliminados/$', cargaViewin, name='productosin'),
    url(r'^carga_productos/nuevo/$', cargaCreate, name='productosadd'),
    url(r'^carga_productos/editar/(?P<pk>.*)/$', cargaUpdate, name='productosedd'),
    url(r'^carga_productos/delete/(?P<pk>.*)/$', cargaDelete, name='productosdel'),
    url(r'^carga_productos/deletep/(?P<pk>.*)/$', cargaDeleteP, name='productosdelp'),
    url(r'^carga_productos/restore/(?P<pk>.*)/$', cargaRestore, name='productosres'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
