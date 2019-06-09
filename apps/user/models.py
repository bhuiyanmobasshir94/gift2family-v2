from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
from oscar.apps.customer.abstract_models import AbstractUser
from django.utils.translation import gettext_lazy as _

class UserManager(auth_models.BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and
        password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(
            email=email, is_staff=False, is_active=True, is_agent=False,
            is_superuser=False,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_agent = False
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractUser):

    is_agent = models.BooleanField(
        _('Agent status'), default=False,
        help_text=_('Designates whether this user should be treated as '
                    'agent. Unselect this to remove him from being agent.'))

    objects = UserManager()

    def get_full_name(self):
        full_name = '%s %s' % (self.last_name.upper(), self.first_name)
        return full_name.strip()
