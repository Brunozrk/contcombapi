from django.contrib import admin
from contcombapi.contact.models import Contact
from django.utils.translation import ugettext as _


class ContactAdmin(admin.ModelAdmin):

    list_display = ('user', 'message', 'reply', 'answered')
    search_fields = ('user__name', 'message', 'reply')
    readonly_fields = ('message', 'user')

    def has_add_permission(self, request):
            return False

    def answered(self, obj):
        return obj.reply != ''

    answered.short_description = _(u'Respondido?')
    answered.boolean = True

admin.site.register(Contact, ContactAdmin)
