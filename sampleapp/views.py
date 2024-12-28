from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View

from sampleapp.forms import AuthorizeForm


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
        print("authorize params: ", form.cleaned_data)
        return HttpResponse("todo")
