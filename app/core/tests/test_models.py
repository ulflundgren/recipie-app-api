from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@test.com', password='testpass'):
    """Create simple user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email"""
        email = 'test@ulflundgren.se'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for the new user is normalized"""
        email = 'test@ULFLUNDGREN.SE'
        user = get_user_model().objects.create_user(email, '1234')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating a user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", '1234')

    def test_create_superuser(self):
        """Test create superuser"""
        user = get_user_model().objects.create_superuser(
            "uffe@ulflundgren.se", "1234"
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_with_shoesize(self):
        """Test to create a user that has shoes"""
        user = get_user_model().objects.create_user(
            "uffe@ulflundgren.se", "password")
        user.shoe_size = 37.5
        self.assertEquals(user.shoe_size, 37.5)

    def test_tag_str(self):
        """Test the tag str"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)
