from .models import Snack
from rest_framework import serializers


class SnackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = ['id', 'name', 'price', 'available']
