from django.shortcuts import render,redirect
from django.template import RequestContext
from .forms import EpicerieForm ,CreditForm,ProduitForm,CreditDetailForm,CreditUpdateForm,ProduitUpdateForm
from .models import Epicerie,Produit,DetailsCredit,Credit
from accounts.models import Epicier,Client
from django.db import transaction
from django import forms
from django.contrib import messages

# from django.views.generic import CreateView,DetailView
from django.http import Http404

"""                    Home                    """

def home(request):
    return render(request, 'project/home.html')

"""                    Epicerie                    """

def epicerie_display(request):
    if request.user.is_superuser ==1:
        epicerie=Epicerie.objects.all()
    else:
        epicerie=Epicerie.objects.filter(epicier_id=request.user.id)
    context={'epicerie':epicerie}
    return render(request, 'project/epicerie_display.html',context)

def createepicerie(request):
    epicier=Epicier.objects.get(user=request.user)
    form=EpicerieForm()
    if request.method=='POST':
        form=EpicerieForm(request.POST)
        if form.is_valid():
            i=form.save(commit=False)
            i.epicier=epicier
            i.save()
            return redirect('home')
    context={'form':form}
    return render(request,'project/epicerie_form.html',context)

def updateepicerie(request,pk):
    epicerie=Epicerie.objects.get(id=pk)
    form=EpicerieForm(instance=epicerie)
    if request.method=='POST':
        form=EpicerieForm(request.POST,instance=epicerie).save()
        return redirect('home')
    context={'form':form}
    return render(request,'project/epicerie_form.html',context)

def deleteepicerie(request,pk):
    epicerie=Epicerie.objects.get(id=pk)
    if request.method=='POST':
        epicerie.delete(  )
        return redirect('home')
    return render(request,'project/delete.html',{'obj':epicerie})

"""                    Credits                    """

def credits_display(request):
    if request.user.is_superuser ==1:
        credit=Credit.objects.all()
    elif request.user.is_Client ==1:
        client=Client.objects.get(user=request.user)
        credit=Credit.objects.filter(client=client)
    else:
        epicier=Epicier.objects.get(user=request.user)
        epicerie=Epicerie.objects.filter(epicier=epicier)
        credit=[]
        for element in epicerie:
            for c in Credit.objects.filter(epicerie=element):
                credit.append(c)
    context={'credit':credit}
    return render(request, 'project/credits_display.html',context)

def createcredits(request): 
    if request.method=='POST':
        form=CreditForm(request.POST,user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful." )
            return redirect('credits_display')
    else:
        form=CreditForm(user=request.user)
    context={'form':form}
    return render(request,'project/credit_form.html',context)
   
def updatecredits(request,pk):
    credit=Credit.objects.get(id=pk)
    form=CreditUpdateForm(instance=credit)
    if request.method=='POST':
        form=CreditUpdateForm(request.POST,instance=credit).save()
        return redirect('credits_display')
    else:
        form = CreditUpdateForm(instance=credit)
    context={'form':form}
    return render(request,'project/credit_form.html',context)

def deletecredits(request,pk):
    credit=Credit.objects.get(id=pk)
    if request.method=='POST':
        credit.delete(  )
        return redirect('credits_display')
    return render(request,'project/delete.html',{'obj':credit})

"""                    Produit                    """

def produits_display(request):
    if request.user.is_superuser ==1:
        produit=Produit.objects.all()
    elif request.user.is_Client ==1:
        client=Client.objects.get(user=request.user)
        produit=Produit.objects.filter(epicerie=client.epicerie)
    else:
        epicier=Epicier.objects.get(user=request.user)
        epicerie=Epicerie.objects.filter(epicier=epicier)
        produit=[]
        for element in epicerie:
            for p in Produit.objects.filter(epicerie=element):
                produit.append(p)
    context={'produit':produit}
    return render(request, 'project/produits_display.html',context)

def createproduits(request):
    if request.method=='POST':
        form=ProduitForm(request.POST,user=request.user)
        if form.is_valid():
            form.save()
            return redirect('produits_display')
    else:
        form=ProduitForm(user=request.user)
    context={'form':form}
    return render(request,'project/produit_form.html',context)

def updateproduits(request,pk):
    produit=Produit.objects.get(id=pk)
    form=ProduitUpdateForm(instance=produit)
    if request.method=='POST':
        form=ProduitUpdateForm(request.POST,instance=produit)
        if form.is_valid():
            i=form.save(commit=False)
            i.produit=produit
            i.save()
            form.save()
        return redirect('produits_display')
    context={'form':form}
    return render(request,'project/produit_form.html',context)

def deleteproduits(request,pk):

    produit=Produit.objects.get(id=pk)
    if request.method=='POST':
        produit.delete(  )
        return redirect('produits_display')
    return render(request,'project/delete.html',{'obj':produit})

"""                    Details credit                    """

def credits_detail_display(request,pk):
    credit_detail=DetailsCredit.objects.filter(credit_id=pk)
    # count = credit_detail.count()
    # for element in credit_detail:
    #     element.count = credit_detail.count()
    #     credit_detail_with_count.append(element)
    for element in credit_detail:
        element.count = credit_detail.count()
    context = {'credit_detail': credit_detail}
    # context={'credit_detail':credit_detail,'count': count}
    return render(request, 'project/credits_detail_display.html',context)
    

def createcredits_detail(request,pk):
    form=CreditDetailForm()
    credit=Credit.objects.get(id=pk)
    if request.method=='POST':
        form=CreditDetailForm(request.POST)
        if form.is_valid():
            i=form.save(commit=False)
            i.credit=credit
            i.Total=i.produit.Prix_Produit * i.Quantite
            i.save()
        return redirect('credits_display')
    context={'form':form}
    return render(request,'project/credit_form.html',context)

