from django.contrib import auth
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, full_name, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not full_name:
            raise ValueError('The given full_name must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, full_name, password, **extra_fields)

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, full_name, password, **extra_fields)
 


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    full_name = models.CharField(_('Full Name'), max_length=150, null=True)
    avatar = models.ImageField(_('Avatar'), upload_to = 'user/avatar', null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    objects = UserManager()

    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the user full_name.
        """
        return self.full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')