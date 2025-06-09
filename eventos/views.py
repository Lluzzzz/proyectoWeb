from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Evento, Inscripcion, Lugar
from .forms import InscripcionForm

# -------------------------------
# Página de Inicio
# -------------------------------
def index(request):
    eventos = Evento.objects.filter(fecha__gte=timezone.now().date()).order_by('fecha')
    return render(request, 'eventos/base.html', {'eventos': eventos})


# -------------------------------
# Lista de Eventos
# -------------------------------
def lista_eventos(request):
    eventos = Evento.objects.filter(fecha__gte=timezone.now().date()).order_by('fecha')
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})


# -------------------------------
# Crear Evento
# -------------------------------
def crear_evento(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        lugar_id = request.POST.get('lugar')

        if titulo and descripcion and fecha and hora and lugar_id:
            lugar = Lugar.objects.get(id=lugar_id)
            Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha=fecha,
                hora=hora,
                lugar=lugar
            )
            return redirect('lista_eventos')
        else:
            error = "Todos los campos son obligatorios."
            lugares = Lugar.objects.all()
            return render(request, 'eventos/crear_evento.html', {'error': error, 'lugares': lugares})

    lugares = Lugar.objects.all()
    return render(request, 'eventos/crear_evento.html', {'lugares': lugares})

# -------------------------------
# Registrar Asistente a Evento
# -------------------------------
def registrar_asistente(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre_participante')
        email = request.POST.get('email_participante')
        
        if nombre and email:
            Inscripcion.objects.create(
                evento=evento,
                nombre_participante=nombre,
                email_participante=email
            )
            return redirect('detalle_evento', evento_id=evento.id)

    return render(request, 'eventos/registrar_asistencia.html', {'evento': evento})


# -------------------------------
# Detalle de Evento
# -------------------------------
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    return render(request, 'eventos/detalle_evento.html', {'evento': evento})


# -------------------------------
# Inscribirse (con formulario)
# -------------------------------
def inscribirse(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.evento = evento
            inscripcion.save()
            return redirect('lista_eventos')
    else:
        form = InscripcionForm()
    
    return render(request, 'eventos/inscribirse.html', {
        'form': form,
        'evento': evento
    })


# -------------------------------
# Registrar asistencia presencial
# -------------------------------
def registrar_asistencia(request, evento_id, inscripcion_id):
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id, evento_id=evento_id)
    
    if not inscripcion.asistio:
        inscripcion.asistio = True
        inscripcion.save()
        mensaje = f"Asistencia registrada para {inscripcion.nombre_participante}."
    else:
        mensaje = f"{inscripcion.nombre_participante} ya había sido marcado como asistente."

    return render(request, 'eventos/asistencia_registrada.html', {
        'mensaje': mensaje,
        'evento': inscripcion.evento,
        'inscripcion': inscripcion
    })
