from django import forms
# from .models import Collage
#
class CollageForms(forms.Form):
    url_1 = forms.CharField(label='url_1', max_length=200, required=False )
    url_2 = forms.CharField(label='url_2', max_length=200, required=False )
    url_3 = forms.CharField(label='url_3', max_length=200, required=False )
    url_4 = forms.CharField(label='url_4', max_length=200, required=False )
    url_5 = forms.CharField(label='url_5', max_length=200, required=False )
    url_6 = forms.CharField(label='url_6', max_length=200, required=False )
    height = forms.IntegerField(label='height',required=False)
    width = forms.IntegerField(label='width', required=False)
    rows = forms.IntegerField(label='rows', required=False)
    columns = forms.IntegerField(label='columns', required=False)