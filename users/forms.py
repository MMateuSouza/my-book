from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from users.models import User


class UserForm(ModelForm):
    error_messages = {
        'password_mismatch': _('As senhas fornecidas não coincidem.'),
    }

    password1 = forms.CharField(
        label=_("Senha"),
        strip=False,
        required=False,
    )

    password2 = forms.CharField(
        label=_("Confirmação da senha"),
        strip=False,
        required=False,
    )

    group = forms.IntegerField(
        required=True,
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'is_active', 'group']

        error_messages = {
            'first_name': {
                'required': 'Nome é um campo obrigatório'
            },
            'last_name': {
                'required': 'Sobrenome é um campo obrigatório'
            },
            'username': {
                'required': 'Usuário é um campo obrigatório'
            },
            'email': {
                'required': 'E-mail é um campo obrigatório'
            },
        }

        labels = {
            'first_name': _('Nome'),
            'last_name': _('Sobrenome'),
            'username': _('Usuário'),
            'email': _('E-mail'),
            'is_active': _('Status do Usuário'),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'is_active' and field != 'password1' and field != 'password2':
                self.fields[field].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_group(self):
        group_id = self.cleaned_data.get("group")
        group = None

        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
            except Group.DoesNotExist:
                raise Group.DoesNotExist

        return group

    def _post_clean(self):
        super()._post_clean()

        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self):
        super().save()

        group = self.cleaned_data.get('group')
        groups = self.instance.groups.all()

        if not groups or group not in groups:
            self.instance.groups.clear()
            self.instance.groups.add(group)
            self.instance.save()
