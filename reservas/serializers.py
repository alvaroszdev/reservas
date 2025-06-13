from rest_framework import serializers
from .models import Servicio, Reserva

class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ['id', 'nombre', 'descripcion', 'tipo']

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'servicio', 'nombre_cliente', 'email_cliente', 'fecha', 'hora']

    def validate(self, data):
        fecha = data.get('fecha')
        hora = data.get('hora')
        if Reserva.objects.filter(fecha=fecha, hora=hora).exists():
            raise serializers.ValidationError("Esa fecha y hora ya están reservadas.")
        return data
