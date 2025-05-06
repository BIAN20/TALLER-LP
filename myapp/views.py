from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import uuid

from .models import Articulo, GrupoArticulo, LineaArticulo, ListaPrecio
from .forms import ArticuloForm, ListaPrecioForm  # Necesitaras esos forms

@login_required
def home(request):
    """Vista para la página principal"""
    total_articulos = Articulo.objects.count()
    total_usuarios = 0  # Deberías reemplazar esto por una consulta real a tu modelo de Usuario
    bajo_stock = Articulo.objects.filter(stock__lt=10).count()

    context = {
        'total_articulos': total_articulos,
        'total_usuarios': total_usuarios,
        'bajo_stock': bajo_stock,
        'ventas_hoy': 0,  # También puedes calcular las ventas reales si tienes el modelo
    }
    return render(request, 'myapp/index.html', context)

@login_required
def articulos_list(request):
    """Vista para listar artículos"""
    articulos_list = Articulo.objects.all()

    # Filtro de búsqueda
    q = request.GET.get('q')
    if q:
        articulos_list = articulos_list.filter(descripcion__icontains=q)

    # Paginación
    paginator = Paginator(articulos_list, 15)
    page_number = request.GET.get('page')
    articulos = paginator.get_page(page_number)

    context = {
        'articulos': articulos,
    }
    return render(request, 'myapp/articulos/list.html', context)

@login_required
def articulo_detail(request, articulo_id):
    """Vista para ver el detalle de un artículo"""
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)

    context = {
        'articulo': articulo,
    }
    return render(request, 'myapp/articulos/detail.html', context)

@login_required
def articulo_create(request):
    """Vista para crear un nuevo artículo"""
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        precio_form = ListaPrecioForm(request.POST)

        if form.is_valid() and precio_form.is_valid():
            articulo = form.save(commit=False)
            articulo.articulo_id = uuid.uuid4()
            articulo.save()

            lista_precio = precio_form.save(commit=False)
            lista_precio.articulo = articulo
            lista_precio.save()

            messages.success(request, 'Artículo creado correctamente.')
            return redirect('articulo_detail', articulo_id=articulo.articulo_id)
    else:
        form = ArticuloForm()
        precio_form = ListaPrecioForm()

    context = {
        'form': form,
        'precio_form': precio_form,
    }
    return render(request, 'myapp/articulos/form.html', context)

@login_required
def articulo_edit(request, articulo_id):
    """Vista para editar un artículo existente"""
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)
    lista_precio = get_object_or_404(ListaPrecio, articulo=articulo)

    if request.method == 'POST':
        form = ArticuloForm(request.POST, instance=articulo)
        precio_form = ListaPrecioForm(request.POST, instance=lista_precio)

        if form.is_valid() and precio_form.is_valid():
            form.save()
            precio_form.save()

            messages.success(request, 'Artículo actualizado correctamente.')
            return redirect('articulo_detail', articulo_id=articulo.articulo_id)
    else:
        form = ArticuloForm(instance=articulo)
        precio_form = ListaPrecioForm(instance=lista_precio)

    context = {
        'form': form,
        'precio_form': precio_form,
    }
    return render(request, 'myapp/articulos/form.html', context)

@login_required
def articulo_delete(request, articulo_id):
    """Vista para eliminar un artículo"""
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id)

    if request.method == 'POST':
        articulo.delete()
        messages.success(request, 'Artículo eliminado correctamente.')
        return redirect('articulos_list')

    context = {
        'articulo': articulo,
    }
    return render(request, 'myapp/articulos/delete.html', context)

@login_required
def get_lineas_por_grupo(request, grupo_id):
    """API para obtener líneas de artículo según el grupo seleccionado (AJAX)"""
    lineas = LineaArticulo.objects.filter(grupo_id=grupo_id, estado=1)
    data = [{'id': str(linea.linea_id), 'nombre': linea.nombre_linea} for linea in lineas]
    return JsonResponse(data, safe=False)