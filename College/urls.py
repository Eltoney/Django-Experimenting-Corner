from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path, include

router = DefaultRouter()
router.register(r'courses', views.CourseViewSet ,basename='c')
urlpatterns = [
    path('', include(router.urls))
]
