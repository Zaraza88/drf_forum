from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase


from prod.models import Post, Category, User
from prod.serializers import PostSerializers


class PostListTest(APITestCase):

    def setUp(self):
        category1 = Category.objects.create(title='CatOne')
        user = User.objects.create(username='User')
        self.post1 = Post.objects.create(
            title='Post',
            author=user,
            content='Content',
            category=category1,
            slug='post',
        )
        category2 = Category.objects.create(title='CatTne')
        user = User.objects.create(username='UserTwo')
        self.post2 = Post.objects.create(
            title='Post2',
            author=user,
            content='Content',
            category=category2,
            slug='post2',
        )

    def test_get(self):
        url = reverse('post_list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_data = PostSerializers([self.post1, self.post2], many=True)
        self.assertEqual(serializer_data.data, response.data)

    def test_get_search(self):
        url = reverse('post_list')
        response = self.client.get(url, data={'title': 'Post'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_data = PostSerializers([self.post1, self.post2], many=True)
        self.assertEqual(serializer_data.data, response.data)

    # def test_get_filter(self):
    #     url = reverse('post_list')
    #     response = self.client.get(url, data={
    #         'author': str(self.post1.author).lower()})
    #     self.assertEqual(status.HTTP_200_OK, response.status_code)
    #     serializer_data = PostSerializers([self.post1, self.post2], many=True)
    #     self.assertEqual(serializer_data.data, response.data)
    #     print(response)


class PostDetailTest(APITestCase):

    def setUp(self):
        category1 = Category.objects.create(title='CatOne')
        user = User.objects.create(username='User')
        self.post = Post.objects.create(
            title='Post',
            author=user,
            content='Content',
            category=category1,
            slug='post',
        )

    def test_get(self):
        url = reverse('post_detail', kwargs={'slug': self.post.slug})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # serializer_data = PostSerializers([self.post1, self.post2], many=True)
        # self.assertEqual(serializer_data.data, response.data)