from django.contrib import admin

from .models import GroupMapping


class GroupMappingAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff

    def has_module_permission(self, request):
        return request.user.is_staff

    list_display = ('django_group', 'ldap_group_name')


admin.site.register(GroupMapping, GroupMappingAdmin)
