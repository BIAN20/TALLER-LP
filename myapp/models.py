from django.db import models
from my_project2.choices import EstadoEntidades
class GrupoArticulo(models.Model):
    grupo_id = models.UUIDField(primary_key=True)
    codigo_grupo = models.CharField(max_length=5, null=False)
    nombre_grupo = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    def __str__(self):
        return self.nombre_grupo

    class Meta:
        db_table = "grupos_articulos"
        ordering  = ["codigo_grupo"]

class LineaArticulo(models.Model):
    linea_id = models.UUIDField(primary_key=True)
    codigo_linea = models.CharField(max_length=10, null=False)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='grupo_linea', db_column='grupo_id')
    nombre_linea = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    
    class Meta:
        db_table = "lineas_articulos"
        ordering = ["codigo_linea"]

class Articulo(models.Model):
    articulo_id = models.UUIDField(primary_key=True)
    codigo_articulo = models.CharField(max_length=25, null=False)
    codigo_barras = models.CharField(max_length=250, null=True)
    descripcion = models.CharField(max_length=500, null=False)
    presentacion = models.CharField(max_length=500, null=True)
    grupo = models.ForeignKey(GrupoArticulo,on_delete=models.RESTRICT,null=False,related_name='articulo_grupo',db_column='grupo_id')
    linea = models.ForeignKey(LineaArticulo,on_delete=models.RESTRICT,null=False,related_name='articulo_linea',db_column='linea_id')
    stock = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    class Meta:
        db_table = 'articulo'
        ordering = ['articulo_id']


class ListaPrecio(models.Model):
    articulo_id = models.ForeignKey(Articulo, on_delete=models.RESTRICT, null=False, related_name='lista_articulo')
    precio_1 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_2 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_3 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_4 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    class Meta:
        db_table = 'lista_precio'
        ordering = ['articulo_id']
class CanalCliente(models.Model):
    canal_id = models.UUIDField(primary_key=True)
    nombre_canal = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'canal_cliente'
        ordering = ['canal_id']

class Cliente(models.Model):
    cliente_id = models.UUIDField(primary_key=True)
    nro_identificacion =  models.CharField(max_length=12, null=False)
    nombres = models.CharField(max_length=150, null=False)
    direccion = models.CharField(max_length=150, null=False)
    correo_electronico = models.CharField(max_length=255, null=False)
    nro_movil = models.CharField(max_length=15, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)
    canal_id = models.ForeignKey(CanalCliente, on_delete=models.RESTRICT, null=False, related_name='cliente_canal', db_column='canal_id')

    class Meta:
        db_table = 'cliente'
        ordering = ['cliente_id']
        
class Pedido(models.Model):
    pedido_id = models.UUIDField(primary_key=True)
    nro_pedido = models.IntegerField(null=False)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=False, related_name='cliente_pedido', db_column='cliente_id')
    importe = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = 'pedido'
        ordering = ['pedido_id']

class ItemPedido(models.Model):
    item_id = models.UUIDField(primary_key=True)
    pedido_id = models.ForeignKey(Pedido, on_delete=models.RESTRICT, null=False, related_name='itemp_pedido',db_column='pedido_id')
    articulo_id = models.ForeignKey(Articulo, on_delete=models.RESTRICT, null=False, related_name='itemp_articulo', db_column='articulo_id')
    cantidad = models.IntegerField(null=False)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    estado = models.IntegerField(choices=EstadoEntidades, default=EstadoEntidades.ACTIVO)

    class Meta:
        db_table = 'item_pedido'
        ordering = ['item_id']