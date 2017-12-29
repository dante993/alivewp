from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

from alive.forms import *

# @login_required(login_url='/')
# Create your views here.
class promocionOB():
    def __init__(self,nomb,descr,prdto,cod,imrl):
        self.id = cod
        self.url = imrl
        self.nombre = nomb
        self.descripcion = descr
        self.productos = prdto

def logoutView(request):
    logout(request)
    return redirect("/login/")

def loginView(request):
    mensaje="nothing"
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['cedula'],
                                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                login(request, user)
                return redirect(request.POST.get('next', '/carga_categorias/'))
            else:
                mensaje="Nombre de Usuario o clave Incorrecto"
                return render(request, "login.html", {"form": form,"mensaje":mensaje})
    return render(request, "login.html", {"form": form,"mensaje":mensaje})


def usrView(request):
    obj = Producto.objects.order_by("prd_nombre").filter(prd_estado='activo')
    obj2 = Categorias.objects.order_by("catg_nombre").filter(catg_estado='activo')
    paginator_listado = Paginator(obj, 20)
    page_listado = request.GET.get('page')
    try:
        pg_listado = paginator_listado.page(page_listado)
    except PageNotAnInteger:
        pg_listado = paginator_listado.page(1)
    except EmptyPage:
        pg_listado = paginator_listado.page(paginator_listado.num_pages)
    return render_to_response('catalogo.html',{'registros':pg_listado,'registrosc':obj2,'categ_act':'Todos'})

def usriniView(request):
    listado = []

    obj = Promociones.objects.order_by("prm_nombre")
    for i in obj:
        productosl = []
        dettemp = DetalleProm.objects.filter(prd_id=i)
        for j in dettemp:
            productosl.append(get_object_or_404(Producto, pk=j.prm_id_id))
        obtemp = promocionOB(i.prm_nombre,i.prm_descripcion,productosl,i.prm_id,i.prm_img.url)
        listado.append(obtemp)
    return render_to_response('index.html',{'categ_act':'ninguna','listado':listado})

def usrfView(request,pk):
    objcat = get_object_or_404(Categorias, pk=pk)
    obj = Producto.objects.order_by("prd_nombre").filter(prd_estado='activo',catg_id=objcat)
    obj2 = Categorias.objects.order_by("catg_nombre").filter(catg_estado='activo')
    paginator_listado = Paginator(obj, 20)
    page_listado = request.GET.get('page')
    try:
        pg_listado = paginator_listado.page(page_listado)
    except PageNotAnInteger:
        pg_listado = paginator_listado.page(1)
    except EmptyPage:
        pg_listado = paginator_listado.page(paginator_listado.num_pages)
    return render_to_response('catalogo.html',{'registros':pg_listado,'registrosc':obj2,'categ_act':objcat.catg_nombre})

# -----------------------------------------------------------------------------------------------------------------------
@login_required(login_url='/')
def cargaView(request):
    if request.method == 'POST':
        search_param=request.POST["buscar"]
        q = Producto.objects.order_by("prd_nombre").filter(prd_nombre__icontains=search_param)
        return render(request,'carga.html',{'registros':q,'ubicacion':'Listado de productos'})
    obj = Producto.objects.order_by("prd_nombre").filter(prd_estado='activo')
    paginator_listado = Paginator(obj, 20)
    page_listado = request.GET.get('page')
    try:
        pg_listado = paginator_listado.page(page_listado)
    except PageNotAnInteger:
        pg_listado = paginator_listado.page(1)
    except EmptyPage:
        pg_listado = paginator_listado.page(paginator_listado.num_pages)
    # if request.method=='POST':
    #     tip = Tipo_cancer.objects.order_by("tc_id").filter(tc_nombre__contains=request.POST["busca"],tc_estado='activo')
    #     return render_to_response('listar/tipo_cancer_list.html',{'img':img,'user':usuario})
    return render(request,'carga.html',{'registros':pg_listado,'ubicacion':'Listado de productos'})

@login_required(login_url='/')
def cargaViewin(request):
    obj = Producto.objects.order_by("prd_nombre").filter(prd_estado='inactivo')
    return render(request, 'carga_in.html',{'registros':obj,'ubicacion':'Listado de productos eliminados'})

@login_required(login_url='/')
def cargaCreate(request, template_name='carga_add.html'):
    form = productosForm(request.POST or None,request.FILES or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect("productos")
    return render(request,template_name,{'form':form,"ubicacion":'Nuevo Producto'})
#
@login_required(login_url='/')
def cargaUpdate(request,pk,template_name='carga_up.html'):
    obj = get_object_or_404(Producto, pk=pk)
    form = productosForm(request.POST or None, instance=obj)
    if form.is_valid():
        # obj.prd_nombre=request.POST.get("prd_nombre")
        # obj.prd_img=request.FILES['prd_img']
        # obj.catg_id=get_object_or_404(Producto, pk=request.POST.get("catg_id"))
        # obj.prd_precio_compra=request.POST.get("prd_precio_compra")
        # obj.prd_descripcion=request.POST.get("prd_descripcion")
        # obj.prd_estado=request.POST.get("prd_estado")
        # obj.save()
        form.save()
        return redirect("productos")
    return render(request,template_name,{'form':form,"ubicacion":'Editar producto'})
#
@login_required(login_url='/')
def cargaDelete(request,pk):
    obj = get_object_or_404(Producto, pk=pk)
    obj.prd_estado='inactivo'
    obj.save()
    return redirect("productos")

@login_required(login_url='/')
def cargaDeleteP(request,pk):
    obj = get_object_or_404(Producto, pk=pk)
    obj.delete()
    return redirect("productosin")

@login_required(login_url='/')
def cargaRestore(request,pk):
    obj = get_object_or_404(Producto, pk=pk)
    obj.prd_estado='activo'
    obj.save()
    return redirect("productosin")


# -----------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/')
def cargaCView(request):
    obj = Categorias.objects.order_by("catg_nombre").filter(catg_estado='activo')
    # if request.method=='POST':
    #     tip = Tipo_cancer.objects.order_by("tc_id").filter(tc_nombre__contains=request.POST["busca"],tc_estado='activo')
    #     return render_to_response('listar/tipo_cancer_list.html',{'img':img,'user':usuario})
    return render(request,'carga_c.html',{'registros':obj,'ubicacion':'Listado de categorias'})

@login_required(login_url='/')
def cargaCViewin(request):
    obj = Categorias.objects.order_by("catg_nombre").filter(catg_estado='inactivo')
    return render(request, 'carga_cin.html',{'registros':obj,'ubicacion':'Listado de categorias eliminadas'})

@login_required(login_url='/')
def cargaCCreate(request, template_name='cargaC_add.html'):
    form = CategoriasForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect("categorias")
    return render(request,template_name,{'form':form,"ubicacion":'Nueva categoria'})
#
@login_required(login_url='/')
def cargaCUpdate(request,pk,template_name='cargaC_add.html'):
    obj = get_object_or_404(Categorias, pk=pk)
    form = CategoriasForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("categorias")
    return render(request,template_name,{'form':form,"ubicacion":'Editar categoria'})
#
@login_required(login_url='/')
def cargaCDelete(request,pk):
    obj = get_object_or_404(Categorias, pk=pk)
    obj.catg_estado='inactivo'
    obj.save()
    return redirect("categorias")

@login_required(login_url='/')
def cargaCDeleteP(request,pk):
    obj = get_object_or_404(Categorias, pk=pk)
    obj.delete()
    return redirect("categoriasin")

@login_required(login_url='/')
def cargaCRestore(request,pk):
    obj = get_object_or_404(Categorias, pk=pk)
    obj.catg_estado='activo'
    obj.save()
    return redirect("categoriasin")

# ------------------------------------------- promociones ---------------------------------------
@login_required(login_url='/')
def promoView(request):
    listado =[]
    obj = Promociones.objects.order_by("prm_nombre")
    for i in obj:
        dettemp = DetalleProm.objects.filter(prd_id=i)
        obtemp = promocionOB(i.prm_nombre,i.prm_descripcion,dettemp,i.prm_id,i.prm_img.url)
        listado.append(obtemp)

    return render(request,'promo.html',{'registros':listado,'ubicacion':'Listado de promociones'})

@login_required(login_url='/')
def promoCreate(request, template_name='promo_add.html'):
    obj = Producto.objects.order_by("prd_nombre").filter(prd_estado='activo')
    form = promosForm(request.POST or None,request.FILES or None)
    formprm = ''
    if request.method=='POST':
        if form.is_valid():
            formprm = form.save()
        try:
            prdss= request.POST.get("productos").split(",")
            for i in prdss:
                objp = get_object_or_404(Producto, prd_id=i)
                objpm = get_object_or_404(Promociones, pk=formprm.prm_id)
                detll = DetalleProm(prm_id=objp,prd_id=objpm)
                detll.save()
        except:
            print("*******sin agregar productos a esta promocion*******")
        return redirect("promos")
    return render(request,template_name,{'registros':obj,'form':form,"ubicacion":'Nueva promocion'})

@login_required(login_url='/')
def promoDeleteP(request,pk):
    obj = get_object_or_404(Promociones, pk=pk)
    obj.delete()
    return redirect("promos")
