from django import forms
from .models import Service

class FormCadastroSevico(forms.ModelForm):

    descricao_servico = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tempo_experiencia = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    descricao_exp = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    valor = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def save(self, request):
        data = self.cleaned_data
        servico = Service()
        servico.usuario = request.user
        servico.categoria = data['categoria']
        servico.descricao_servico = data['descricao_servico']
        servico.tempo_experiencia = data['tempo_experiencia']
        servico.unid_tempo = data['unid_tempo']
        servico.descricao_exp = data['descricao_exp']
        servico.valor = data['valor']
        servico.valor_servico = data['valor_servico']
        servico.unid_tempo = data['unid_tempo']

        servico.save()

    class Meta:
        model = Service
        fields = ['descricao_servico', 'valor', 'valor_servico', 'tempo_experiencia', 'unid_tempo', 'descricao_exp','categoria']

class AtualizarServicoForm(forms.ModelForm):

    descricao_servico = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tempo_experiencia = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    descricao_exp = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    valor = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Service
        fields = ['categoria','descricao_servico', 'valor', 'valor_servico', 'tempo_experiencia', 'unid_tempo', 'descricao_exp']


class DetalhaServicoForm(forms.ModelForm):

    descricao_servico = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    tempo_experiencia = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    descricao_exp = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    valor = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
