import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from posts.models import Post
from posts.serializers import PostSerializer


class PostSerializerTestCase(TestCase):
    def test_ok(self):
        user_1 = User.objects.create(username='test_username_1')
        user_2 = User.objects.create(username='test_username_2')

        post_1 = Post.objects.create(author=user_1, content='Test content 1')
        post_2 = Post.objects.create(author=user_1, content='Test content 2')
        post_2.likes.add(user_2)
        post_3 = Post.objects.create(author=user_2, content='Test content 3 test_username')
        post_3.likes.add(user_2)
        post_3.likes.add(user_1)

        actual_data = PostSerializer([post_1, post_2, post_3], many=True).data
        expected_data = [
            {
                'id': post_1.id,
                'author': 'test_username_1',
                'content': 'Test content 1',
                'creation_date': post_1.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
                'likes': []
            },
            {
                'id': post_2.id,
                'author': 'test_username_1',
                'content': 'Test content 2',
                'creation_date': post_1.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
                'likes': [
                    {
                        'username': 'test_username_2'
                    }
                ]
            },
            {
                'id': post_3.id,
                'author': 'test_username_2',
                'content': 'Test content 3 test_username',
                'creation_date': post_1.creation_date.strftime("%Y-%m-%d %H:%M:%S"),
                'likes': [
                    {
                        'username': 'test_username_1',
                    },
                    {
                        'username': 'test_username_2'
                    }
                ]
            },
        ]
        self.assertEqual(expected_data, actual_data)
