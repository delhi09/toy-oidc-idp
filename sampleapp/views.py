from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views import View

from sampleapp.forms import AuthorizeForm, LoginForm
from sampleapp.models import RelyingParty
from django.contrib.auth import authenticate, login


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

        return render(request, "login.html", {"form": LoginForm()})

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
        return HttpResponse("Logged in")
