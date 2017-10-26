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
    # nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    rua = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    numero = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
    bairro = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
    cidade = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))
    estado = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control'}))


    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError('A confirmação não está correta')
    #     return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        # user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'telefone', 'cpf', 'sexo', 'rua', 'numero', 'bairro', 'estado', 'cidade']
        # fields = '__all__'

class EditAccountForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    rua = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    numero = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bairro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cidade = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'telefone', 'rua', 'numero', 'bairro', 'estado', 'cidade']
        # fields = '__all__'
