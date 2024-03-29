from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Category {}: {}'.format(self.pk, self.name)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # writer = models.CharField(max_length=50)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField('Tag', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Post {}: {}'.format(self.pk, self.title)


class Comment(models.Model):
    content = models.TextField(max_length=200)
    # writer = models.CharField(max_length=50)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    post = models.ForeignKey(Post, null=True, blank=True)
    parent_comment = models.ForeignKey('Comment', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment {}: {}'.format(self.pk, self.content[:30])


class Tag(models.Model):
    name = models.CharField(max_length=30, db_index=True, unique=True)

    def __str__(self):
        return 'Tag {}: {}'.format(self.pk, self.name)
