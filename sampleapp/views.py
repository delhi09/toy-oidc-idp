from datetime import datetime, timedelta
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from sampleapp.forms import AuthorizeForm, LoginForm, TokenForm
from sampleapp.models import (
    AuthorizationCode,
    ConsentAccessToken,
    ConsentAccessTokenScope,
    RelyingParty,
)
from django.contrib.auth import authenticate, login
from django.utils import crypto
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password


class DiscoveryView(View):
    def get(self, request):
        return JsonResponse(
            {
                "authorization_endpoint": "http://localhost:8000/sample/authorize/",
                "token_endpoint": "http://localhost:8000/sample/token/",
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
                        "client_id": form.cleaned_data["client_id"],
                        "nonce": form.cleaned_data["nonce"],
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
            expired_at=datetime.now() + timedelta(minutes=120),
            redirect_uri=form.cleaned_data["redirect_uri"],
            state=form.cleaned_data["state"],
            client=RelyingParty.objects.get(client_id=form.cleaned_data["client_id"]),
            nonce=form.cleaned_data["nonce"],
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

        # 認可コード発行
        code = crypto.get_random_string(8)
        AuthorizationCode.objects.create(
            code=code,
            redirect_uri=token.redirect_uri,
            client=token.client,
            expired_at=datetime.now() + timedelta(minutes=120),
            user=request.user,
            nonce=token.nonce,
        )

        # リダイレクト先URL作成
        location_url = f"{token.redirect_uri}?code={code}&state={token.state}"

        token.delete()
        return redirect(location_url)


@method_decorator(csrf_exempt, name="dispatch")
class TokenView(View):
    def post(self, request):
        form = TokenForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest()
        try:
            relying_party = RelyingParty.objects.get(
                client_id=form.cleaned_data["client_id"]
            )
        except RelyingParty.DoesNotExist:
            return HttpResponseBadRequest()
        if not check_password(
            form.cleaned_data["client_secret"], relying_party.client_secret
        ):
            return HttpResponseBadRequest()
        try:
            authorization_code = AuthorizationCode.objects.get(
                code=form.cleaned_data["code"],
                client=relying_party,
                expired_at__gte=datetime.now(),
            )
        except AuthorizationCode.DoesNotExist:
            return HttpResponseBadRequest()
        if form.cleaned_data["redirect_uri"] != authorization_code.redirect_uri:
            return HttpResponseBadRequest()
        id_token_data = {
            "iss": "http://localhost:8000",
            "sub": authorization_code.user.id,
            "aud": relying_party.client_id,
            "nonce": authorization_code.nonce,
            "exp": int((datetime.now() + timedelta(minutes=10)).timestamp()),
            "iat": int(datetime.now().timestamp()),
        }
        print("id_token_data:", id_token_data)
        return JsonResponse({})
