import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


# @pytest.fixture
def create_user_token():
    User.objects.create_user('user', 'user@test.com', 'testuser')
    user = User.objects.get(username='user')
    token, _ = Token.objects.get_or_create(user=user)
    return token


# @pytest.fixture
def create_admin_token():
    User.objects.create_superuser('admin', 'admin@test.com', 'adminuser')
    user = User.objects.get(username='admin')
    token, _ = Token.objects.get_or_create(user=user)
    return token


@pytest.fixture
def admin_api_client():
    admin_token = create_admin_token()
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION='Token '+admin_token.key)
    return api_client


@pytest.fixture
def user_api_client():
    user_token = create_user_token()
    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION='Token '+user_token.key)
    return api_client
