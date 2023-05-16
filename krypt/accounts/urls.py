from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('registeruser/', views.registeruser_view, name='registeruser'),
    path('createNewEthAccount/', views.createNewEthAccount_view, name='createNewEthAccount'),
    path('EthiriumTransaction/', views.EthiriumTransaction_view, name='EthiriumTransaction'),
    path('getBalance/', views.getBalance_view, name='getBalance'),
    path('getTransactions/', views.getTransactions_view, name='getTransactions'),
    path('logout/',views.logout, name = "logout"),
    path('getPrices/', views.getPrices ,name="getPrices") ,
    path('unlink/',views.unlink, name = "unlink"),
]   

