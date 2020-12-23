# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse , HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth import authenticate, get_user_model
from django.views.generic import ListView, DetailView, FormView, CreateView
from .forms import CommentForm
from .models import Post, Category, Comment
# Create your views here.
User = get_user_model()


class PostsArchive(ListView):
    model = Post
    queryset = Post.objects.filter(draft=False)
    ordering = ('published_at',)
    template_name = 'blog/posts.html'


# def home(request):
#     posts = Post.objects.all()
#     template = loader.get_template('blog/posts.html')
#     post_image_exist = True
#     for p in posts:
#         if not p.image:
#             post_image_exist = False
#     print(post_image_exist)
#     context = {
#         'posts':posts,
#         'post_image_exist': post_image_exist
#     }
#     return HttpResponse(template.render(context, request))

class PostSingle(DetailView, FormView, CreateView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context.get('post', None)
        context['comments'] = Comment.objects.filter(post=post)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse('post_single', kwargs={'slug': slug})

    def form_valid(self, form):
        data = self.get_form_kwargs().get('data')
        content = data.get('content', None)
        slug = self.kwargs.get('slug', None)
        author = self.request.user
        post = Post.objects.get(slug__exact=slug)
        Comment.objects.create(
            post=post,
            author=author,
            content=content,
            is_confirmed=True
        )
        return HttpResponseRedirect(self.get_success_url())


# def post_single(request, pk):
#     try:
#         post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
#     except Post.DoesNotExist:
#         return HttpResponseNotFound('Post Not Found')
#     context = {
#         'post': post,
#         'category': post.category,
#         'author': post.author,
#         'settings': post.post_setting,
#         'comments': post.comments.filter(is_confirmed=True),
#         'form': CommentForm()
#     }
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#         else:
#             context['form'] = form

#     return render(request, 'blog/post_single.html', context)


class CategoriesArchive(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'blog/categories.html'

# def categories_archive(request):
    # categories = Category.objects.all()
    # links = ''.join('<li><a href={}>{}</a></li>'.format(reverse('category_single', args=[category.slug]), category.title) for category in categories)
    # blog = "<html><head><title>Post Archive</title></head><body>{}</body></html>".format('<ul>{}</ul>'.format(links))
    # return HttpResponse(blog)



# def category_single(request, pk):
#     try:
#         category = Category.objects.get(slug=pk)
#     except Category.DoesNotExist:
#         return HttpResponseNotFound('Category not found')
#     posts = Post.objects.filter(category=category)
#     links = ''.join('<li><a href={}>{}</a></li>'.format(reverse('post_single', args=[post.slug]), post.title) for post in posts)
#     blog = '<html><head><title>Post Archive</title></head><body>{}<a href={}>All Categories</a></body></html>'.format('<ul>{}</ul>'.format(links), reverse('categories_archive'))
#     return HttpResponse(blog)

class CategorySingle(DetailView):
    model = Category
    template_name = 'blog/category_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context.get('category', None)
        context['posts'] = Post.objects.filter(category=category)
        return context     