from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify


class Category(models.Model):
    title = models.CharField('Название категории', max_length=50)
    slug = models.SlugField('URL', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField('Название поста', max_length=150, db_index=True)
    content = models.TextField('Текст')
    author = models.ForeignKey(
        User, db_index=True, verbose_name='Автор поста', 
        on_delete=models.SET_NULL, null=True, related_name='my_post'
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, 
        verbose_name='Категория'
    )
    date_of_creation = models.DateTimeField('Дата создания', auto_now_add=True)
    slug = models.SlugField('URL', unique=True)
    publication_date = models.DateTimeField('Дата публикации', auto_now=True)
    is_published = models.BooleanField('Опубликованно?', default=True)
    appreciated = models.ManyToManyField(User, through='Rating')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('date_of_creation',)

    def __str__(self) -> str:
        return self.title

    def save(self,  *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    email = models.EmailField('Email')
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', 
        on_delete=models.CASCADE, blank=True, null=True, related_name='children'
    )
    post = models.ForeignKey(
        Post, verbose_name='Пост', on_delete=models.CASCADE, related_name='post_review'
    )
    date = models.DateTimeField(auto_now=True)
    name = models.ForeignKey(
        User, blank=True, null=True, 
        on_delete=models.PROTECT, verbose_name='Автор комментария',
        related_name='name'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date']

    def __str__(self) -> str:
        return f"{self.name} - {self.post}"


class Rating(models.Model):
    STAR = (
        (1, '1 звезда'),
        (2, '2 звезды'),
        (3, '3 звезды'),
        (4, '4 звезды'),
        (5, '5 звезд')
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Кто поставил рейтинг'
    )
    post_id = models.ForeignKey(
        Post, on_delete=models.CASCADE, 
        verbose_name='Какой пост оценили', related_name='post_id'
    )
    rating = models.PositiveBigIntegerField(choices=STAR)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self) -> str:
        return f"{self.user.username}"