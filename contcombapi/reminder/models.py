# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _
from contcombapi.vehicle.models import Vehicle
from contcombapi.reminder.managers import ReminderManager

class Reminder(models.Model):
    
    id = models.AutoField(primary_key=True,)
    description = models.TextField(_('descrição'), blank=False)
    date = models.DateField(_('data'), blank=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    
    objects = ReminderManager()
    
    def __unicode__(self):
        return self.description

    class Meta:
        db_table = 'reminder'
        verbose_name = _(u'Lembrete')
        verbose_name_plural = _(u'Lembretes')
