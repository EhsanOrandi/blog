from django.urls import path
from .views import PostsArchive, PostSingle, CategoriesArchive, CategorySingle, likeComment, addComment
from .api import post_list, post_detail, comment_list, comment_detail

urlpatterns = [
    path('posts/', PostsArchive.as_view(), name="post_archive"),
    path('posts/<slug:slug>/', PostSingle.as_view(), name='post_single'),
    path('categories/', CategoriesArchive.as_view() , name="categories_archive"),
    path('categories/<slug:slug>', CategorySingle.as_view(), name='category_single'),
    path('likeComment/', likeComment, name='likeComment'),
    path('addComment/', addComment, name='addComment'),
    path('json/posts/', post_list, name='post_list'),
    path('json/posts/<int:pk>', post_detail, name='post_detail'),
    path('json/comments/', comment_list, name='comment_list'),
    path('json/comments/<int:pk>', comment_detail, name='comment_detail'),
]