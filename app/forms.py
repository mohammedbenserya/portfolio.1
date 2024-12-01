# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    project_type = forms.ChoiceField(choices=[
        ('Web Scraping', 'Web Scraping'),
        ('Process Automation', 'Process Automation'),
        ('Data Processing', 'Data Processing'),
        ('Custom Solution', 'Custom Solution'),
    ])
    message = forms.CharField(widget=forms.Textarea)