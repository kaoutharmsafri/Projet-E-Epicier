# Projet E-Epicier
Ce projet de fin de module correspond à une application web qui gère les crédits des épiciers envers leurs clients.

pour que ce projet fonctionne vous devez suivre ces étapes:

-créer une base de données sur phpmyadmin nommée : 'db_epicerie'

-ouvrer la console des commandes :

cd desktop

mkdir django_E_epicier

cd django_E_epicier

py -3 -m venv venv

venv\scripts\activate

pip install django

django-admin startproject epicerie

cd epicerie

python manage.py startapp project

python manage.py startapp accounts

python -m pip install mysql-connector-python

pip install mysqlclient

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 

python manage.py createsuperuser

python manage.py runserver 


après avoir créer le super user rendez vous au site localhost http://127.0.0.1:8000/admin/ puis créer deux groupes:

-le 1er: 'userclient'

et ses permissions sont:

project | credit | Can view credit

project | produit | Can view produit

project | details credit | Can view details credit

accounts | client | Can change client

accounts | client | Can view client


et maintenant vous n'avez plus qu'à se rendre à http://127.0.0.1:8000/epicerie/home/ et déconnecter vous par 'Logout' (car vous êtes encore connectés en tant que super user ).Maintenant commencer votre expérience sur notre application app en toute simplicité.

On vous souhaite une bonne aventure ! 
