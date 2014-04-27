from django.contrib import admin
from django.utils.translation import ugettext as _
from contcombapi.vehicle.models import Mark, Model, Vehicle


class MarkAdmin(admin.ModelAdmin):

    list_display = ('name', 'models')
    search_fields = ('name', 'model__name')

    def models(self, obj):
        return ', '.join(obj.model_set.all().values_list('name', flat=True))

    models.short_description = _(u'Modelos')


class ModelAdmin(admin.ModelAdmin):

    list_display = ('name', 'mark', 'valid')
    search_fields = ('name', 'mark__name')


class VehicleAdmin(admin.ModelAdmin):

    list_display = ('user', 'model', 'motor', 'manufactured', 'mark')
    search_fields = ('user__name', 'model__name', 'motor', 'manufactured', 'model__mark__name')

    def mark(self, obj):
        return obj.model.mark.name

    mark.short_description = _('Marca')

admin.site.register(Mark, MarkAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Vehicle, VehicleAdmin)
