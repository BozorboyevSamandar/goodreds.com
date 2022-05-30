from django import forms
from django.core.mail import send_mail
from users.models import CustomUser


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()

        if user.email:
            send_mail(
                "Welcome to Goodreads website",
                f"Hi, {user.username}. Welcome to Goodreads Clone. Enjoy the books and reviews",
                'samandarbozorboyev29@gmail.com',
                [user.email]
            )

        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile_picture', 'username', 'first_name', 'last_name', 'email')








    # username = forms.CharField(max_length=150)
    # email = forms.EmailField()
    # first_name = forms.CharField(max_length=150)
    # last_name = forms.CharField(max_length=150)
    # password = forms.CharField(max_length=128)
    #
    # def save(self):
    #     username = self.cleaned_data['username']
    #     first_name = self.cleaned_data['first_name']
    #     last_name = self.cleaned_data['last_name']
    #     email = self.cleaned_data['email']
    #     password = self.cleaned_data['password']
    #
    #     user = User.objects.create(
    #         username=username,
    #         first_name=first_name,
    #         last_name=last_name,
    #         email=email,
    #     )
    #     user.set_password(password)
    #     user.save()
    #
    #     return user
