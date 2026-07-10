import bleach
from rest_framework.serializers import ModelSerializer, ValidationError
from chatbot.models import Conversacion


class ConversacionSerializer(ModelSerializer):
    class Meta:
        model = Conversacion
        fields = ['id', 'pregunta', 'respuesta', 'temperatura', 'usuario', 'modelo', 'creado']
        extra_kwargs = {
            "fecha_creacion": {"read_only": True},
            "fecha_actualizacion": {"read_only": True},
            "usuario": {"read_only": True},
            "respuesta": {"read_only": True},
            "pregunta": {"max_length": 500},
            "temperatura": {"max_value": 2.0, "min_value": 0.0},
            "modelo": {"max_length": 50},
        }

    def validate_pregunta(self, value):
        sanitized = bleach.clean(value, strip=True)
        if not sanitized or not sanitized.strip():
            raise ValidationError("La pregunta no puede estar vacia despues de sanitizar.")
        return sanitized
