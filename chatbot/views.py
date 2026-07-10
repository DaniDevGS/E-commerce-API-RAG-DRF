import logging
from django.utils.html import escape
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from chatbot.models import Conversacion
from chatbot.serializers import ConversacionSerializer
from chatbot.rag import generar_respuesta, limpiar_respuesta
from chatbot.vectors import buscar_productos_similares
from productos.utils.conversion import obtener_cambio
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

class ChatbotView(APIView):
    serializer_class = ConversacionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        engine = request.query_params.get('engine', "groq").lower()
        pregunta = serializer.validated_data["pregunta"].lower() # type: ignore

        resultados = buscar_productos_similares(pregunta, top_k=5)

        cambio_bolivar = obtener_cambio()
        if cambio_bolivar:
            cambio_bolivar = Decimal(str(cambio_bolivar))

        if resultados:
            contexto_lineas = []
            for res in resultados:
                p_nombre = res.metadata.get('nombre', 'Producto') # type: ignore
                p_precio = res.metadata.get('precio', 0) # type: ignore
                p_texto = res.data

                precio_bs_str = ""
                if cambio_bolivar:
                    precio_bs = round(Decimal(str(p_precio)) * cambio_bolivar, 2)
                    precio_bs_str = f" | Precio Bs: {precio_bs}"

                contexto_lineas.append(f"- {p_texto} | Precio USD: {p_precio}{precio_bs_str}")

            contexto = "\n".join(contexto_lineas)
        else:
            contexto = "No se encontraron productos especificos relacionados en el inventario."

        SYSTEM_PROMPT = (
            "Eres un asistente virtual del eCommerce de Tech Store te llamas Techty, eres alguien amigable pero tambien alguien profesional como un amigo dentro del sistema para el usuario."
            "Usa solo la informacion provista en el 'CONTEXT' para responder sobre productos. "
            "Si te preguntan cosas basicas o saludos, se amable y responde con naturalidad, no bloquees la conversacion. "
            "Consultas sobre productos, disponibilidad, recomendaciones basadas en necesidades y gustos son tu especialidad. "
            "Si no puedes responder con la informacion del contexto, indicalo de forma amable, sin ser demasiado cerrado."
        )
        historial_usuario = Conversacion.objects.filter(usuario=request.user).order_by('-creado')[:3]
        historial_plano = "".join([
            f"\nPregunta: {h.pregunta.lower()}\nAsistente: {h.respuesta.lower()}" for h in historial_usuario]
        )
        prompt = (
            f"{SYSTEM_PROMPT}\n\n"
            f"=== CONTEXT ===\n{contexto}\n\n"
            f"=== HISTORIAL RELEVANTE ===\n"
            f"{historial_plano}" if historial_plano else "Sin historial previo relevante.\n"
            f"\n=== INSTRUCCION ===\n"
            "Responde solo con informacion del contexto pero tambien responde preguntas basicas de una manera amigable. Se claro, conciso pero tambien algo creativo no seas alguien de pocas palabras y emite la respuesta en texto plano.\n"
        )
        temperatura = serializer.validated_data.get("temperatura", 0.7) # type: ignore
        modelo = serializer.validated_data.get("modelo", "modelo_base") # type: ignore
        try:
            logger.debug("Engine: %s, Modelo: %s", engine, modelo)
            respuesta = generar_respuesta(prompt, pregunta, temperatura=temperatura, engine=engine)
            LISTA_ERROR = ["No puedo responder a esa pregunta.",
                           "No puedo responder a tu pregunta.", "No puedo responder a tu pregunta", ""]
            if respuesta and respuesta not in LISTA_ERROR:
               respuesta_limpia = escape(limpiar_respuesta(respuesta))
               Conversacion.objects.create(pregunta=pregunta, respuesta=respuesta_limpia, usuario=request.user, temperatura=temperatura)
               return Response({"pregunta": escape(pregunta), "respuesta": respuesta_limpia})
        except Exception as e:
            logger.exception("Error en chatbot")
            return Response({"error": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"pregunta": escape(pregunta), "respuesta": escape(respuesta)})

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Autenticacion requerida"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        conversacion = Conversacion.objects.filter(usuario=request.user)
        serializer = ConversacionSerializer(conversacion, many=True)
        return Response(serializer.data)