# from django.urls import reverse
from django.db import models
from django.db import transaction
# from accounts.models import Epicier,Client

class Epicerie(models.Model):
    Nom_Epicerie=models.CharField(max_length=255)
    Adresse_Epicerie=models.CharField(max_length=255)
    Tel_Epicerie=models.CharField(max_length=10)
    epicier=models.ForeignKey('accounts.Epicier', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)+" - "+self.Nom_Epicerie


class Produit(models.Model):
    Description_Produit = models.CharField(max_length=250)
    # image=models.ImageField()
    Prix_Produit = models.FloatField()
    Disponibilité = models.BooleanField()
    epicerie=models.ForeignKey('project.Epicerie', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id)+" - "+self.Description_Produit

class Credit(models.Model):
    Date_d_operation = models.DateField()
    # Nombre_d_articles = models.AutoField()
    Total_Credit = models.FloatField()
    Date_d_echeance = models.DateField()
    Etat = models.BooleanField()
    Avance = models.FloatField()
    client=models.ForeignKey('accounts.Client', on_delete=models.CASCADE)
    epicerie=models.ForeignKey(Epicerie, on_delete=models.CASCADE)



class DetailsCredit(models.Model):
    credit=models.ForeignKey(Credit,on_delete=models.CASCADE)
    produit=models.ForeignKey(Produit,on_delete=models.CASCADE)
    # Description_Produit=models.OneToOneField(Produit,on_delete=models.CASCADE)
    Quantite=models.IntegerField()
    # Prix=models.OneToOneField(Produit,on_delete=models.CASCADE, related_name="Prix")
    Total=models.FloatField()
    def DetailsCredit_total(self):
        return self.Quantite * self.produit.Prix
#, related_name="Description_Produit"