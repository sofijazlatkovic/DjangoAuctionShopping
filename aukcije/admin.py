from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import KorisnikCreationForm, KorisnikChangeForm

class KorisnikAdmin(UserAdmin):
    add_form = KorisnikCreationForm
    form = KorisnikChangeForm
    model = Korisnik
    fieldsets=UserAdmin.fieldsets + (
        (None, {
            'fields': ('grad','drzava','telefon','adresa', 'lista_zelja'),
        }),
    )
    
admin.site.register(Korisnik, KorisnikAdmin)
admin.site.register(Kategorija)
admin.site.register(Osobina)
admin.site.register(PonudjeneVrednosti)
