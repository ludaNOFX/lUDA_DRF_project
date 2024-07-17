from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils import timezone

User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='password123',
            date_birth=timezone.make_aware(timezone.datetime(1990, 1, 1))
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='password123',
            date_birth=timezone.make_aware(timezone.datetime(1992, 2, 2))
        )

    def test_user_creation(self) -> None:
        self.assertEqual(self.user1.username, 'testuser1')
        self.assertEqual(self.user1.email, 'testuser1@example.com')
        self.assertEqual(self.user1.date_birth.strftime('%Y-%m-%d'), '1990-01-01')
        self.assertEqual(self.user1.slug, slugify('testuser1'))

    def test_user_str(self) -> None:
        self.assertEqual(str(self.user1), 'testuser1')

    def test_follow(self) -> None:
        self.user1.follow(self.user2)
        self.assertTrue(self.user1.is_following(self.user2))
        self.assertIn(self.user2, self.user1.followed.all())

    def test_unfollow(self) -> None:
        self.user1.follow(self.user2)
        self.user1.unfollow(self.user2)
        self.assertFalse(self.user1.is_following(self.user2))
        self.assertNotIn(self.user2, self.user1.followed.all())

    def test_is_following(self) -> None:
        self.assertFalse(self.user1.is_following(self.user2))
        self.user1.follow(self.user2)
        self.assertTrue(self.user1.is_following(self.user2))




