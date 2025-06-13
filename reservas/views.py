from datetime import time, datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localdate
from .models import Reserva, Servicio
from rest_framework import viewsets
from .serializers import ServicioSerializer, ReservaSerializer
from django.core.mail import send_mail
from django.conf import settings

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

HORAS_DISPONIBLES = [
    time(8, 0), time(9, 0), time(10, 0), time(11, 0), time(12, 0), time(13, 0),
    time(14, 0), time(15, 0), time(16, 0), time(17, 0), time(18, 0), time(19, 0),
    time(20, 0), time(21, 0)
]

def calendario(request):
    fecha_seleccionada = request.GET.get('fecha') or str(localdate())

    reservas = Reserva.objects.filter(fecha=fecha_seleccionada).values_list('hora', flat=True)
    horas_reservadas = list(reservas)
    horas_libres = [hora.strftime('%H:%M') for hora in HORAS_DISPONIBLES if hora not in horas_reservadas]

    servicios = Servicio.objects.all()
    
    if request.method == 'POST':
        servicio_id = request.POST.get('servicio')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        fecha = request.POST.get('fecha')
        hora_str = request.POST.get('hora')
        hora = datetime.strptime(hora_str, '%H:%M').time()

        if Reserva.objects.filter(fecha=fecha, hora=hora).exists():
            messages.error(request, "Esa fecha y hora ya está reservada.")
        else:
            servicio_obj = Servicio.objects.get(id=servicio_id)
            Reserva.objects.create(
                servicio=servicio_obj,
                nombre_cliente=nombre,
                email_cliente=email,
                fecha=fecha,
                hora=hora
            )

            # Enviar correo de confirmación al cliente
            asunto = "Confirmación de reserva"
            mensaje = f"""
Hola {nombre},

Tu reserva ha sido confirmada con los siguientes datos:

- Servicio: {servicio_obj.nombre}
- Fecha: {fecha}
- Hora: {hora.strftime('%H:%M')}

Gracias por confiar en nosotros.
"""
            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [email],  # Correo del cliente
                fail_silently=False,
            )

            messages.success(request, "Reserva realizada con éxito.")
            return redirect(f'/calendario/?fecha={fecha}')

    context = {
        'fecha': fecha_seleccionada,
        'horas_libres': horas_libres,
        'servicios': servicios,
    }
    return render(request, 'reservas/calendario.html', context)


def calendario_reservas(request):
    return render(request, "reservas.html")

def home(request):
    return render(request, 'peluqueria/home.html')

# Aquí la vista para borrar un servicio:
def borrar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    servicio.delete()
    messages.success(request, "Servicio borrado correctamente.")
    return redirect('calendario')  # Cambia 'calendario' por la vista donde listas tus servicios
