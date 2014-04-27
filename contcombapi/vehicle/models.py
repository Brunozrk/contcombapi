# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _
from contcombapi.user.models import User
from contcombapi.vehicle.managers import VehicleManager


class Mark(models.Model):

    id = models.AutoField(primary_key=True,)
    name = models.CharField(_('nome'), max_length=100, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'mark'
        verbose_name = _(u'Marca')
        verbose_name_plural = _(u'Marcas')


class Model(models.Model):

    id = models.AutoField(primary_key=True,)
    name = models.CharField(_('nome'), max_length=100, blank=False)
    mark = models.ForeignKey('Mark', null=True, on_delete=models.CASCADE)
    valid = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'model'
        verbose_name = _(u'Modelo')
        verbose_name_plural = _(u'Modelos')


class Vehicle(models.Model):

    id = models.AutoField(primary_key=True,)
    motor = models.CharField(_(u'motor'), blank=False, max_length=10)
    manufactured = models.IntegerField(_(u'ano de fabricação'), blank=False, max_length=4)
    model = models.ForeignKey('Model', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = VehicleManager()

    def __unicode__(self):
        return self.model.name

    class Meta:
        db_table = 'vehicle'
        verbose_name = _(u'Veículo')
        verbose_name_plural = _(u'Veículos')
