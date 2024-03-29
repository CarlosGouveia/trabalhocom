from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .mail import send_mail_template

class contato_form(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu nome completo'}), max_length=100)
    email_contato= forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Digite seu email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite aqui sua mensagem'}))
    assunto = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o assunto da mensagem'}), max_length=40)

    # def send_email(self, course):
    #     subject = '[%s] Contato' % course
    #     message = 'Nome: %n(name)s;E-mail: %(email)s;%(message)s'
    #     context = {
    #         'name': self.cleaned_data['name'],
    #         'email': self.cleaned_data['email'],
    #         'message' : self.cleaned_data['message']
    #     }
    #     message = message % context
    #     send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
    class Meta:
        fields = ['username','email_contato','assunto','message']

    def send_mail(self):
        #subject = 'Contato'
        subject = self.cleaned_data['assunto']
        context = {
            'username': self.cleaned_data['username'],
            'email_contato': self.cleaned_data['email_contato'],
            'message': self.cleaned_data['message'],
        }
        template_name = 'contato_email.html'
        send_mail_template(
            subject, template_name, context, [settings.CONTACT_EMAIL]
        )