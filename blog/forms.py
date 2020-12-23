from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from blog.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none;',
                                                    'rows': '8',
                                                    'placeholder': 'Enter your comment here ... '})}


