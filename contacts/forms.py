from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize= value.size
    if filesize > 2097152:
        raise ValidationError(f"The maximum file size that can be uploaded is 2mb but found {round(filesize*0.00000095367432,1)}mb")
    else:
        return value

def validate_file_extension(value):
	return FileExtensionValidator(["csv"])(value)


class NewListForm(forms.Form):
    name = forms.CharField(max_length = 20)
    file = forms.FileField(validators=[validate_file_extension,validate_file_size],required = False)


class FileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension,validate_file_size])


class ContactForm(forms.Form):
    name = forms.CharField(max_length = 20)
    email = forms.EmailField()
