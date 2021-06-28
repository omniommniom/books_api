from django import forms


class ChooseQuery(forms.Form):
    query = forms.CharField(max_length=255)
