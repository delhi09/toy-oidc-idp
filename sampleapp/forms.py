from django import forms


class AuthorizeForm(forms.Form):
    response_type = forms.CharField()
    scope = forms.CharField()
    client_id = forms.CharField()
    state = forms.CharField()
    redirect_uri = forms.CharField()
    nonce = forms.CharField()

    def clean_response_type(self):
        response_type = self.cleaned_data["response_type"]
        if response_type != "code":
            raise forms.ValidationError("Invalid response_type")
        return response_type

    def clean_scope(self):
        scope = self.cleaned_data["scope"].split()
        if "openid" not in scope:
            raise forms.ValidationError("Invalid scope")
        return scope
