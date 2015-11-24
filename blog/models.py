from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return 'Category {}: {}'.format(self.pk, self.name)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    writer = models.CharField(max_length=50)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField('Tag', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Post {}: {}'.format(self.pk, self.title)


class Comment(models.Model):
    content = models.TextField(max_length=200)
    writer = models.CharField(max_length=50)

    post = models.ForeignKey(Post, null=True, blank=True)
    parent_comment = models.ForeignKey('Comment', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Comment {}: {}'.format(self.pk, self.content[:30])


class Tag(models.Model):
    name = models.CharField(max_length=30, db_index=True)

    def __str__(self):
        return 'Tag {}: {}'.format(self.pk, self.name)
