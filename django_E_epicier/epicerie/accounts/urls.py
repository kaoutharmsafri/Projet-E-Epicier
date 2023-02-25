from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('client_register/', views.Client_register, name='client_register'),
    # path('client_register/', views.Client_register.as_view(), name='client_register'),
    path('update-epicier/<str:pk>/',views.updateepicier,name='update-epicier'),
    path('epicier_register/', views.Epicier_register.as_view(), name='epicier_register'),
    path('client_display/', views.client_display, name='client_display'),
    path('update-client/<str:pk>/',views.updateclient,name='update-client'),
    path('delete-client/<str:pk>/',views.deleteclient,name='delete-client'),
        
    #                   PROFILE                   

    path('Profile_display/<str:username>/', views.Profile_display, name='Profile_display'),
    path('password_update/', views.password_update, name='password_update'),

]