from rest_framework import serializers
from apps.clientes.models.clientes import Cliente
from django.core.validators import MinLengthValidator,MaxLengthValidator

from datetime import date


class clientSerializersView(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    nombre_completo = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    fecha_nacimiento = serializers.DateField(read_only=True)
    fecha_creacion = serializers.DateField(read_only=True)
    numero_documento = serializers.DateField(read_only=True)


class clientSerializers(serializers.Serializer):
    nombre_completo = serializers.CharField()
    email = serializers.EmailField(error_messages={"invalid":"Formato invalido"})
    fecha_nacimiento = serializers.DateField(input_formats=['%Y-%m-%d'])
    numero_documento = serializers.CharField(validators=[MinLengthValidator(8,"Debe ser de minimo 8 digitos"),MaxLengthValidator(12,"Debe tener menos de 12 digitos")])
    
    def validate_fecha_nacimiento(self, value):
        
        fecha_str = value.strftime('%Y-%m-%d')

        if fecha_str != self.initial_data.get('fecha_nacimiento'):
            raise serializers.ValidationError('El formato de fecha debe ser yyyy-mm-dd.')
        
        if value < date(1950, 1, 1):
            raise serializers.ValidationError('La fecha debe ser mayor a 2023-01-01.')

        return value
    
    
    def validate_email(self, value):
        if Cliente.objects.filter(email=value).exists():
            raise serializers.ValidationError('Ya existe un registro con este email.')
        
        return value
    
    def validate_numero_documento(self, value):
        if Cliente.objects.filter(numero_documento=value).exists():
            raise serializers.ValidationError('Ya existe un registro con este numero de documento.')
        
        return value

    def create(self, validated_data):
        instance = Cliente.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        instance.nombre_completo = validated_data.get(
            "nombre_completo", instance.nombre_completo
        )
        instance.email = validated_data.get("email", instance.email)
        instance.fecha_nacimiento = validated_data.get(
            "fecha_nacimiento", instance.fecha_nacimiento
        )
        instance.numero_documento = validated_data.get(
            "numero_documento", instance.numero_documento
        )
        instance.save()
        return instance
