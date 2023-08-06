from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from gas.sites import site


class BaseFilterForm(forms.Form):
    """
        Form for content filtering.

        The `filter` method must be replaced.
    """
    def filter(self, qs):
        """
            This function takes a queryset and returns another queryset, with
            the content filtered with the data in the form.
        """
        return qs


class UserForm(forms.ModelForm):
    roles = forms.MultipleChoiceField(
        choices=site.role_choices,
        label=_('roles'),
        required=False,
    )
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'email', 'is_active',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'roles' not in self.initial and self.instance.pk is not None:
            self.initial['roles'] = self.instance.user_roles.values_list('role', flat=True)

    def save(self, commit=True):
        obj = super().save(commit=False)

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            roles = self.cleaned_data['roles']
            for role in roles:
                obj.user_roles.update_or_create(role=role)
            obj.user_roles.exclude(role__in=roles).delete()

        self.save_m2m = save_m2m

        if commit:
            obj.save()
            self.save_m2m()

        return obj
