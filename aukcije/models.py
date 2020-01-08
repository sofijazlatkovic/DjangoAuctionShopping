from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils import timezone
import os
# Create your models here.


class Korisnik(AbstractUser):
    adresa = models.CharField(max_length=45)
    grad = models.CharField(max_length=45)
    opstina = models.CharField(max_length=45)
    drzava = models.CharField(max_length=45)
    telefon = models.CharField(max_length=45)
    lista_zelja = models.ManyToManyField('Aukcija', related_name='lista_zelja', blank=True, verbose_name="Lista zelja")

    def __str__(self):
        return self.username

class Aukcija(models.Model):
    idaukcije = models.AutoField(db_column='idAukcije', primary_key=True)  # Field name made lowercase.
    nazivpredmeta = models.CharField(db_column='nazivPredmeta', max_length=45, verbose_name="Naziv predmeta")  # Field name made lowercase.
    datumpocetka = models.DateTimeField(db_column='datumPocetka', verbose_name="Datum pocetka", auto_now_add=True)  # Field name made lowercase.
    datumisteka = models.DateTimeField(db_column='datumIsteka', verbose_name="Datum isteka")  # Field name made lowercase.
    aktuelnaponuda = models.PositiveIntegerField(db_column='aktuelnaPonuda', verbose_name="Aktuelna ponuda")  # Field name made lowercase.
    kupiodmah = models.BooleanField(db_column='kupiOdmah', verbose_name="Kupi odmah")  # Field name made lowercase.
    kupiodmahcena = models.PositiveIntegerField(db_column='kupiOdmahCena', blank=True, null=True, verbose_name="Kupi odmah cena") 
    opispredmeta = models.TextField(db_column='opisPredmeta', max_length=200, blank=True, null=True, verbose_name="Opis predmeta")
    aktivna = models.BooleanField(default=True)
    idprodavca = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='idProdavca', verbose_name="Prodavac")
    proizvodjac = models.CharField(max_length=45, blank=True, null=True)
    kategorije = models.ManyToManyField('Kategorija')

    def __str__(self):
        return self.nazivpredmeta

class Kategorija(models.Model):
    idkategorija = models.AutoField(db_column='idKategorija', primary_key=True)  # Field name made lowercase.
    naziv = models.CharField(max_length=45)
    idnadkategorije = models.ForeignKey('self', models.DO_NOTHING, db_column='idNadKategorije', blank=True, null=True, verbose_name="Nadkategorija")  # Field name made lowercase.
    osobine = models.ManyToManyField('Osobina', blank=True)

    def __str__(self):
        return self.naziv

class Osobina(models.Model):
    idosobina = models.AutoField(db_column='idOsobina', primary_key=True)  # Field name made lowercase.
    nazivosobine = models.CharField(db_column='nazivOsobine', max_length=45, verbose_name="Naziv osobine")  # Field name made lowercase.

    def __str__(self):
        return self.nazivosobine

class PonudjeneVrednosti(models.Model):
    idponudjenevrednosti = models.AutoField(db_column='idPonudjeneVrednosti', primary_key=True)
    idosobine = models.ForeignKey(Osobina, models.CASCADE, db_column='idOsobine', verbose_name="Osobina")
    vrednost = models.CharField(max_length=45, verbose_name="Ponudjena vrednost")

    def __str__(self):
        return "%s, %s" % (self.idosobine.nazivosobine, self.vrednost)

    class Meta:
        unique_together = (('idponudjenevrednosti', 'idosobine'),)

class Slika(models.Model):
    def user_directory_path(instance, filename):
        return os.path.join("slike/aukcija_%d" % instance.idaukcije.idaukcije, filename)


    idslika = models.AutoField(db_column='idSlika', primary_key=True)
    idaukcije = models.ForeignKey(Aukcija, models.CASCADE, db_column='idAukcije', verbose_name="Aukcija", blank=False)
    slika = models.ImageField(upload_to=user_directory_path)
    

    def pathslike(self):
        return "slike/%d" % self.idaukcija.idaukcije

    class Meta:
        unique_together = (('idslika', 'idaukcije'),)

class Prodaja(models.Model):
    idaukcije = models.OneToOneField(Aukcija, models.DO_NOTHING, db_column='idAukcije', primary_key=True, verbose_name="Aukcija")
    idkupca = models.ForeignKey(Korisnik, models.DO_NOTHING, related_name='kupac' ,db_column='idKupca', verbose_name="Kupac")
    krajnjacena = models.PositiveIntegerField(db_column='krajnjaCena', verbose_name="Krajnja cena")
    datum = models.DateTimeField(db_column='datumProdaje', verbose_name="Datum prodaje", default=timezone.now)
    def __str__(self):
        return self.idaukcije.nazivpredmeta

class Ponuda(models.Model):
    def getCena(self):
        return self.aukcija.aktuelnaponuda

    aukcija = models.ForeignKey(Aukcija, models.DO_NOTHING, db_column='idAukcije', verbose_name="Aukcija")
    korisnik = models.ForeignKey(Korisnik, models.DO_NOTHING, db_column='idKorisnik', verbose_name="Korisnik")
    cena = models.PositiveIntegerField()
    datum = models.DateTimeField(db_column='datumPonude', verbose_name="Datum ponude", auto_now_add=True)

    def __str__(self):
        return "%s , %s" % (self.aukcija.nazivpredmeta, self.korisnik.username)

class Ocena(models.Model):
    prodaja = models.ForeignKey(Prodaja, models.DO_NOTHING, db_column='idAukcija', verbose_name="Aukcija")
    ocena = models.CharField(max_length=10)
    komentar = models.CharField(max_length=45)
    datum = models.DateTimeField(auto_now_add=True)
    ocenio = models.CharField(max_length=10)
    ocenjivac = models.ForeignKey(Korisnik, models.DO_NOTHING, related_name='ocenjivac',db_column='idOcenjivac', verbose_name="Ocenjivac")  
    ocenjeni = models.ForeignKey(Korisnik, models.DO_NOTHING, related_name='ocenjeni',db_column='idOcenjenog', verbose_name="Ocenjeni") 
    
    def __str__(self):
        return self.prodaja.idaukcije.nazivpredmeta

    class Meta:
        unique_together = (('prodaja', 'ocenjivac', 'ocenjeni'),)


class OdabraneVrednostiPredmeta(models.Model):
    pv = models.ManyToManyField(PonudjeneVrednosti, verbose_name="Ponudjena vrednost")
    aukcija = models.OneToOneField(Aukcija, models.CASCADE, db_column='idAukcije', verbose_name="Aukcija")
    
    def __str__(self):
        return "%s" % (self.aukcija.nazivpredmeta)


