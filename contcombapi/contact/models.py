# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

from django.db import models
from managers import ContactManager
from contcombapi.user.models import User
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):

    id = models.AutoField(primary_key=True, db_column='id_contact')
    user = models.ForeignKey(User)
    message = models.TextField(_('mensagem'), blank=False)
    reply = models.TextField(_('resposta'), default='')

    objects = ContactManager()

    class Meta:
        db_table = 'contact'
        verbose_name = _(u'Mensagem')
        verbose_name_plural = _(u'Mensagens')

    def __unicode__(self):
        return self.message
