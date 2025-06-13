from django.db import models

class Servicio(models.Model):
    TIPOS_SERVICIO = [
        ('corte', 'Corte de pelo'),
        ('corte_lavado', 'Corte y lavado'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS_SERVICIO, default='corte')

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

class Reserva(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f"{self.nombre_cliente} - {self.fecha} {self.hora}"
