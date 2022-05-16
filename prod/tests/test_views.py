from django.test import TestCase
from django.urls import reverse

from prod.models import Post, Category


class TestPostListView(TestCase):

    def test_get(self):
        category1 = Category.objects.create(title='CatOne')
        post1 = Post.objects.create(
            title='PostOne',
            content='ContentOne',
            category=category1,
            slug='postone',
        )
        post1 = Post.objects.create(
            title='PostTwo',
            content='ContentTwo',
            category=category1,
            slug='posttwo',
        )
        url = reverse('post-list')
        print(url)
        response = self.client.get(url)
        print(response)

