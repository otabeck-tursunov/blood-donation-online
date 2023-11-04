from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from HomeApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', BoshSahifaView.as_view()),
    path('donorlar/<int:pk>/', DonorlarView.as_view()),
    path('donor/<int:pk>/', DonorView.as_view()),
    path('qon-sorash/', QonSorashView.as_view()),
    path('oluvchilar/', BarchaQonOluvchilarView.as_view()),
    path('donor-bolish/', DonorBolishView.as_view()),
    path("login/", Login,),
    path("logout/", Logout, name="logout"),
    path("profil/", profil, name="logout"),
    path('profil_tahrirlash/', profil_tahrirlash),
    path('status_belgilash/', status_belgilash),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
