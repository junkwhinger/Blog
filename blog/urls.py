from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index_blog, name='index'),
    url(r'^list/$', views.list_posts, name='list'),
    url(r'^list/(?P<pk>[0-9]+)/$', views.view_post, name='view'),
    url(r'^update/$', views.update_post, name='create'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.update_post, name='update'),
    url(r'^delete/post/$', views.delete_post, name='delete_post'),
    url(r'^delete/comment/$', views.delete_comment, name='delete_comment'),
]
