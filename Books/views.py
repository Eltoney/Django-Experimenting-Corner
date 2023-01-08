from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
# Create your views here.


def cleanNullTerms(d):
    return {
        k: v
        for k, v in d.items()
        if v is not None
    }


@api_view(['GET', 'POST'])
def books(request):
    if request.method == 'GET':
        all_books = Book.objects.all()
        serialized_books = BookSerializer(all_books, many=True)
        return Response(serialized_books.data, status=status.HTTP_200_OK)
    else:
        if request.user.is_superuser:
            serialized_book = BookSerializer(data=request.data)
            serialized_book.is_valid(raise_exception=True)
            serialized_book.save()
            return Response(serialized_book.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def single_book(request, book_id):
    if request.method == 'GET':
        book = get_object_or_404(Book, pk=book_id)
        serialized_book = BookSerializer(book)
        return Response(serialized_book.data, status=status.HTTP_200_OK)
    if request.user.is_superuser:
        if request.method == 'PUT':

            attrs = {'title': None, 'price': None}
            attrs['title'] = request.data.get('title')
            attrs['price'] = request.data.get('price')
            attrs = cleanNullTerms(attrs)

            book = get_object_or_404(Book, pk=book_id)
            Book.objects.filter(pk=book_id).update(**attrs)
            serialized_book = BookSerializer(Book.objects.get(pk=book_id))
            return Response(serialized_book.data, status=status.HTTP_204_NO_CONTENT)
        else:
            book = get_object_or_404(Book, pk=book_id)
            book.delete()
            return Response({'message': 'ok'}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({'message': 'Not authorized'}, status=status.HTTP_401_UNAUTHORIZED)
