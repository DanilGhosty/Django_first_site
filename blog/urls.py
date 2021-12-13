from django.conf.urls import include,url
from django.urls import path
from . import views
#from django.contrib.staticfiles.urls import staticfiles_urlspatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.main_page)

]
urlpatterns+=static(settings.STATIC_URL,
                    document_roor=settings.STATIC_ROOT)