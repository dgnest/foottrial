
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from .models import MyUser


class UserLoginForm(forms.Form):

    '''A form for login users.'''

    # Username or email.
    email = forms.EmailField(
        max_length=255,
    )
    password = forms.CharField(
        max_length=255,
        min_length=6,
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if MyUser.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(_('Email is not registered'))


class CleanNamesForm(forms.ModelForm):

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return first_name.title()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return last_name.title()


class UserCreationForm(CleanNamesForm):

    '''A form for creating new users. Includes all the required
    fields, plus a repeated password.'''

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        max_length=255,
        min_length=6,
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = MyUser
        fields = '__all__'
        pass

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_('Passwords don\'t match'))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(CleanNamesForm):

    '''A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    '''

    password = ReadOnlyPasswordHashField(
        help_text=_(
            'Raw passwords are not stored, so there is no way to see '
            'this user\'s password, but you can change the password '
            'using <a href=\'password/\'>this form</a>.'
        )
    )

    class Meta:
        model = MyUser
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value.
        return self.initial['password']
