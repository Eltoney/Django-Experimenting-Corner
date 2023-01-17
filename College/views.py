from django.shortcuts import render, get_object_or_404
from .models import Course
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
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

    @action(detail=False)
    def collect_students(self, request):
        queryset = Course.objects.all()
        tot = 0
        for item in queryset:
            tot += item.total_students
        return Response(tot)

    @action(detail=True, methods=['patch'])
    def add_students(self, request, pk=None):
        add = request.data['add']
        course = get_object_or_404(Course, pk=pk)
        course.total_students += int(add)
        course.save()
        return Response({'message': 'ok'})
