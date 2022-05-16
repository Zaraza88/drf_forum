from datetime import datetime
from django.test import TestCase

from prod.serializers import PostSerializers, CommentCreateSerializers
from prod.models import Category, User, Post, Comment


class PostSerializersTestCase(TestCase):
    """Тест PostSerializers на корректный вывод данных"""

    def setUp(self):
        category1 = Category.objects.create(title='CatOne')
        user = User.objects.create(username='User')
        self.post1 = Post.objects.create(
            author=user,
            title='Post',
            content='Content',
            category=category1,
        )
        category2 = Category.objects.create(title='CatTne')
        user = User.objects.create(username='UserTwo')
        self.post2 = Post.objects.create(
            author=user,
            title='Post2',
            content='Content',
            category=category2,
        )

    def test_ok(self):
        data = PostSerializers([self.post1, self.post2], many=True)
        expected_data = [
            {   
                'id': self.post1.id,
                'author': 'User',
                'title': 'Post',
                'content': 'Content',
                'category': 1,
            },
            {
                'id': self.post2.id,
                'author': 'UserTwo',
                'title': 'Post2',
                'content': 'Content',
                'category': 2,
            }
        ]
        self.assertEqual(expected_data, data.data)


class CommentCreateSerializersTestCase(TestCase):
    """Тест CommentCreateSerializers на корректный вывод данных"""

    def setUp(self):
        category1 = Category.objects.create(title='CatOne')
        user = User.objects.create(username='user', email='user@mail.com')
        user2 = User.objects.create(username='user2', email='user2@mail.com')

        self.post1 = Post.objects.create(
            author=user,
            title='Post',
            content='Content',
            category=category1,
        )

        self.comment = Comment.objects.create(
            name=user.username,
            email=user.email,
            post=self.post1,
            text='Комментарий'
        )
        self.comment2 = Comment.objects.create(
            name=user2.username,
            email=user2.email,
            post=self.post1,
            text='Комментарий'
        )

    def test_ok(self):
        data = CommentCreateSerializers(
            [self.comment, self.comment2], many=True
        )
        expected_data = [
            {
                "id": 12,
                "name": "admin",
                "email": "admin@admin.com",
                "text": "Комментарий",
                # "date": "2022-05-16T12:41:37.303185Z",
                "post": 1
            },
            {
                "id": 11,
                "name": "admin",
                "email": "admin@admin.com",
                "text": "Комментарий",
                # "date": "2022-05-15T16:27:13.549758Z",
                # "parent": null,
                "post": 1
            },
        ]
        self.assertEqual(expected_data, data.data)
