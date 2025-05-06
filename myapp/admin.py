from django.contrib import admin
from .models import Cliente, CanalCliente, GrupoArticulo, LineaArticulo, Articulo, ListaPrecio, Pedido, ItemPedido

# Registra los modelos
admin.site.register(Cliente)
admin.site.register(CanalCliente)
admin.site.register(GrupoArticulo)
admin.site.register(LineaArticulo)
admin.site.register(Articulo)
admin.site.register(ListaPrecio)
admin.site.register(Pedido)
admin.site.register(ItemPedido)
