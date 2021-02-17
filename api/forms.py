from django import forms

class PriceForm(forms.Form):
    date_from = forms.DateField(input_formats=['%Y-%m-%d'], required=True)
    date_to = forms.DateField(input_formats=['%Y-%m-%d'], required=True)
    orig_code = forms.CharField(max_length=10, required=True)
    destination_code = forms.CharField(max_length=10, required=True)
    price = forms.IntegerField(required=True)