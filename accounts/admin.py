from django.contrib import admin
from .models import DispositivoMovil, Perfil, Usuario, UbicacionDispositivo
# Register your models here.

admin.site.register(DispositivoMovil)
admin.site.register(Perfil)
admin.site.register(UbicacionDispositivo)

admin.site.register(Usuario)