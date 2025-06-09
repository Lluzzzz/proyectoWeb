from django.contrib import admin
from .models import Evento, Organizador, Inscripcion, Lugar

admin.site.register(Evento)
admin.site.register(Organizador)
admin.site.register(Inscripcion)
admin.site.register(Lugar)
