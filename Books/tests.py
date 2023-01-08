from django.test import TestCase
from django.urls import reverse
from .models import Book
from .serializers import BookSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import pytest

# Create your tests here.


def create_book(title='title', price=1):
    return Book.objects.create(title=title, price=price)


def create_user_token():
    User.objects.create_user('user', 'user@test.com', 'testuser')
    user = User.objects.get(username='user')
    token, _ = Token.objects.get_or_create(user=user)
    return token


def create_admin_token():
    User.objects.create_superuser('admin', 'admin@test.com', 'adminuser')
    user = User.objects.get(username='admin')
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_admin_get_all_books(api_client):
    book1 = create_book('title1', 1)
    book2 = create_book('title2', 2)
    book3 = create_book('title3', 3)

    url = reverse('Books:all_books')
    token = create_admin_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data == BookSerializer(
        [book1, book2, book3], many=True).data


@pytest.mark.django_db
def test_user_get_all_books(api_client):
    book1 = create_book('title1', 1)
    book2 = create_book('title2', 2)
    book3 = create_book('title3', 3)

    url = reverse('Books:all_books')
    token = create_user_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data == BookSerializer(
        [book1, book2, book3], many=True).data


@pytest.mark.django_db
def test_admin_add_book(api_client):
    serialized_book = BookSerializer(Book(id=1, title='book1', price=1))
    url = reverse('Books:all_books')
    token = create_admin_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
    respone = api_client.post(url, data=serialized_book.data)
    assert respone.status_code == 201
    assert respone.data == serialized_book.data


@pytest.mark.django_db
def test_user_add_book(api_client):
    serialized_book = BookSerializer(Book(id=1, title='book1', price=1))
    url = reverse('Books:all_books')
    token = create_user_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token '+token.key)
    respone = api_client.post(url, data=serialized_book.data)
    assert respone.status_code == 401
    assert respone.data['message'] == 'Not authorized'


@pytest.mark.django_db
def test_admin_get_single_book(api_client):
    book = create_book(title='book1', price=10)
    token = create_admin_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.get(url)
    assert respone.status_code == 200
    assert respone.data == BookSerializer(book).data


@pytest.mark.django_db
def test_user_get_single_book(api_client):
    book = create_book(title='book1', price=10)
    token = create_user_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.get(url)
    assert respone.status_code == 200
    assert respone.data == BookSerializer(book).data


@pytest.mark.django_db
def test_admin_update_title_single_book(api_client):
    book = create_book(title='title1', price=15)
    token = create_admin_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.put(url, data={'title': 'title2'})
    assert respone.status_code == 204
    book.title = 'title2'
    assert respone.data == BookSerializer(book).data


@pytest.mark.django_db
def test_user_update_title_single_book(api_client):
    book = create_book(title='title1', price=15)
    token = create_user_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.put(url, data={'title': 'title2'})
    assert respone.status_code == 401
    assert Book.objects.get(pk=book.id) == book


@pytest.mark.django_db
def test_admin_update_price_single_book(api_client):
    book = create_book(title='title1', price=15)
    token = create_admin_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.put(url, data={'price': 10})
    assert respone.status_code == 204
    assert respone.data != BookSerializer(book).data
    book.price = 10
    assert respone.data == BookSerializer(book).data


@pytest.mark.django_db
def test_user_update_price_single_book(api_client):
    book = create_book(title='title1', price=15)
    token = create_user_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.put(url, data={'price': 10})
    assert respone.status_code == 401
    assert Book.objects.get(pk=book.id) == book


@pytest.mark.django_db
def test_admin_update_single_book(api_client):
    book = create_book(title='title1', price=15)
    token = create_admin_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.put(url, data={'title': 'title2', 'price': 10})
    assert respone.status_code == 204
    assert respone.data != BookSerializer(book).data
    book.price = 10
    book.title = 'title2'
    assert respone.data == BookSerializer(book).data


@pytest.mark.django_db
def test_user_update_single_book(api_client):
    book = create_book(title='title1', price=15)
    token = create_user_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.put(url, data={'title': 'title2', 'price': 10})
    assert respone.status_code == 401
    assert Book.objects.get(pk=book.id) == book


@pytest.mark.django_db
def test_admin_delete_single_book(api_client):
    book = create_book(title='title1', price=15)
    token = create_admin_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.delete(url)
    assert respone.status_code == 202
    assert Book.objects.filter(id=book.id).exists() == False


@pytest.mark.django_db
def test_user_delete_single_book(api_client):
    book = create_book(title='title1', price=15)
    token = create_user_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    url = reverse('Books:single_book', kwargs={'book_id': book.id})
    respone = api_client.delete(url)
    assert respone.status_code == 401
    assert Book.objects.filter(id=book.id).exists() == True
