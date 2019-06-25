from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .forms import UserCreationForm, CompanyForm, AccountEntryForm, RateForm

from .models import (
    # Profile,
    # Tenant,
    Company,
    Service,
    AccountEntry,
    Rate,
)


# def get_unique_tenant():
#     count = Tenant.objects.all().count()
#     if count == 1:
#         return dict(tenant=[Tenant.objects.all().first().pk])
#     return {}


# class ProfileInline(admin.TabularInline):
#     model = Profile
#     can_delete = False

# prepopulated_fields = get_unique_tenant()


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', ),
        }),
    )

    # inlines = [
    #     ProfileInline,  # adds the inline profile to user forms
    # ]
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_active')

# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
    # add_form = UserCreationForm


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


class AdminCompany(AdminAuthSignature):
    list_display = ('code', 'razon_social', 'balance',
                    'created_by', 'created_on', 'modified_by', 'modified_on')
    readonly_fields = ('balance',)
    form = CompanyForm

    def has_add_permission(self, request, obj=None):
        return False if Company.objects.all().count() > 0 else True

    def has_delete_permission(self, request, obj=None):
        return False


# class AdminTag(AdminAuthSignature):
#     list_display = ('tag', 'slug', 'created_by', 'created_on')


class AdminService(AdminAuthSignature):
    pass


class AdminAccountEntry(AdminAuthSignature):
    list_display = ('entry_type', 'amount',
                    'reference', 'created_on', 'created_by')
    form = AccountEntryForm
    admin_fields = ('entry_type',
                    'amount', 'reference')

    fieldsets = (
        (None, {'fields': admin_fields}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': admin_fields,
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ('amount', 'entry_type')
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.entry_type == obj.CHARGE:
                return False
        return True

    def has_add_permission(self, request, obj=None):
        if not Company.get():
            return False
        if obj:
            if obj.entry_type == obj.CHARGE:
                return False
        return True
    # def get_fieldsets(self, request, obj=None):
    #     if obj:
    #         return self.fieldsets
    #     return self.add_fieldsets


class AdminRate(AdminAuthSignature):
    form = RateForm
    list_display = ('service', 'unit_price', 'is_active',
                    'valid_from', 'valid_until', 'created_by', 'created_on')


# register custom user model
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# admin.site.register(Profile)
admin.site.register(Company, AdminCompany)
admin.site.register(Service, AdminService)
admin.site.register(AccountEntry, AdminAccountEntry)
admin.site.register(Rate, AdminRate)
# admin.site.register(Tag, AdminTag)
