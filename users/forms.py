from django import forms

from users.models import CustomUser


class UserRegisterForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])

        user.save()
        return user


class UserEditForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'photo')
