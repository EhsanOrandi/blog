from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from blog.models import Comment


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"), required=True, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control my- 2'}))
    password = forms.CharField(label=_("Password"), required=True, widget=forms.PasswordInput(attrs={'class': 'form-control my- 2'})) 

class UserRegisterationForm(forms.ModelForm):
    password2 = forms.CharField(label=_('Repeat password'), required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'})
        }

    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise ValidationError(_("Password and its confirmation don't match"), code='invalid')
        return password2


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control', 'style': 'resize:none;',
                                                    'rows': '8',
                                                    'placeholder': 'Enter your comment here ... '})}


