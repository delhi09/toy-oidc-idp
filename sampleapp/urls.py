from django.urls import path

from . import views

app_name = "sampleapp"
urlpatterns = [
    path(
        ".well-known/openid-configuration/",
        views.DiscoveryView.as_view(),
        name="discovery",
    ),
    path("authorize/", views.AuthorizeView.as_view(), name="authorize"),
]
