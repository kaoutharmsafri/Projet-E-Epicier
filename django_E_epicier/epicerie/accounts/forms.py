from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms
from .models import  User , Client, Epicier,Epicerie
from django.forms import ModelChoiceField, ModelForm
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm
class ClientSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    adress = forms.CharField(required=False)
    epicerie=ModelChoiceField(queryset=Epicerie.objects.all())
    class Meta(UserCreationForm.Meta):
        model = User
    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(ClientSignUpForm, self).__init__(*args, **kwargs)
            epicier=Epicier.objects.get(user_id=user)
            self.fields['epicerie'] = forms.ModelChoiceField(queryset=Epicerie.objects.filter(epicier=epicier),to_field_name='Nom_Epicerie',widget=forms.Select(attrs={'class': 'form-control'}))

   
    @transaction.atomic
    def data_save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_Client = True
        
        user.save()
        grp=Group.objects.get(name="userclient")
        user.groups.add(grp)
        client = Client.objects.create(user=user)
        client.phone_number = self.cleaned_data.get('phone_number')
        client.adress = self.cleaned_data.get('adress')
        client.epicerie = self.cleaned_data['epicerie']
        client.save()
        return user

class EpicierSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    adress = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def data_save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_Epicier = True
        
        user.save()
        grp=Group.objects.get(name="usermanager")
        user.groups.add(grp)
        epicier = Epicier.objects.create(user=user)
        epicier.phone_number = self.cleaned_data.get('phone_number')
        epicier.adress = self.cleaned_data.get('adress')
        epicier.save()
        return user

class ClientForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=80)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=80)
    class Meta:
        model=Client
        fields='__all__'
        exclude = ['user']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'class': 'form-control'}),
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # *** instance
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.initial['phone_number'] = self.instance.phone_number
        self.initial['adress'] = self.instance.adress
        # **** label
        self.fields['first_name'].label = 'Prénom'
        self.fields['last_name'].label = 'Nom'
        self.fields['phone_number'].label = 'Téléphone'
        self.fields['adress'].label = 'Addresse'
        # **** filter
        client = self.instance.epicerie
        self.fields['epicerie'] = forms.ModelChoiceField(queryset=Epicerie.objects.filter(pk=client.pk),to_field_name='Nom_Epicerie',widget=forms.Select(attrs={'class': 'form-control'}))
        self.fields['user'] = forms.CharField(initial=self.instance.user.username,widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))

    def save(self, commit=True):
        client = super().save(commit=False)
        user = client.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            client.save()
            user.save()
        return client

class EpicierForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=80)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=80)
    class Meta:
        model=Epicier
        fields='__all__'
        exclude = ['epicerie']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'adress': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.initial['phone_number'] = self.instance.phone_number
        self.initial['adress'] = self.instance.adress
        self.fields['user'].label = 'Epicier'

        user = self.instance
        self.fields['user'] = forms.CharField(initial=self.instance.user.username,widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    def save(self, commit=True):
        epicier = super().save(commit=False)
        user = epicier.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            epicier.save()
            user.save()
        return epicier
        # self.fields['user'] = forms.ModelChoiceField(queryset=Epicier.objects.filter(pk=user.pk),widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))

class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'old_password': forms.TextInput(attrs={'class': 'form-control'}),
            'new_password1': forms.TextInput(attrs={'class': 'form-control'}),
            'new_password2': forms.TextInput(attrs={'class': 'form-control'}),
        }
    