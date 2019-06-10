from django.contrib import admin

from .models import (
    Tenant,
    Profile,
    Tag,
)
# Register your models here.


class AdminAuthSignature(admin.ModelAdmin):
    """Abstract class that overrides save_model'
       and updates the model with the user that created or
       modified the model instance"""

    exclude = ('created_by', 'modified_by')

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    class Meta:
        abstract = True


class TenantAdmin(AdminAuthSignature):
    list_display = ('tenant', 'description', 'created_by', 'modified_by')


class AdminTag(AdminAuthSignature):
    list_display = ('tenant', 'tag')


admin.site.register(Tenant, TenantAdmin)
admin.site.register(Profile)
admin.site.register(Tag, AdminTag)
