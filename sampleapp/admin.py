from .models import (
    RelyingParty,
    ConsentAccessToken,
    ConsentAccessTokenScope,
    AuthorizationCode,
    JwtKeyPair,
)
from django.contrib import admin
from django.utils import crypto
from django.contrib.auth.hashers import make_password


class RelyingPartyAdmin(admin.ModelAdmin):
    list_display = ["name", "client_id"]

    def save_model(self, request, obj, form, change):
        client_secret = crypto.get_random_string(16)
        print("client_secret:", client_secret)
        obj.client_secret = make_password(client_secret)
        return super().save_model(request, obj, form, change)


admin.site.register(RelyingParty, RelyingPartyAdmin)
admin.site.register(ConsentAccessToken)
admin.site.register(ConsentAccessTokenScope)
admin.site.register(AuthorizationCode)
admin.site.register(JwtKeyPair)
