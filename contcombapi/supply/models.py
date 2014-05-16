# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''
from contcombapi.supply.managers import SupplyManager, FuelManager
from contcombapi.vehicle.models import Vehicle
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Fuel(models.Model):

    id = models.AutoField(primary_key=True,)
    name = models.CharField(_('nome'), max_length=100, blank=False)

    objects = FuelManager()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'fuel'
        verbose_name = _(u'Combustível')
        verbose_name_plural = _(u'Combustíveis')

class Supply(models.Model):
    
    id = models.AutoField(primary_key=True,)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    odometer = models.FloatField(_('odômetro'), blank=False)
    is_full = models.BooleanField(_('cheio'), blank=False, default=True)
    date = models.DateField(_('data'), blank=False)
    liters = models.FloatField(_('litros'), blank=False)

    station = models.CharField(_('posto'), max_length=100, blank=False)
    fuel = models.ForeignKey(Fuel, null=False)
    total_spending = models.FloatField(_('total gasto'), blank=False)
    fuel_price = models.FloatField(_('preço do combustível'), blank=False)
    obs = models.TextField(_('observação'), blank=True)
    
    objects = SupplyManager()

    def __unicode__(self):
        return self.obs

    class Meta:
        db_table = 'supply'
        verbose_name = _(u'Abastecimento')
        verbose_name_plural = _(u'Abastecimentos')
    
