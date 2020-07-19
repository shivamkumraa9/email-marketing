from django import forms

def v(value):
	if "@" in value:
		raise forms.ValidationError("Sender should not contain @")

class SendEmail(forms.Form):
	subject = forms.CharField(max_length = 30)
	sender = forms.CharField(max_length = 30,validators = [v])
	body = forms.CharField(widget=forms.Textarea)
