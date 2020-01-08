from django import forms
from django.forms.models import inlineformset_factory
from django.forms import formset_factory
from .models import *

from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class CreateAuctionForm(forms.ModelForm):
    nazivpredmeta = forms.CharField(label="Naziv predmeta")
    aktuelnaponuda = forms.IntegerField(label="Pocetna cena")
    kupiodmah = forms.BooleanField(label="Opcija 'Kupi odmah'", required=False)
    kupiodmahcena = forms.IntegerField(label="Kupi odmah cena", required=False)
    opispredmeta = forms.CharField(widget=forms.Textarea(attrs={ "rows": 4,"cols": 25}), 
    label="Opis predmeta", required=False)
    proizvodjac = forms.CharField(required=False)
    kategorije = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, 
    queryset = Kategorija.objects.all())
    datumisteka = forms.DateTimeField(label="Datum isteka")

    class Meta:
    	model = Aukcija
    	fields = [
    		'idaukcije',
    		'nazivpredmeta',
    		'datumisteka',
    		'aktuelnaponuda',
    		'kupiodmah',
    		'kupiodmahcena',
    		'opispredmeta',
    		'proizvodjac',
    		'kategorije',
    	]
    	

    # def __init__(self, user, *args, **kwargs):
         # user = kwargs.pop('user','')
         # super(CreateAuctionForm, self).__init__(*args, **kwargs)
        # self.fields['idprodavca']=forms.ModelChoiceField(queryset=Korisnik.objects.filter(username=user), required=True, label="Prodavac")

class AddValuesForm(forms.Form):
	value = forms.ModelChoiceField(queryset=PonudjeneVrednosti.objects.all(), label='') 

class KorisnikCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = Korisnik
        fields =('username','email', 'first_name', 'last_name', 'adresa','grad','opstina', 'drzava', 'telefon')

class KorisnikChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Korisnik
        fields = ('username', 'email', 'lista_zelja',)

class PonudaForm(forms.ModelForm):
    class Meta:
        model = Ponuda
        fields = ('cena',)

class OcenjivanjeForm(forms.ModelForm):
    CHOICES= [('pozitivna', 'Pozitivna'), ('negativna', 'Negativna')]
    ocena=forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    komentar=forms.CharField(widget=forms.Textarea(attrs={ "rows": 4,"cols": 25}))
    class Meta:
        model=Ocena
        fields=('ocena','komentar',)