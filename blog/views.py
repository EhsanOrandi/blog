# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse , HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, UserRegisterationForm, CommentForm
from .models import Post, Category

# Create your views here.

def home(request):
    posts = Post.objects.all()
    template = loader.get_template('blog/posts.html')
    context = {
        'posts':posts
    }
    return HttpResponse(template.render(context, request))


def post_single(request, pk):
    try:
        post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
    except Post.DoesNotExist:
        return HttpResponseNotFound('Post Not Found')
    context = {
        'post': post,
        'category': post.category,
        'author': post.author,
        'settings': post.post_setting,
        'comments': post.comments.filter(is_confirmed=True),
        'form': CommentForm()
    }
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        else:
            context['form'] = form

    return render(request, 'blog/post_single.html', context)


def categories_archive(request):
    categories = Category.objects.all()
    links = ''.join('<li><a href={}>{}</a></li>'.format(reverse('category_single', args=[category.slug]), category.title) for category in categories)
    blog = "<html><head><title>Post Archive</title></head><body>{}</body></html>".format('<ul>{}</ul>'.format(links))
    return HttpResponse(blog)



def category_single(request, pk):
    try:
        category = Category.objects.get(slug=pk)
    except Category.DoesNotExist:
        return HttpResponseNotFound('Category not found')
    posts = Post.objects.filter(category=category)
    links = ''.join('<li><a href={}>{}</a></li>'.format(reverse('post_single', args=[post.slug]), post.title) for post in posts)
    blog = '<html><head><title>Post Archive</title></head><body>{}<a href={}>All Categories</a></body></html>'.format('<ul>{}</ul>'.format(links), reverse('categories_archive'))
    return HttpResponse(blog)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('post_archive')
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('post_archive')

    context = {
        'form': form,
    }
    return render(request, 'blog/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('post_archive')


def register_view(request):
    # if request.method == 'POST':
    #     form = UserRegisterationForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         email = form.cleaned_data['email']
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
    #         user.set_password(password)
    #         user.save()
    #         return redirect('login')
    #     else:
    #         pass
    #     context = {'form': form}
    # else:
    #     form = UserRegisterationForm()
    #     context = {'form': form}
    # return render(request, 'blog/register.html', context=context)
    # context = {
    #     'form': UserRegisterationForm()
    # }
    # return render(request, 'blog/register.html', context=context)


    if request.method == 'GET':
        form = UserRegisterationForm()
    else:
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            form.save()
            return redirect('post_archive')

    context = {
        'form': form,
    }
    return render(request, 'blog/register.html', context=context)