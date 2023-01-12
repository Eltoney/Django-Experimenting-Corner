from django.test import TestCase
import pytest
from django.urls import reverse
from .models import Snack
from .serializers import SnackSerializer
from pytest_gloabl_helpers import (
    admin_api_client, user_api_client)
# Create your tests here.


def create_snack(name='snack', price='0', available=False):
    return Snack.objects.create(name=name, price=price, available=available)


@pytest.mark.django_db
def test_admin_show_all_snacks(admin_api_client):
    snack1 = create_snack('snack1')
    snack2 = create_snack('snack2')
    snack3 = create_snack('snack3')
    url = reverse('Snacks:all_snacks')
    response = admin_api_client.get(url)
    print(dir(response))
    assert response.status_code == 200
    assert response.data == SnackSerializer(
        [snack1, snack2, snack3], many=True).data


@pytest.mark.django_db
def test_user_show_all_snacks(user_api_client):
    snack1 = create_snack('snack4')
    snack2 = create_snack('snack5')
    snack3 = create_snack('snack6')
    url = reverse('Snacks:all_snacks')
    response = user_api_client.get(url)
    print(dir(response))
    assert response.status_code == 200
    assert response.data == SnackSerializer(
        [snack1, snack2, snack3], many=True).data


@pytest.mark.django_db
def test_admin_create_snack(admin_api_client):
    snack = Snack(id=1, name='snack', price='1', available=True)
    url = reverse('Snacks:all_snacks')
    response = admin_api_client.post(url, data=SnackSerializer(snack).data)
    assert response.status_code == 201
    assert response.data == SnackSerializer(snack).data


@pytest.mark.django_db
def test_user_create_snack(user_api_client):
    snack = Snack(id=1, name='snack', price='1', available=True)
    url = reverse('Snacks:all_snacks')
    response = user_api_client.post(url, data=SnackSerializer(snack).data)
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_view_single_snack(admin_api_client):
    snack = create_snack(name='snack')
    url = reverse('Snacks:single_snack', kwargs={'pk': snack.id})
    response = admin_api_client.get(url)
    assert response.status_code == 200
    assert response.data == SnackSerializer(snack).data


@pytest.mark.django_db
def test_user_view_single_snack(user_api_client):
    snack = create_snack(name='snack')
    url = reverse('Snacks:single_snack', kwargs={'pk': snack.id})
    response = user_api_client.get(url)
    assert response.status_code == 200
    assert response.data == SnackSerializer(snack).data


@pytest.mark.django_db
def test_admin_delete_snack(admin_api_client):
    snack = create_snack(name='snack1')
    url = reverse('Snacks:single_snack', kwargs={'pk': snack.id})
    respone = admin_api_client.delete(url)
    assert respone.status_code == 204
    assert Snack.objects.filter(pk=snack.id).exists() == False


@pytest.mark.django_db
def test_user_delete_snack(user_api_client):
    snack = create_snack(name='snack1')
    url = reverse('Snacks:single_snack', kwargs={'pk': snack.id})
    respone = user_api_client.delete(url)
    assert respone.status_code == 403
    assert Snack.objects.filter(pk=snack.id).exists() == True


@pytest.mark.django_db
def test_admin_update_snack(admin_api_client):
    snack = create_snack(name='snack1')
    url = reverse('Snacks:single_snack', kwargs={'pk': snack.id})
    response = admin_api_client.patch(url, data={'name': 'snack2'})
    assert response.status_code == 200
    snack.name = 'snack2'
    assert response.data == SnackSerializer(snack).data


@pytest.mark.django_db
def test_user_update_snack(user_api_client):
    snack = create_snack(name='snack1')
    url = reverse('Snacks:single_snack', kwargs={'pk': snack.id})
    response = user_api_client.patch(url, data={'name': 'snack2'})
    assert response.status_code == 403
