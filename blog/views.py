from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404

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
    per_page = 5
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

    after_del = request.GET.get('after_del', False)

    return render(
        request,
        'list.html',
        {'page_info': paginator_info, 'after_del':after_del, }
    )


def view_post(request, pk):
    # URI: /blog/list/pk
    # GET: 1개의 Post 내용 출력, POST: 1개 Post 아래 댓글을 저장하고 다시 1개 Post 내용으로 Redirect
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'GET':
        return render(request, 'view.html', {'post': post, })
    elif request.method == 'POST':
        comment_writer = request.POST.get('comment_writer')
        comment_content = request.POST.get('comment_content')

        # comment_writer, comment_content 중 빈 값이 있다면 등록하지 않는다.
        if comment_writer and comment_content:
            comment = Comment(
                writer=comment_writer,
                content=comment_content,
                post=post
            )
            comment.save()

        return redirect(reverse('blog:view', kwargs={'pk': post.pk, }))


def update_post(request, pk=None):
    # URI: /blog/update
    # GET: 글 등록/수정하는 페이지, pk 여부에 따라 등록인지 수정인지 판단한다.
    # POST: 글 등록/수정한 데이터 처리하는 페이지, pk 여부에 따라 등록인지 수정인지 판단한다.
    if request.method == 'GET':
        categories = Category.objects.all()

        if pk:
            post = Post.objects.get(pk=pk)
            return render(
                request,
                'update.html',
                {'categories': categories, 'post': post, }
            )
        else:
            return render(
                request,
                'update.html',
                {'categories': categories, }
            )
    elif request.method == 'POST':
        # 필수 데이터들의 유효성을 확인한다. 오류가 발생하면 404 페이지로 redirect 한다.
        try:
            title = request.POST.get('post_title')
            category = Category.objects.get(
                pk=int(request.POST.get('post_category'))
            )
            writer = request.POST.get('post_writer')
            content = request.POST.get('post_content')
        except:
            raise Http404('Necessary info to upload post is insufficient.')

        # title, category, writer, content 중 하나라도 없다면 등록하지 않고 리스트 화면으로 간다.
        if title and category and writer and content:
            tags = list(
                map(str.strip, request.POST.get('post_tags', '').split(','))
            )

            # pk 가 있다면 기존 post 에서 불러오고, 없다면 방금 입력된 내용으로 post 를 만든다.
            if pk:
                post = Post.objects.get(pk=pk)

                for post_tag in post.tags.all():
                    post.tags.remove(post_tag)

                post.title, post.category = title, category
                post.writer, post.content = writer, content
            else:
                post = Post(
                    title=title,
                    category=category,
                    writer=writer,
                    content=content
                )

            post.save()

            # tag 를 만들고, post 에 연결한다.
            for tag_name in tags:
                if not Tag.objects.filter(name=tag_name).exists():
                    tag = Tag(name=tag_name)
                    tag.save()
                else:
                    tag = Tag.objects.filter(name=tag_name).first()

                post.tags.add(tag)

            return redirect(reverse('blog:view', kwargs={'pk': post.pk, }))
        else:
            return redirect(reverse('blog:list'))


def delete_post(request):
    # URI: /blog/delete/post
    # 1개 Post 삭제하고 리스트 화면으로 Redirect
    pk = request.GET.get('pk', None)

    if pk:
        post = Post.objects.get(pk=pk)
        post.delete()

    return redirect(reverse('blog:list')+'?after_del=True')


def delete_comment(request):
    # URI: /blog/delete/comment
    # 1개 Comment 삭제하고 Post 조회 화면으로 Redirect
    pk = request.GET.get('pk', None)
    post_pk = None

    if pk:
        comment = Comment.objects.get(pk=pk)
        post_pk = comment.post.pk
        comment.delete()

    return redirect(reverse('blog:view', kwargs={'pk': post_pk, }))
