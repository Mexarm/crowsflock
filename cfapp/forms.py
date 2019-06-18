from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django import forms

from .models import Tenant, Service, AccountEntry


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ('tenant', 'description', 'balance', 'max_credit', 'services')
        readonly = ('balance',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['services'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields['services'].help_text = ''
        self.fields['services'].queryset = Service.objects.all()


class AccountEntryForm(forms.ModelForm):
    class Meta:
        model = AccountEntry
        fields = ('tenant', 'entry_type', 'amount', 'reference')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        entry_type = self.fields.get('entry_type')
        if entry_type:
            entry_type.choices = (
                (AccountEntry.PAYMENT, 'Payment'), )


class RateForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        tenant_name = self.cleaned_data.get('tenant')

        service_name = self.cleaned_data.get('service')

        tenant = Tenant.objects.get(tenant=tenant_name)
        service = Service.objects.get(name=service_name)

        if not service in tenant.services.all():
            msg = _(f'{service.name} is not active on {tenant}')
            self.add_error('service', forms.ValidationError(msg))

        valid_from = self.cleaned_data.get('valid_from')
        valid_until = self.cleaned_data.get('valid_until')

        if valid_from and valid_until:
            if valid_until < valid_from:
                msg = _(f'valid until date cannot be earlier than valid from date')
            self.add_error('valid_until', forms.ValidationError(msg))

        return cleaned_data


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(max_length=200, help_text='required')

    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        if self.Meta.model.objects.filter(email=email).exists():
            msg = _('email already exists')
            self.add_error('email', forms.ValidationError(msg))
        profile_tenant = self.data.get('profile-0-tenant')
        if not profile_tenant:
            msg = _('tenant is required')
            self.add_error(None, forms.ValidationError(msg))
        return cleaned_data

    class Meta:
        model = get_user_model()
        # this is required to avoid improperlyConfigured Error
        fields = ("username",)
        #field_classes = {'username': UsernameField}
        # fields = ('username', 'email', 'password1', 'password2')
