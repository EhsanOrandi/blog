# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Post, Category, Comment, Post_setting, Comment_like
from .actions import make_published
# Register your models here.


class ChildrenItemInLine(admin.TabularInline):
    model = Category
    fields = ('title', 'slug')
    extra = 1
    show_change_link = True


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'parent')
    search_fields = ('slug', 'title')
    list_filter = ('parent',) # "," notation means it is a tuple
    inlines = [ChildrenItemInLine,]


class PostsettingAdmin(admin.TabularInline):
    model = Post_setting



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'author', 'category', 'created_at', 'updated_at', 'published_at', 'draft')
    search_fields = ('slug', 'title')
    list_filter = ('draft', 'author', 'category')
    date_hierarchy = 'published_at'
    inlines = [PostsettingAdmin, ]
    actions = [make_published]



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_at', 'updated_at', 'like_count', 'dislike_count')
    search_fields = ('content', )
    list_filter = ('author', 'post')
    date_hierarchy = 'created_at'



admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment_like)
# admin.site.register(Post, PostAdmin)
# admin.site.register(Comment, CommentAdmin)
