from django import forms
from .models import UniCollection, Link

class UniCollectionForm(forms.ModelForm):
    collection_url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "link-input", "placeholder": "Paste here a link..."}))
    
    class Meta:
        model = UniCollection
        fields = ('collection_url',)


class CollectionPasswordAdd(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class": "link-input", "placeholder": "Password..."}))
    
    class Meta:
        model = UniCollection
        fields = ("password",)


class UniCollectionEditForm(forms.ModelForm):
    collection_name = forms.CharField(widget=forms.TextInput(
        attrs={"class": "sim-input", "placeholder": "Name this unilection..."}))
    
    description = forms.CharField(widget=forms.TextInput(
        attrs={"class": "sim-input", "placeholder": "Description here..."}), required=False)

    class Meta:
        model = UniCollection
        fields = ('collection_name', 'description')


class CollectionAddForm(forms.ModelForm):
    url = forms.URLField(widget=forms.URLInput(
        attrs={"class": "link-input", "placeholder": "Your link to save"}))
    
    class Meta:
        model = Link
        fields = ("url",)
