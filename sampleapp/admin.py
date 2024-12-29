from .models import RelyingParty, ConsentAccessToken, ConsentAccessTokenScope
from django.contrib import admin

admin.site.register(RelyingParty)
admin.site.register(ConsentAccessToken)
admin.site.register(ConsentAccessTokenScope)
