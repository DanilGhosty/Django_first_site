from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
    path('', views.load_mesages_home),
    path('search_user/', views.search_user, name="search_user"),
    path('<int:pk>', views.load_messages),
    path('ajax/<int:pk>', views.load_messages_ajax,name='chatroom_ajax'),
    ]