from django.shortcuts import render, get_object_or_404
from .models import Course
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import CourseSerializer
# Create your views here.


class CourseViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Course.objects.all()
        serialized = CourseSerializer(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Course, pk=pk)
        serialized = CourseSerializer(queryset)
        return Response(serialized.data)
