from django.contrib import admin
from contcombapi.user.models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ('name', 'username', 'email')
    search_fields = ('name', 'username', 'email')
    exclude = ['password', 'token']

    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)
        del actions['delete_selected']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(User, UserAdmin)
