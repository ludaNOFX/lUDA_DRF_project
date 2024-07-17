from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from accounts.serializers.users import UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            date_birth=timezone.make_aware(timezone.datetime(1990, 1, 1))
        )
        self.factory = APIRequestFactory()

    def test_user_serializer_fields(self):
        request = self.factory.get('/api/v1/accounts/')
        serializer_context = {'request': request}
        serializer = UserSerializer(instance=self.user, context=serializer_context)
        data = serializer.data

        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertEqual(data['date_birth'], '1990-01-01T00:00:00+03:00')
        self.assertEqual(data['products_url'], f'http://testserver/api/v1/accounts/{self.user.pk}/products')
        self.assertEqual(data['followers'], f'http://testserver/api/v1/accounts/{self.user.pk}/followers')
        self.assertEqual(data['following'], f'http://testserver/api/v1/accounts/{self.user.pk}/following')
        self.assertEqual(data['following_users_products'],
                         f'http://testserver/api/v1/accounts/{self.user.pk}/following_users_products')

    def test_get_products_url(self):
        request = self.factory.get('/api/v1/accounts/')
        serializer_context = {'request': request}
        serializer = UserSerializer(instance=self.user, context=serializer_context)

        self.assertEqual(
            serializer.get_products_url(self.user),
            f'http://testserver/api/v1/accounts/{self.user.pk}/products'
        )

    def test_get_followers(self):
        request = self.factory.get('/api/v1/accounts/')
        serializer_context = {'request': request}
        serializer = UserSerializer(instance=self.user, context=serializer_context)

        self.assertEqual(
            serializer.get_followers(self.user),
            f'http://testserver/api/v1/accounts/{self.user.pk}/followers'
        )

    def test_get_following(self):
        request = self.factory.get('/api/v1/accounts/')
        serializer_context = {'request': request}
        serializer = UserSerializer(instance=self.user, context=serializer_context)

        self.assertEqual(
            serializer.get_following(self.user),
            f'http://testserver/api/v1/accounts/{self.user.pk}/following'
        )

    def test_get_following_users_products(self):
        request = self.factory.get('/api/v1/accounts/')
        serializer_context = {'request': request}
        serializer = UserSerializer(instance=self.user, context=serializer_context)

        self.assertEqual(
            serializer.get_following_users_products(self.user),
            f'http://testserver/api/v1/accounts/{self.user.pk}/following_users_products'
        )
