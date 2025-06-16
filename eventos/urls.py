from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='inicio'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('evento/editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
     path('eventos/<int:evento_id>/eliminar/', views.eliminar_evento, name='eliminar_evento'),

    path('eventos/<int:evento_id>/asistentes/', views.ver_asistentes, name='ver_asistentes'),
    path('eventos/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:evento_id>/registrar/', views.registrar_asistente, name='registro_asistente'),
    path('eventos/<int:evento_id>/inscribirse/', views.inscribirse, name='inscribirse'),
    path('eventos/<int:evento_id>/asistencia/<int:inscripcion_id>/', views.registrar_asistencia, name='registrar_asistencia'),
    path('eventos/buscar/', views.buscar_eventos, name='buscar_eventos'),
    path('eventos/<int:evento_id>/exportar-asistentes/', views.exportar_asistentes_csv, name='exportar_asistentes'),
    path('eventos/<int:evento_id>/exportar-asistentes/pdf/', views.exportar_asistentes_pdf, name='exportar_asistentes_pdf'),
    path('eventos/pasados/', views.eventos_pasados, name='eventos_pasados'),

]

