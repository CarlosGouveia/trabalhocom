from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

class login_form(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True, 'class':'form-control text-center'}))
    password = forms.CharField(label="Password", strip=False, widget=forms.PasswordInput(attrs={'class':'form-control text-center'}))


class RegisterForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password1 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : '999.999.999-99'}))
    rg = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    dt_nasc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    rua = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    numero = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bairro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cidade = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        # user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'telefone', 'cpf', 'sexo', 'rua','dt_nasc', 'rg','numero', 'bairro', 'estado', 'cidade']
        # fields = '__all__'

class EditAccountForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    rua = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    numero = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bairro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cidade = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))


    class Meta:
        model = User
        fields = ['username', 'telefone', 'rua', 'numero', 'bairro', 'estado', 'cidade', 'image']
