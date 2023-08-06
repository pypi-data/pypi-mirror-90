import datetime
import pytz
import uuid
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from django.conf import settings
import secrets
import string
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import check_password, make_password

class TimeStampBase(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

class RSSFeedUrl(TimeStampBase):
    title = models.CharField(max_length=32)
    url = models.URLField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = _('RSS feed URL')
        verbose_name_plural = _('RSS feed URLs ')


class HazardLevels(models.Model):
    title = models.CharField(max_length=32)
    danger_level = models.IntegerField(validators=[MaxValueValidator(10)])
    color_code = models.CharField(max_length=6, null=True)
    description = models.TextField()

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = _('Hazard Level')
        verbose_name_plural = _('Hazard Levels')

class HazardFeeds(TimeStampBase):
    id = models.BigIntegerField(primary_key=True)
    date = models.DateTimeField()
    title = models.CharField(max_length=128)
    external_link = models.URLField()
    summary = models.TextField()
    hazard_level = models.ForeignKey(HazardLevels, on_delete=models.CASCADE)
    is_sent = models.BooleanField(default=False)
    date_send = models.DateTimeField(null=True)
    date_start = models.DateField(null=True)
    date_end = models.DateField(null=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = _('Hazard Feed')
        verbose_name_plural = _('Hazard Feeds')

    def resency(self):
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        return now-self.date

    def is_newer_that(self, timedelta):
        return self.date_created-self.date < timedelta

    def date_send_set(self):
        self.date_send = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    @classmethod
    def not_sent(cls):
        return cls.objects.filter(is_sent=False)

def gen_act_code():
    lenth = settings.ACTIVATION_CODE_LENTH
    code = ''.join(secrets.choice(string.digits)
                   for i in range(lenth))

    return code


class ActivationCodeBaseModel(models.Model):
    """
     inherit this class to activate your model objects from sending activation codes
     activated object must have is_active field with Type models.Booleanfield
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    code = models.CharField(editable=False,  default=gen_act_code, max_length=256)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def _is_expired(self):
        expiration = settings.CODE_EXPIRATION_TIME
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        exp = now-datetime.timedelta(seconds=expiration)
        if exp > self.date_created:
            return True
        else:
            return False

    @property
    def date_expiration(self):
        return (self.date_created + datetime.timedelta(seconds=settings.CODE_EXPIRATION_TIME)).replace(tzinfo=pytz.utc)

    def is_valid(self, code):
        if not self._is_expired():
            return code == self.code
        return False

    class Meta:
        abstract = True



class EmailActivationCode(ActivationCodeBaseModel):
    pass

class WeatherRecipients(models.Model):
    email = models.EmailField(unique=True)
    title = models.CharField(max_length=64, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_active = models.BooleanField(default=False)
    hazard_levels = models.ManyToManyField(HazardLevels, blank=True)
    code = models.OneToOneField(EmailActivationCode,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True
                                )

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = _('Weather hazard recipient')
        verbose_name_plural = _('Weather hazard recipients')

class EmailTemplates(models.Model):
    title = models.CharField(max_length=64, editable=False, unique=True)
    template = HTMLField(null=True)

    def __str__(self):
        return '%s' % self.title

    class Meta:
        verbose_name = _('Email Template')
        verbose_name_plural = _('Email Templates')


class WeatherRecipientsEditCandidate(models.Model):
    title = models.CharField(max_length=64, null=True)
    valid = models.BooleanField(default=False)
    hazard_levels = models.ManyToManyField(HazardLevels, blank=True)
    target = models.OneToOneField(WeatherRecipients,
                                  on_delete=models.CASCADE,
                                  primary_key=True
                                  )