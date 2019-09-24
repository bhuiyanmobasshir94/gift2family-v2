from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone
from oscar.apps.customer.abstract_models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

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
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()


class AgentProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_('Agent Full Name'), max_length=40,
                            blank=False, help_text=_("Full name as in Passport"))
    email = models.EmailField(_('Agent Email Address'), blank=False,
                              unique=True, help_text=_("Active email address"))
    phone_number = PhoneNumberField(_("Agent Phone Number"), blank=False, help_text=_("Active phone number"))
    nationality = models.CharField(
        _("Agent Nationality"), max_length=30, blank=False, help_text=_("As described in passport"))
    country = models.ForeignKey('address.Country', on_delete=models.CASCADE, verbose_name=_("Agent Present Country"))
    passport_copy = models.FileField(upload_to='agents/passport/%Y/%m/%d/', blank=False,
                                     null=False, verbose_name=_("Agent Passport Copy"), help_text=_("Scanned document"))
    date_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Agent Created"))

    class Meta:
        verbose_name = _('Agent')
        verbose_name_plural = _('Agents')
    
    def __str__(self):
        return self.name
    
class AgentInterestRate(models.Model):
    name = models.CharField(
        _("Interest Rate Name"), max_length=30, blank=False, default="", editable=True)
    interest_rate = models.FloatField(default=0.0)
    class Meta:
        verbose_name = _('Agent interest rate')
        verbose_name_plural = _('Agents interest rate')
    
    def __str__(self):
        return str(self.name)
