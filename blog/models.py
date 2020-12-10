# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _     # for making app multilingual
from django.contrib.auth.models import User     # Django user model
from django.db import models

# Create your models here.
class Category (models.Model) :
    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    parent = models.ForeignKey('self', verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True, related_name='children', related_query_name='children')
    

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


class Post (models.Model) :
    title = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    published_at = models.DateTimeField(_("Published at"), db_index=True)
    draft = models.BooleanField(_("Draft"), default=True, db_index=True)
    image = models.ImageField(_("Image"), upload_to = 'post/images', null=True, blank=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), related_name='posts', related_query_name='posts', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_("Category"), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title


class Post_like (models.Model) :
    status = models.BooleanField(_("Status"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_("Post"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Post_like")
        verbose_name_plural = _("Post_likes")

    def __str__(self):
        return self.status


class Post_setting (models.Model) :
    allow_discussion = models.BooleanField(_("Discussion"))
    show_author_name = models.BooleanField(_("Author name"))
    show_created_at = models.BooleanField(_("Show Create Date"))
    post = models.OneToOneField('Post', verbose_name=_("Post"), related_name='post_setting', related_query_name='post_setting', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Post_setting")
        verbose_name_plural = _("Post_settings")


class Comment_like (models.Model) :
    status = models.BooleanField(_("Status"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', verbose_name=_("Comment"), on_delete=models.CASCADE)

    class Meta:
        unique_together = [['author', 'comment']]
        verbose_name = _("Comment_like")
        verbose_name_plural = _("Comment_likes")

    def __str__(self):
        return str(self.status)



class Comment (models.Model) :
    content = models.TextField(_("Content"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name=_("Post"), related_name='comments', related_query_name='comments', on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(_("confirm"), default=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.content

    @property
    def like_count(self):
        return Comment_like.objects.filter(comment=self, status=True).count()

    @property
    def dislike_count(self):
        return Comment_like.objects.filter(comment=self, status=False).count()




