from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('signup',views.signup, name='signup'),
    path('login', views.signin,name='login'),
    path('logout', views.signout, name='logout'),
    path('topic_detail/<int:id>', views.topic, name='topic_detail'),
    path('post_comment/<int:id>', views.postcomment, name='post_comment'),
    path('addtopic', views.addtopic, name='addtopic')
]