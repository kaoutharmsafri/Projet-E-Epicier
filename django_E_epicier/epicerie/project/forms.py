from django.forms import ModelChoiceField, ModelForm
from django.db import transaction
from django import forms
from .models import  Epicerie,Credit,DetailsCredit,Produit
from accounts.models import  Epicier,Client
# from .forms import CreditForm
class EpicerieForm(ModelForm):
    class Meta:
        model=Epicerie
        fields=['Nom_Epicerie','Adresse_Epicerie','Tel_Epicerie']
        widgets = {
            'Nom_Epicerie': forms.TextInput(attrs={'class': 'form-control'}),
            'Adresse_Epicerie': forms.TextInput(attrs={'class': 'form-control'}),
            'Tel_Epicerie': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CreditDetailForm(forms.ModelForm):
      class Meta:
        model=DetailsCredit
        fields=['produit','Quantite']
      Quantite=forms.IntegerField()
      widgets = {
            'Quantite': forms.TextInput(attrs={'class': 'form-control'}),
        }
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['produit'].widgets=attrs={'class': 'form-control'}
           

class CreditForm(forms.ModelForm):
      class Meta:
        model=Credit
        fields='__all__'
        widgets = {
            'Date_d_operation': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'Date_d_echeance': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'Total_Credit': forms.TextInput(attrs={'class': 'form-control'}),
            'Avance': forms.TextInput(attrs={'class': 'form-control'}),
        }
      def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(CreditForm, self).__init__(*args, **kwargs)
            epicier=Epicier.objects.get(user_id=user)
            self.fields['epicerie'] = forms.ModelChoiceField(
                  queryset=Epicerie.objects.filter(epicier=epicier),
            widget=forms.Select(attrs={'class': 'form-control'}))
            epicerie=Epicerie.objects.filter(epicier=epicier)
            self.fields['client'] = forms.ModelChoiceField(
                  queryset=Client.objects.filter(epicerie__in=epicerie),
            widget=forms.Select(attrs={'class': 'form-control'}))
   
class CreditUpdateForm(forms.ModelForm):
      class Meta:
        model=Credit
        fields='__all__'
        widgets = {
            'Date_d_operation': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'Date_d_echeance': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'Total_Credit': forms.TextInput(attrs={'class': 'form-control'}),
            'Avance': forms.TextInput(attrs={'class': 'form-control'}),

        }
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['ID_Credit'] = forms.CharField(initial=self.instance.id,widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
            self.fields['Date_d_operation'].initial = self.instance.Date_d_operation
            self.fields['Total_Credit'].initial = self.instance.Total_Credit
            self.fields['Date_d_echeance'].initial = self.instance.Date_d_echeance
            self.fields['Etat'].initial = self.instance.Etat
            self.fields['Avance'].initial = self.instance.Avance
            client = self.instance.client
            self.fields['client'] = forms.ModelChoiceField(
                  queryset=Client.objects.filter(pk=client),
            widget=forms.Select(attrs={'class': 'form-control'}))
            self.fields['epicerie'] = forms.ModelChoiceField(
                  queryset=Epicerie.objects.filter(pk=client.epicerie.pk),
            widget=forms.Select(attrs={'class': 'form-control'}))
   
class ProduitForm(forms.ModelForm):
      class Meta:      
            model = Produit
            fields = ['Description_Produit','Prix_Produit','Disponibilité','epicerie']
            widgets = {
            'Description_Produit': forms.TextInput(attrs={'class': 'form-control'}),
            'Prix_Produit': forms.TextInput(attrs={'class': 'form-control'}),
        }
      def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(ProduitForm, self).__init__(*args, **kwargs)
            epicier=Epicier.objects.get(user_id=user)
            self.fields['epicerie'] = forms.ModelChoiceField(
                  queryset=Epicerie.objects.filter(epicier=epicier),
            widget=forms.Select(attrs={'class': 'form-control'}))

class ProduitUpdateForm(forms.ModelForm):
      class Meta:      
            model = Produit
            fields = ['Description_Produit','Prix_Produit','Disponibilité','epicerie']
            widgets = {
            'Description_Produit': forms.TextInput(attrs={'class': 'form-control'}),
            'Prix_Produit': forms.TextInput(attrs={'class': 'form-control'}),
        }
      def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            epicerie = self.instance.epicerie
            self.fields['epicerie'] = forms.ModelChoiceField(
                  queryset=Epicerie.objects.filter(pk=epicerie.pk),
            widget=forms.Select(attrs={'class': 'form-control'}))