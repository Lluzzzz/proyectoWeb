from django.db import models

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Organizador(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    organizador = models.ForeignKey(Organizador, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Inscripcion(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='inscripciones')
    nombre_participante = models.CharField(max_length=100)
    email = models.EmailField()
    asistio = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre_participante} - {self.evento.titulo}"
