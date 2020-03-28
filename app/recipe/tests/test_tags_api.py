from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the public tags api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that the user needs to log in"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the auth tags api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@test.com', password='testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Vegetarian')
        Tag.objects.create(user=self.user, name='Normal people')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the auth user"""
        user_local = get_user_model().objects.create_user(
            email='test2@test.com',  password='testpass'
        )
        tag = Tag.objects.create(user=self.user, name='Vegan')

        Tag.objects.create(user=user_local, name='Local')
        Tag.objects.create(user=user_local, name='Local')
        Tag.objects.create(user=user_local, name='local people')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        self.assertEqual(res.data[0]['name'], tag.name)
