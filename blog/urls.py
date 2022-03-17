from django.conf.urls import include,url
from django.urls import path
from . import views
#from django.contrib.staticfiles.urls import staticfiles_urlspatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.main_page),
    path('register/',views.register),
    path('logout/',views.logout_request),
    path('login/', views.login_request),
    path('profile/',views.profile, name = 'user_profile'),
    path('search_post/',views.search_post,name="search_post"),
    path('add_post/',views.add_post,name="add_post"),
    path('like<int:pk>', views.LikeView, name='like_post'),
    

    path('<single_slug>/', views.single_slug, name = "slug_url"),
    


    
    

]
urlpatterns+=static(settings.STATIC_URL,
                    document_roor=settings.STATIC_ROOT)