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
    path(
        "consent/<str:consent_access_token>/",
        views.ConsentView.as_view(),
        name="consent",
    ),
    path("token/", views.TokenView.as_view(), name="token"),
]
