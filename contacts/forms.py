from django import forms
from .models import Contact

class SearchForm(forms.Form):
    search = forms.CharField(max_length=100,
                            widget=forms.TextInput(
                            attrs={
                                'placeholder': 'Enter any keyword',
                                'size': '50'
                                })
                            )
class ContactForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)
    class Meta:
        model = Contact
        fields = ('image', 'name', 'phone', 'ext', 'email', 'department', 'title')
    
    