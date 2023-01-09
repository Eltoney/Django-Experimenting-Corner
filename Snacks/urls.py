from django.urls import path
from . import views
app_name = 'Snacks'
urlpatterns = [
    path('', views.SnacksView.as_view(), name='all_snacks'),
    path('<int:pk>', views.SingleSnackView.as_view(), name='single_snack'),
]
