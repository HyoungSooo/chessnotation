from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI, File, Schema
from ninja.files import UploadedFile

api = NinjaAPI()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('rest-auth/', include('rest_auth.urls')),
]
