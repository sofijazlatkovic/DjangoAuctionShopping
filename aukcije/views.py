from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.core.validators import MinValueValidator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.forms import modelformset_factory, formset_factory
# from django.core.exceptions import ValidationError
from django.contrib import messages

from .models import *
from .forms import CreateAuctionForm,  KorisnikCreationForm, AddValuesForm, PonudaForm, OcenjivanjeForm

from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.


def home_view(request, idkategorija=''):
	aukcijeAll = Aukcija.objects.all()
	aukcije=set()
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	if(idkategorija!=''):
		kategorija=Kategorija.objects.get(idkategorija=idkategorija)
	else:
		kategorija=None
	for a in aukcijeAll:
		if (a.datumisteka < (timezone.now() + timezone.timedelta(hours=2))):
			a.aktivna = False
			a.save()
			if(len(a.ponuda_set.all())!=0):
				try:
					prodaja=Prodaja.objects.get(idaukcije=a)
				except Exception as e:
					prodaja=Prodaja(idaukcije=a)
					prodaja.krajnjacena=a.aktuelnaponuda
					prodaja.datum= a.datumisteka
					prodaja.idkupca=a.ponuda_set.all()[len(a.ponuda_set.all())-1].korisnik
					prodaja.save()

		if (kategorija):
			if(kategorija in a.kategorije.all()):
				aukcije.add(a)
	context={
		'aukcije': aukcije,
		'kategorije':kategorije,
		'kategorija':kategorija,
		'aukcijeAll':aukcijeAll,
		
	}
	return render(request, "home.html", context)
	

@login_required(login_url='login')
def create_auction_view(request):
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	if(request.method == 'POST'):
		korisnik = Korisnik.objects.get(username = request.user.username)
		form= CreateAuctionForm(request.POST or None)
		if form.is_valid():
			print(form.cleaned_data)
			aukcija= form.save(commit=False)
			aukcija.idprodavca=korisnik
			aukcija.save()
			form.save_m2m()
			return redirect('add_photos', idaukcije=aukcija.idaukcije)
		else:
			print (form.errors)
	else:
		form = CreateAuctionForm()
	context = {
    	'form': form,
    	'kategorije':kategorije,
	}
	return render(request, "aukcije/create_auction.html", context)

@login_required(login_url='create_auction')
def addPhotos_view(request, idaukcije):
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	aukcija = get_object_or_404(Aukcija, idaukcije=idaukcije)
	kategorijeA = aukcija.kategorije.all()
	osobine = set()
	for kat in kategorijeA:
		for osobina in kat.osobine.all():
			osobine.add(osobina)
	ValuesFormset=formset_factory(form=AddValuesForm, extra=len(osobine))
	formset1=ValuesFormset(request.GET or None)
	for (form, osobina) in zip(formset1, osobine):
		form.fields['value'].queryset = PonudjeneVrednosti.objects.filter(idosobine_id=osobina.idosobina)
	PhotoFormset = modelformset_factory(Slika, fields=('slika',), extra=5)
	if(request.method=='POST'):
		instance=OdabraneVrednostiPredmeta.objects.create(aukcija=aukcija)
		formset=PhotoFormset(request.POST or None, request.FILES or None)
		formset1=ValuesFormset(request.POST or None)
		if(formset.is_valid() and formset1.is_valid()):
			for form in formset:
				try:
					slika = Slika(idaukcije=aukcija, slika=form.cleaned_data['slika'])
					slika.save()
				except Exception as e:
					break
			for form in formset1:
				try:
					value=form.cleaned_data['value']
					instance.pv.add(value)
					
				except Exception as e:
					break
			return redirect("home")		
		else:
			print(formset.errors, formset1.errors)
	formset=PhotoFormset(queryset=Slika.objects.none())
	context = {
		'formset' : formset,
		'osobine' : osobine,
		'kategorije':kategorije,
		'formset1' : formset1,
		'list' : zip(osobine, formset1)
	}
	return render(request, "aukcije/add_photos.html", context)

class SignUpView(CreateView):
    form_class = KorisnikCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def auctionDetail_view(request, idaukcije):
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	ovp = get_object_or_404(OdabraneVrednostiPredmeta, aukcija_id=idaukcije)
	vreme = ovp.aukcija.datumisteka-timezone.now()- timezone.timedelta(hours=2)
	vreme= vreme-timezone.timedelta(microseconds=vreme.microseconds)
	time=""
	sek = vreme.total_seconds()
	if sek > 86400: # 60sec * 60min * 24hrs
		dani = sek // 86400
		time += "{} dana".format(int(dani))
		sek = sek - dani*86400
	if sek > 3600:
		sati = sek // 3600
		time += " {} sati".format(int(sati))
		sek = sek - sati*3600
	if sek > 60:
		mins = sek // 60
		time += " {} minuta".format(int(mins))
		sek = sek - mins*60
	if sek > 0:
		time += " {} sekundi".format(int(sek))

	if (vreme<timezone.timedelta(days=0, hours=0, minutes=0, seconds=0, microseconds=0)):
			ovp.aukcija.aktivna = False
			ovp.aukcija.save()
			if(len(ovp.aukcija.ponuda_set.all())!=0):
				try:
					prodaja=Prodaja.objects.get(idaukcije=a)
				except Exception as e:
					prodaja=Prodaja(idaukcije=ovp.aukcija)
					prodaja.krajnjacena=ovp.aukcija.ponuda_set.all()[len(ovp.aukcija.ponuda_set.all())-1].cena
					prodaja.datum= ovp.aukcija.datumisteka
					prodaja.idkupca=ovp.aukcija.ponuda_set.all()[len(ovp.aukcija.ponuda_set.all())-1].korisnik
					prodaja.save()

	if(request.method=='POST' and request.user):
		korisnik =Korisnik.objects.get(username=request.user.username)
		form=PonudaForm(request.POST or None)
		if(form.is_valid() and len(ovp.aukcija.ponuda_set.all())==0 and form.cleaned_data['cena']>=ovp.aukcija.aktuelnaponuda+10):
			ponuda=form.save(commit=False)
			ponuda.korisnik=korisnik
			ponuda.aukcija=ovp.aukcija
			ponuda.save()
			ovp.aukcija.aktuelnaponuda+=10
			ovp.aukcija.save()
		elif form.is_valid() and form.cleaned_data['cena'] >= ovp.aukcija.ponuda_set.all()[len(ovp.aukcija.ponuda_set.all())-1].cena+10:
			ponuda=form.save(commit=False)
			ponuda.korisnik=korisnik
			ponuda.aukcija=ovp.aukcija
			ponuda.save()
			ovp.aukcija.aktuelnaponuda=ovp.aukcija.ponuda_set.all()[len(ovp.aukcija.ponuda_set.all())-2].cena+10
			ovp.aukcija.save()
		else:
			messages.warning(request, 'Cena mora biti veca od trenutne ponude')
				
	form = PonudaForm()
	form.fields['cena'].initial=ovp.aukcija.aktuelnaponuda + 10
	
	context={
		'aukcija': ovp.aukcija,
		'vrednosti': ovp.pv,
		'vreme': time,
		'kategorije':kategorije,
		'form' :form,
		'slike': ovp.aukcija.slika_set.all(),
	}
	return render(request, "aukcije/auction-details.html", context)

@login_required
def add_to_wishlist(request,idaukcije):
	korisnik=Korisnik.objects.get(username=request.user.username)
	aukcija=get_object_or_404(Aukcija, idaukcije=idaukcije)
	korisnik.lista_zelja.add(aukcija)
	korisnik.save()
	print(korisnik.lista_zelja.all())
	messages.success(request, "Dodato u listu zelja")
	return redirect('auction-details', idaukcije=idaukcije)

@login_required
def show_wishlist_view(request):
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	korisnik=get_object_or_404(Korisnik,username=request.user.username)
	lista_zelja=korisnik.lista_zelja.all()
	print(lista_zelja)
	context={
		'lista_zelja':lista_zelja,
		'kategorije':kategorije,
	}
	return render(request, "aukcije/show_wishlist.html", context)

@login_required
def delete_from_wishlist(request, idaukcije):
	korisnik=get_object_or_404(Korisnik, username=request.user.username)
	aukcija=Aukcija.objects.get(idaukcije=idaukcije)
	korisnik.lista_zelja.remove(aukcija)
	korisnik.save()
	return redirect('show_wishlist')

@login_required
def bought_list_view(request):
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	aukcije = Aukcija.objects.all()
	for a in aukcije:
		if (a.datumisteka < (timezone.now() + timezone.timedelta(hours=2))):
			a.aktivna = False
			a.save()
			if(len(a.ponuda_set.all())!=0):
				try:
					prodaja=Prodaja.objects.get(idaukcije=a)
				except Exception as e:
					prodaja=Prodaja(idaukcije=a)
					prodaja.krajnjacena=a.aktuelnaponuda
					prodaja.datum= a.datumisteka
					prodaja.idkupca=a.ponuda_set.all()[len(a.ponuda_set.all())-1].korisnik
					prodaja.save()

	korisnik=request.user
	prodaje=Prodaja.objects.filter(idkupca=korisnik)
	ocene=list()
	for p in prodaje:
		ocena=Ocena.objects.filter(prodaja=p, ocenjivac=request.user)
		if(ocena):
			ocene.append(ocena[0])
		else:
			ocene.append(None)
	print(ocene)
	context={
		'prodaje':prodaje,
		'lista':zip(prodaje,ocene),
		'kategorije':kategorije,
	}
	return render(request, "aukcije/bought_list.html", context)

@login_required
def sold_list_view(request):
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	aukcije = Aukcija.objects.all()
	for a in aukcije:
		if (a.datumisteka < (timezone.now() + timezone.timedelta(hours=2))):
			a.aktivna = False
			a.save()
			if(len(a.ponuda_set.all())!=0):
				try:
					prodaja=Prodaja.objects.get(idaukcije=a)
				except Exception as e:
					prodaja=Prodaja(idaukcije=a)
					prodaja.krajnjacena=a.aktuelnaponuda
					prodaja.datum= a.datumisteka
					prodaja.idkupca=a.ponuda_set.all()[len(a.ponuda_set.all())-1].korisnik
					prodaja.save()
	aukcija=Aukcija.objects.filter(idprodavca=request.user)
	prodaje=Prodaja.objects.filter(idaukcije__in=aukcija)
	ocene=list()
	for p in prodaje:
		ocena=Ocena.objects.filter(prodaja=p, ocenjivac=request.user)
		if(ocena):
			ocene.append(ocena[0])
		else:
			ocene.append(None)
	context={
		'prodaje':prodaje,
		'kategorije':kategorije,
		'list':zip(prodaje,ocene)
	}
	return render(request, "aukcije/sold_list.html",context)

@login_required
def ocenjivanje_view(request, idprodaja):
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	prodaja = Prodaja.objects.get(pk=idprodaja)
	form=OcenjivanjeForm()
	if request.user==prodaja.idkupca:
		korisnik="prodavca "+prodaja.idaukcije.idprodavca.username
	elif request.user==prodaja.idaukcije.idprodavca:
		korisnik="kupca "+prodaja.idkupca.username
	if(request.method=='POST' and request.user):
		form=OcenjivanjeForm(request.POST or None)
		if(form.is_valid()):
			print(form.cleaned_data)
			ocena=form.save(commit=False)
			ocena.prodaja=prodaja
			ocena.ocenjivac=request.user
			if request.user==prodaja.idkupca:
				ocena.ocenio='kupac'
				ocena.ocenjeni=prodaja.idaukcije.idprodavca
				ocena.save()
				return redirect('bought_list')
			elif request.user==prodaja.idaukcije.idprodavca:
				ocena.ocenio='prodavac'
				ocena.ocenjeni=prodaja.idkupca
				ocena.save()
				return redirect('sold_list')
				
	context={

		'form':form,
		'korisnik':korisnik,
		'kategorije':kategorije,
	}
	return render(request, "aukcije/ocenjivanje.html", context)

def prikaz_korisnika_view(request, idkorisnika):
	kategorije = Kategorija.objects.filter(idnadkategorije=None)
	korisnik=Korisnik.objects.get(pk=idkorisnika)
	ocene=Ocena.objects.filter(ocenjeni=korisnik)
	pozitivne=Ocena.objects.filter(ocenjeni=korisnik,ocena='pozitivna')
	print(korisnik)
	print(pozitivne)
	context={
		'korisnik':korisnik,
		'pozitivne':pozitivne,
		'ocene':ocene,
		'kategorije':kategorije,
	}
	return render(request, "aukcije/prikaz_korisnika.html", context)

@login_required
def kupi_odmah_view(request, idaukcije):
	aukcija=get_object_or_404(Aukcija, idaukcije=idaukcije)
	aukcija.aktivna=False
	aukcija.save()
	prodaja=Prodaja(idaukcije=aukcija, idkupca=request.user, krajnjacena=aukcija.kupiodmahcena)
	prodaja.datum+=timezone.timedelta(hours=2)
	prodaja.save()
	return redirect('auction-details', idaukcije)