from email import message
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views.generic import CreateView
from .models import User ,Client,Epicier,Epicerie
from .forms import ClientSignUpForm,EpicierSignUpForm,ClientForm,EpicierForm,ChangePasswordForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate, login


# Create your views here.

# class Client_register(CreateView):
    # model = User  
    # form_class = ClientSignUpForm
    # template_name= 'accounts/client_register.html'

    # def form_valid(self, form_class):
    #     user = form_class.data_save()
    #     login(self.request, user)
    #     return redirect('home')

def register(request):
    return render(request, 'accounts/register.html')

class Epicier_register(CreateView):
    model = User  
    form_class = EpicierSignUpForm
    template_name= 'accounts/epicier_register.html'

    def form_valid(self, form_class):
        user = form_class.data_save()
        login(self.request, user)
        return redirect('home')

def Client_register(request):
        if request.method == 'POST' :
            form=ClientSignUpForm(request.POST,user=request.user)
            if form.is_valid():
                form.data_save()
                messages.success(request, "Registration successful." )
                return redirect('home')
            messages.error(request, "Unsuccessful registration. Invalid information.")
        else:
            form=ClientSignUpForm(user=request.user)
        context={'form':form}
        return render(request,'accounts/client_register.html',context)

def login_user(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    return render(request, 'accounts/login.html',context={'form':AuthenticationForm()})

def logout_user(request):
    logout(request)
    return redirect('home')

def client_display(request):
    if request.user.is_superuser ==1:
        client=Client.objects.filter(user_id__is_Client=True,user_id__is_active=True)
    elif request.user.is_Epicier==1:
        epicier=Epicier.objects.get(user=request.user)
        epicerie=Epicerie.objects.filter(epicier=epicier)
        client=[]
        for element in epicerie:
            for c in Client.objects.filter(user_id__is_Client=True,user_id__is_active=True,epicerie=element):
                client.append(c) 
    else:
        return redirect('home')       
    context={'client':client}
    return render(request, 'accounts/client_display.html',context)

def updateepicier(request,pk):
    epicier=Epicier.objects.get(user_id=pk)
    form=EpicierForm(instance=epicier)
    if request.method=='POST':
        form=EpicierForm(request.POST,instance=epicier)
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = EpicierForm(instance=epicier)
    context={'form':form}
    return render(request,'accounts/epicier_form .html',context)

def updateclient(request,pk):
    client=Client.objects.get(user_id=pk)
    form=ClientForm(instance=client)
    if request.method=='POST':
        form=ClientForm(request.POST,instance=client)
        if form.is_valid():
            # client.save()
            form.save()
            return redirect('home')
    else:
        form = ClientForm(instance=client)
    context={'form':form}
    return render(request,'accounts/client_form.html',context)

def deleteclient(request,pk):
    client=Client.objects.get(user_id=pk)
    if request.method=='POST':
        user=User.objects.get(id=pk)
        user.is_active=False
        user.save()
        client.delete( )
        return redirect('home')
    return render(request,'project/delete.html',{'obj':client})

class Client_create(CreateView):
    model = User  
    form_class = ClientSignUpForm
    template_name= 'accounts/client_form.html'

    def form_valid(self, form_class):
        user = form_class.data_save()
        return redirect('client_display')

"""                   Profile                   """

def Profile_display(request,username):
    user = User.objects.get(username=username)
    context = {'user': user}
    if user.is_Client:
        client = Client.objects.get(user=user)
        context['client'] = client
    elif user.is_Epicier:
        epicier = Epicier.objects.get(user=user)
        context['epicier'] = epicier
    return render(request, 'accounts/profile.html', context)
@login_required
def password_update(request):
    if request.method == 'POST':
        password_form = ChangePasswordForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            auth_user = authenticate(username=user.username, password=password_form.cleaned_data['new_password2'])
            login(request, auth_user)
            messages.success(request, 'Votre profil a été mis à jour.')
            return redirect('home')
    else:
            password_form = ChangePasswordForm(request.user)
    context = {
        'password_form': password_form,
    }
    return render(request, 'accounts/changepassword.html', context)