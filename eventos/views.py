from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Evento, Inscripcion, Lugar
from .forms import InscripcionForm, EventoForm
from django.contrib import messages
from django.http import HttpResponse
import csv
from datetime import date
from django.shortcuts import get_object_or_404
from .models import Evento, Inscripcion
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# -------------------------------
# Página de Inicio
# -------------------------------

def index(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('lista_eventos') 
        else:
            return render(request, 'eventos/inicio.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'eventos/inicio.html')
#__________________-------------
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
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
        form = EventoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_eventos')
    else:
        form = EventoForm()
    
    return render(request, 'eventos/crear_evento.html', {'form': form})


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


# -------------------------------
# Ver Asistentes
# -------------------------------
def ver_asistentes(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    asistentes = Inscripcion.objects.filter(evento=evento)
    
    return render(request, 'eventos/lista-asistentes.html', {
        'evento': evento,
        'asistentes': asistentes
    })


# -------------------------------
# Eliminar Evento
# -------------------------------
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, "Evento eliminado correctamente.")
        return redirect('lista_eventos')
    return render(request, 'eventos/confirmar_eliminar.html', {'evento': evento})


# -------------------------------
# Editar Evento
# -------------------------------
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento actualizado correctamente.")
            return redirect('detalle_evento', evento_id=evento.id)
    else:
        form = EventoForm(instance=evento)
    
    return render(request, 'eventos/editar_evento.html', {'form': form, 'evento': evento})


# -------------------------------
# BUSCAR EVENTOS
# -------------------------------
def buscar_eventos(request):
    query = request.GET.get('q', '')
    resultados = Evento.objects.filter(titulo__icontains=query)
    return render(request, 'eventos/buscar_eventos.html', {
        'eventos': resultados,
        'query': query
    })


# -------------------------------
# EXPORTAR ASISTENTES A CSV
# -------------------------------
def exportar_asistentes_csv(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    asistentes = Inscripcion.objects.filter(evento=evento)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="asistentes_{evento.titulo}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Email', 'Asistió'])

    for a in asistentes:
        writer.writerow([
            a.nombre_participante,
            a.email,  
            'Sí' if a.asistio else 'No'
        ])

    return response

# -------------------------------
# EXPORTAR ASISTENTES A PDF
# -------------------------------

def exportar_asistentes_pdf(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    asistentes = Inscripcion.objects.filter(evento=evento)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setTitle(f"Asistentes - {evento.titulo}")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, f"Asistentes al evento: {evento.titulo}")
    p.setFont("Helvetica", 12)
    p.drawString(50, 730, f"Fecha: {evento.fecha}  -  Hora: {evento.hora}")

    y = 700
    for a in asistentes:
        estado = "✅ Asistió" if a.asistio else "❌ No asistió"
        p.drawString(50, y, f"- {a.nombre_participante} ({a.email}) — {estado}")
        y -= 20
        if y < 60:
            p.showPage()
            y = 750

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename=f"asistentes_{evento.titulo}.pdf")


    # -------------------------------
    #  VER EVENTOS PASADOS
    # -------------------------------
    def eventos_pasados(request):
    eventos = Evento.objects.filter(fecha__lt=date.today()).order_by('-fecha')
    return render(request, 'eventos/eventos_pasados.html', {'eventos': eventos})
