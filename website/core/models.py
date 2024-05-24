from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='ХУЙ ЗНАЕТ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Katigori'
        verbose_name_plural = 'boom'


class Article(models.Model):
    name = models.CharField(max_length=225, verbose_name='GLOBAL')
    short_description = models.TextField(max_length=250, verbose_name='micro text')
    full_description = models.TextField(max_length=250, verbose_name='full text')
    preview = models.ImageField(upload_to='articles/', verbose_name='Photo', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0, verbose_name='Время')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Integer')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='MY WORK')

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'article_id': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья',
                                related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(verbose_name='Комментарий')


    def __str__(self):
        return f'{self.author}: {self.article}'

    class Meta:
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'


class ArticleViewsCount(models.Model):
    session_id = models.CharField(max_length=255)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class BaseVote(models.Model):
    user = models.ManyToManyField(User)
    article = models.OneToOneField(Article, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True


class Like(models.Model):
    user = models.ManyToManyField(User)
    article = models.OneToOneField(Article, related_name='likes', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.OneToOneField(Comment, related_name='likes', on_delete=models.CASCADE, blank=True, null=True)


class Dislike(models.Model):
    user = models.ManyToManyField(User)
    article = models.OneToOneField(Article, related_name='dislikes', on_delete=models.CASCADE, blank=True, null=True)
    comment = models.OneToOneField(Comment, related_name='dislikes', on_delete=models.CASCADE, blank=True, null=True)
