from django.contrib import admin
from .models import Category
from .models import Post
from .models import Comment
from .models import Tag


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5


class PostAdmin(admin.ModelAdmin):
    fields = ['category', 'writer', 'title', 'content', 'tags']
    inlines = [CommentInline]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
