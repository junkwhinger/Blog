from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.urlresolvers import reverse

from .models import Category
from .models import Post
from .models import Comment
from .models import Tag


def index_blog(request):
    # URI: /blog/
    # blog 첫 화면
    return render(request, 'index.html')


def list_posts(request):
    # URI: /blog/list/
    # Post 들의 리스트 출력
    per_page = 3
    page = request.GET.get('page', 1)
    paginator = Paginator(Post.objects.all().order_by('-created_at'), per_page)

    try:
        posts_in_page = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts_in_page = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts_in_page = paginator.page(page)

    paginator_info = {
        'post_in_page': posts_in_page,
        'page_current': int(page),
        'page_range': paginator.page_range,
        'has_previous': posts_in_page.has_previous(),
        'has_next': posts_in_page.has_next(),
    }

    return render(request, 'list.html', {'page_info': paginator_info, })


def view_post(request, pk):
    # URI: /blog/list/pk
    # GET: 1개의 Post 내용 출력, POST: 1개 Post 아래 댓글을 저장하고 다시 1개 Post 내용으로 Redirect
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        return render(request, 'view.html', {'post': post, })
    elif request.method == 'POST':
        comment_writer = request.POST['comment_writer']
        comment_content = request.POST['comment_content']
        comment = Comment(writer=comment_writer, content=comment_content, post=post)
        comment.save()

        return redirect(reverse('blog:view', kwargs={'pk': post.pk, }))


def update_post(request, pk=None):
    # URI: /blog/update
    # GET: 글 등록/수정하는 페이지, pk 여부에 따라 등록인지 수정인지 판단한다.
    # POST: 글 등록/수정한 데이터 처리하는 페이지, pk 여부에 따라 등록인지 수정인지 판단한다.
    if request.method == 'GET':
        categories = Category.objects.all()

        if pk is not None:
            post = Post.objects.get(pk=pk)
            return render(request, 'update.html', {'categories': categories, 'post': post, })
        else:
            return render(request, 'update.html', {'categories': categories, })
    elif request.method == 'POST':
        if pk is None:
            title = request.POST['post_title']
            category = Category.objects.get(pk=int(request.POST['post_category']))
            writer = request.POST['post_writer']
            content = request.POST['post_content']
            tags = list(map(str.strip, request.POST['post_tags'].split(',')))

            post = Post(title=title, category=category, writer=writer, content=content)
            post.save()

            for tag_name in tags:
                tag = Tag(name=tag_name)
                tag.save()
                post.tags.add(tag)

            return redirect(reverse('blog:view', kwargs={'pk': post.pk, }))
        elif pk is not None:
            title = request.POST['post_title']
            category = Category.objects.get(pk=int(request.POST['post_category']))
            writer = request.POST['post_writer']
            content = request.POST['post_content']
            tags = list(map(str.strip, request.POST['post_tags'].split(',')))

            post = Post.objects.get(pk=pk)
            post.title = title
            post.category = category
            post.writer = writer
            post.content = content
            post.save()

            for post_tag in post.tags.all():
                post.tags.remove(post_tag)

            for tag_name in tags:
                tag = Tag(name=tag_name)
                tag.save()
                post.tags.add(tag)

            return redirect(reverse('blog:view', kwargs={'pk': post.pk, }))
    else:
        pass


def delete_post(request):
    # URI: /blog/delete/post
    # 1개 Post 삭제하고 리스트 화면으로 Redirect
    pk = request.GET.get('pk', None)

    if pk is not None:
        post = Post.objects.get(pk=pk)
        post.delete()

    return redirect(reverse('blog:list'))


def delete_comment(request):
    # URI: /blog/delete/comment
    # 1개 Comment 삭제하고 Post 조회 화면으로 Redirect
    pk = request.GET.get('pk', None)
    post_pk = None

    if pk is not None:
        comment = Comment.objects.get(pk=pk)
        post_pk = comment.post.pk
        comment.delete()

    return redirect(reverse('blog:view', kwargs={'pk': post_pk, }))
