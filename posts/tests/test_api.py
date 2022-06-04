import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from posts.models import Post
from posts.serializers import PostSerializer


class PostsAPITestCase(APITestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username='test_username')

        self.post_1 = Post.objects.create(author=self.user_1, content='Test content 1')
        self.post_2 = Post.objects.create(author=self.user_1, content='Test content 2 test_username')
        self.post_2.likes.add(self.user_1)

    def test_get(self):
        url = reverse('post-list')
        actual_response = self.client.get(url)
        expected_data = PostSerializer([self.post_1, self.post_2], many=True).data

        self.assertEqual(status.HTTP_200_OK, actual_response.status_code)
        self.assertEqual(expected_data, actual_response.data)

    def test_get_one(self):
        url = reverse('post-detail', args=(self.post_1.id,))
        actual_response = self.client.get(url)
        expected_data = PostSerializer(self.post_1).data

        self.assertEqual(status.HTTP_200_OK, actual_response.status_code)
        self.assertEqual(expected_data, actual_response.data)

    def test_create(self):
        self.assertEqual(2, Post.objects.all().count())

        url = reverse('post-list')
        data = {
            'content': 'Test new post content'
        }
        json_data = json.dumps(data)
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        actual_response = client.post(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, actual_response.status_code)
        self.assertEqual(3, Post.objects.all().count())

    def test_partial_update(self):
        url = reverse('post-detail', args=(self.post_1.id,))
        data = {
            'content': 'Updated test content 1'
        }
        json_data = json.dumps(data)
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        actual_response = client.patch(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, actual_response.status_code)
        self.post_1.refresh_from_db()
        self.assertEqual('Updated test content 1', self.post_1.content)

    def test_partial_update_not_author(self):
        self.user_2 = User.objects.create(username='test_username2')
        url = reverse('post-detail', args=(self.post_1.id,))
        data = {
            'content': 'Updated test content 1 by not author'
        }
        json_data = json.dumps(data)
        client = APIClient()
        client.force_authenticate(user=self.user_2)
        actual_response = client.patch(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_403_FORBIDDEN, actual_response.status_code)
        self.post_1.refresh_from_db()
        self.assertEqual('Test content 1', self.post_1.content)

    def test_partial_update_not_author_but_staff(self):
        self.user_2 = User.objects.create(username='test_username2', is_staff=True)
        url = reverse('post-detail', args=(self.post_1.id,))
        data = {
            'content': 'Updated test content 1 by staff'
        }
        json_data = json.dumps(data)
        client = APIClient()
        client.force_authenticate(user=self.user_2)
        actual_response = client.patch(url, data=json_data, content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, actual_response.status_code)
        self.post_1.refresh_from_db()
        self.assertEqual('Updated test content 1 by staff', self.post_1.content)

    def test_like(self):
        url = reverse('post-like', args=(self.post_1.id,))
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        actual_response = client.patch(url)

        self.assertEqual(status.HTTP_200_OK, actual_response.status_code)
        self.assertEqual({'likes': 1}, actual_response.data)

    def test_already_liked(self):
        url = reverse('post-like', args=(self.post_2.id,))
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        actual_response = client.patch(url)

        self.assertEqual(status.HTTP_409_CONFLICT, actual_response.status_code)
        self.assertEqual({'error': 'The post already liked'}, actual_response.data)

    def test_like_nonexistent_post(self):
        url = reverse('post-like', args=(3,))
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        actual_response = client.patch(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, actual_response.status_code)
        self.assertEqual({'error': 'The post does not exists'}, actual_response.data)

    def test_unlike(self):
        url = reverse('post-unlike', args=(self.post_2.id,))
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        actual_response = client.patch(url)

        self.assertEqual(status.HTTP_200_OK, actual_response.status_code)
        self.assertEqual({'likes': 0}, actual_response.data)

    def test_already_unliked(self):
        url = reverse('post-unlike', args=(self.post_1.id,))
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        actual_response = client.patch(url)

        self.assertEqual(status.HTTP_409_CONFLICT, actual_response.status_code)
        self.assertEqual({'error': 'The post already unliked'}, actual_response.data)

    def test_unlike_nonexistent_post(self):
        url = reverse('post-unlike', args=(3,))
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        actual_response = client.patch(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, actual_response.status_code)
        self.assertEqual({'error': 'The post does not exists'}, actual_response.data)
