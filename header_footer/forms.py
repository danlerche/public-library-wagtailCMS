from django import forms

class closeTickerForm(forms.Form):
	ticker = forms.BooleanField(widget=forms.HiddenInput(attrs={'value': 'True'}))


