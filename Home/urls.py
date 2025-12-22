from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('signup',views.signup, name='signup'),
    path('login', views.signin,name='login'),
    path('logout', views.signout, name='logout')
]