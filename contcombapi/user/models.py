# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.conf import settings
from django.db import models
from managers import UserManager
import base64
import datetime
import time
from django.utils.translation import ugettext_lazy as _


class User(models.Model):

    id = models.AutoField(primary_key=True, db_column='id_user')
    username = models.CharField(_('usuário'), max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=100, blank=False)
    email = models.EmailField(_('email'), max_length=100, blank=False)
    name = models.CharField(_('nome'), max_length=100, blank=False)
    token = models.CharField(max_length=100)

    objects = UserManager()

    DELIMITER_TOKEN = "?"

    class Meta:
        db_table = 'user'
        managed = True
        verbose_name = _(u'Usuário')
        verbose_name_plural = _(u'Usuários')

    def __unicode__(self):
        return '%s' % self.username

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.username)

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def has_token(self):
        if self.token:
            return True
        else:
            return False

    def is_valid_token(self):
        token_base64 = base64.b64decode(self.token)
        token_vector = token_base64.split("?")

        t1 = float(token_vector[1])
        t2 = time.mktime(datetime.datetime.now().timetuple())

        if  t1 >= t2:
            return True

        else:
            return False

    def generate_token(self):
        valid_token = datetime.datetime.now() + datetime.timedelta(minutes=settings.DEFAULT_TIMEOUT)
        pre_token = "%s%s%s" % (self.username, self.DELIMITER_TOKEN, time.mktime(valid_token.timetuple()))
        self.token = base64.b64encode(pre_token)
