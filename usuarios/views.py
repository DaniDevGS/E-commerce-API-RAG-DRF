import logging
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from .serializers import UsuarioSerializer

logger = logging.getLogger(__name__)

class UsuarioViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(
            **serializer.validated_data,
            is_staff=False,
            is_superuser=False
        )

        return Response(
            UsuarioSerializer(user).data,
            status=status.HTTP_201_CREATED
        )
