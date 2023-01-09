from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from .models import Snack
from .serializers import SnackSerializer
from rest_framework.permissions import IsAdminUser
# Create your views here.


class SnacksView(generics.ListCreateAPIView):
    queryset = Snack.objects.all()
    serializer_class = SnackSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class SingleSnackView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SnackSerializer
    queryset = Snack.objects.all()

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
