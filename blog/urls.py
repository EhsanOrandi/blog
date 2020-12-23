from django.urls import path
from .views import PostsArchive, PostSingle, CategoriesArchive, CategorySingle

urlpatterns = [
    path('posts/', PostsArchive.as_view(), name="post_archive"),
    path('posts/<slug:slug>/', PostSingle.as_view(), name='post_single'),
    path('categories/', CategoriesArchive.as_view() , name="categories_archive"),
    path('categories/<slug:slug>', CategorySingle.as_view(), name='category_single'),
]