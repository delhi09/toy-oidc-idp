from datetime import datetime, timedelta
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from sampleapp.forms import AuthorizeForm, LoginForm
from sampleapp.models import ConsentAccessToken, ConsentAccessTokenScope, RelyingParty
from django.contrib.auth import authenticate, login
from django.utils import crypto
from django.contrib.auth.mixins import LoginRequiredMixin


class DiscoveryView(View):
    def get(self, request):
        return JsonResponse(
            {
                "authorization_endpoint": "http://localhost:8000/sample/authorize/",
            }
        )


class AuthorizeView(View):
    def get(self, request):
        form = AuthorizeForm(request.GET)
        if not form.is_valid():
            return HttpResponseBadRequest()
        client_id = form.cleaned_data["client_id"]
        if not RelyingParty.objects.filter(client_id=client_id).exists():
            return HttpResponseBadRequest()

        return render(
            request,
            "login.html",
            {
                "form": LoginForm(
                    initial={
                        "scope": " ".join(form.cleaned_data["scope"]),
                        "redirect_uri": form.cleaned_data["redirect_uri"],
                        "state": form.cleaned_data["state"],
                    }
                )
            },
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, "login.html", {"form": form})
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is None:
            form.add_error(None, "IDかパスワードが間違っています")
            return render(request, "login.html", {"form": form})
        login(request, user)
        token = ConsentAccessToken.objects.create(
            token=crypto.get_random_string(8),
            user=user,
            expired_at=datetime.now() + timedelta(minutes=10),
            redirect_uri=form.cleaned_data["redirect_uri"],
            state=form.cleaned_data["state"],
        )
        for scope in form.cleaned_data["scope"]:
            ConsentAccessTokenScope.objects.create(token=token, scope=scope)
        return redirect("sampleapp:consent", consent_access_token=token.token)


class ConsentView(LoginRequiredMixin, View):
    def get(self, request, consent_access_token):
        token = ConsentAccessToken.objects.filter(
            token=consent_access_token,
            user=request.user,
            expired_at__gte=datetime.now(),
        ).get()
        return render(request, "consent.html", {"consent_access_token": token})

    def post(self, request, consent_access_token):
        token = ConsentAccessToken.objects.filter(
            token=consent_access_token,
            user=request.user,
            expired_at__gte=datetime.now(),
        ).get()
        code = crypto.get_random_string(8)
        location_url = f"{token.redirect_uri}?code={code}&state={token.state}"
        token.delete()
        return redirect(location_url)
