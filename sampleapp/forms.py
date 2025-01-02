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


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput)
    scope = forms.CharField(widget=forms.HiddenInput)
    redirect_uri = forms.CharField(widget=forms.HiddenInput)
    state = forms.CharField(widget=forms.HiddenInput)
    client_id = forms.CharField(widget=forms.HiddenInput)
    nonce = forms.CharField(widget=forms.HiddenInput)

    def clean_scope(self):
        scope = self.cleaned_data["scope"].split()
        if "openid" not in scope:
            raise forms.ValidationError("Invalid scope")
        return scope


class TokenForm(forms.Form):
    redirect_uri = forms.CharField()
    grant_type = forms.CharField()
    code = forms.CharField()
    client_id = forms.CharField()
    client_secret = forms.CharField()

    def clean_grant_type(self):
        grant_type = self.cleaned_data["grant_type"]
        if grant_type != "authorization_code":
            raise forms.ValidationError("Invalid grant_type")
        return grant_type
