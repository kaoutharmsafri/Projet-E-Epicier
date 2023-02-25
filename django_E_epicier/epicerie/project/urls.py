from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),

    #                    Epicerie                    

    path('epicerie_display/', views.epicerie_display, name='epicerie_display'),
    path('create-epicerie/',views.createepicerie,name='createepicerie'),
    path('update-epicerie/<str:pk>/',views.updateepicerie,name='update-epicerie'),
    path('delete-epicerie/<str:pk>/',views.deleteepicerie,name='delete-epicerie'),

    #                    Credits                    

    path('credits_display/', views.credits_display, name='credits_display'),
    path('create-credits/',views.createcredits,name='createcredits'),
    path('update-credits/<str:pk>/',views.updatecredits,name='update-credits'),
    path('delete-credits/<str:pk>/',views.deletecredits,name='delete-credits'),
    
    #                    Produit                    
    
    path('produits_display/', views.produits_display, name='produits_display'),
    path('create-produits/',views.createproduits,name='createproduits'),
    path('update-produits/<str:pk>/',views.updateproduits,name='update-produits'),
    path('delete-produits/<str:pk>/',views.deleteproduits,name='delete-produits'),
    
    #                    Detail Credit                    

    path('credits_detail_display/<int:pk>/', views.credits_detail_display, name='credits_detail_display'),
    # path('credits_detail_display/<int:pk>/', views.CreditsDetailView.as_view(), name='CreditsDetailView'),
    path('createcredits_detail/<int:pk>/', views.createcredits_detail, name='createcredits_detail'),


    ]