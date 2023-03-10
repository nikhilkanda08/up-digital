from django import forms
from django.contrib import auth
from bot.models import *
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

class ReadOnlyPasswordHashWidget(forms.Widget):
    template_name = 'auth/widgets/read_only_password_hash.html'
    read_only = True

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary.append({'label': gettext("No password set.")})
        else:
            try:
                hasher = identify_hasher(value)
            except ValueError:
                summary.append({'label': gettext("Invalid password format or unknown hashing algorithm.")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({'label': gettext(key), 'value': value_})
        context['summary'] = summary
        return context
class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        kwargs.setdefault('disabled', True)
        super().__init__(*args, **kwargs)

class LoginForm(forms.Form):
    email = forms.EmailField(label=_(u'Your email_id'))
    password = forms.CharField(widget=forms.PasswordInput, label=_(u'Password'))

    def clean_email(self):
        data = self.cleaned_data['email']
        if not data:
            raise forms.ValidationError(_("Please enter email_id"))
        return data

    def clean_password(self):
        data = self.cleaned_data['password']
        if not data:
            raise forms.ValidationError(_("Please enter your password"))
        return data

    def clean(self):
        try:
            email = User.objects.get(email__iexact=self.cleaned_data['email']).email
        except User.DoesNotExist:
            raise forms.ValidationError(_("No such email registered"))
        password = self.cleaned_data['password']
        self.user = auth.authenticate(email=email, password=password)
        if self.user is None or not self.user.is_active:
            raise forms.ValidationError(_("email_id or password is incorrect"))

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        acc = User.objects.filter(email=email.lower()).count()
        if acc > 0:
            raise forms.ValidationError('An account with this email already exists')
        return email.lower()

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password',)


    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        return user

    # def clean(self):
    #     cleaned_data = super().clean()
    #     phone = cleaned_data.get('phone')
    #     print(phone)
    #     if phone is not None:
    #         phone_output = ''.join(c for c in phone if c.isdigit())
    #         if len(phone_output) < 10 or len(phone_output) > 11:
    #             raise ValidationError('Phone Number format is: xxxxxxxxxx')