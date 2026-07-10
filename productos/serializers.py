from rest_framework import serializers
from .models import *

class ProductoSerializer(serializers.ModelSerializer):
    subcategoria = serializers.ReadOnlyField(source='subcategoria.nombre')
    class Meta:
        model = Producto
        fields = ['id','nombre','precio','descripcion','subcategoria','cantidad','imagen', 'caracteristicas']

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id','nombre']

class SubcategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategoria
        fields = '__all__'
