from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from django.utils.translation import ugettext_lazy as _

from ResistenciaCoC.models import Clan


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=50)

    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect user or password")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class RegistrationForm(ModelForm):
    password2 = forms.CharField(label=_("Confirm password"), widget=forms.PasswordInput)

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name')

        widgets = {
            'password': forms.PasswordInput(),
            'username': forms.EmailInput(),

        }
        labels = {
            'username': 'Email',
            'first_name': 'In game name',
        }
        error_messages = {
            'username': {
                'unique': _("The email already exists."),
            },
        }
        help_texts = {
            'username': "",
        }

    # Password verification
    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
            )
        return password2

class CreateClanForm (ModelForm):

    class Meta:
        model = Clan

        fields = ('name', 'tag')

        error_messages = {
            'tag': {
                'unique': _('This clan tag is already taken.'),
            }
        }

    # Check if there is already a clan with this tag.
    def clean(self):
        cleaned_data = self.cleaned_data
        if Clan.objects.filter(tag=cleaned_data['tag']).exists():
            raise ValidationError(_('This clan tag is already taken.'))

        print cleaned_data['tag']

        if len(cleaned_data['tag']) != 8:
            raise ValidationError(_('The clan tag must have 8 characters.'))

        return cleaned_data