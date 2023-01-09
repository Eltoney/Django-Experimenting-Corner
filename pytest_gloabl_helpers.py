import pytest 
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


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
