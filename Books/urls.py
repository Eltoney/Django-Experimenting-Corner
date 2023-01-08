from django.urls import path
from . import views
app_name = 'Books'
urlpatterns = [
    path('', views.books, name='all_books'),
    path('<int:book_id>', views.single_book, name='single_book'),
]
