from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
    redirect_url = forms.CharField(widget=forms.HiddenInput, required=False)

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
    reenter_password = forms.CharField(label='Password',widget=forms.PasswordInput(render_value=False))
    email = forms.EmailField()
    
    def clean(self):
        password = self.cleaned_data['password']
        reenter_password = self.cleaned_data['reenter_password']
        if password != reenter_password:
            raise forms.ValidationError("Your passwords did not match")
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user by that name already exists. Pick another.")
        return username

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(data['username'], data['email'], data['password'])
        return user

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
