from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("sample/", include("sampleapp.urls")),
    path("admin/", admin.site.urls),
]
