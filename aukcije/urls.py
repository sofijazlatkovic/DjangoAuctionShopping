from django.urls import path

from aukcije.views import (
	home_view,
	create_auction_view,
	addPhotos_view,
	SignUpView,
	auctionDetail_view,
	add_to_wishlist,
	show_wishlist_view,
	delete_from_wishlist,
	bought_list_view,
	sold_list_view,
	ocenjivanje_view,
	prikaz_korisnika_view,
	kupi_odmah_view,
	# AukcijeList,
	  )

# app_name='aukcije'

urlpatterns = [
    # path('', home_view, name='home'),
    # path('aukcije_list/', AukcijeList.as_view()),
    path('create_auction/', create_auction_view, name='create_auction'),
    path('add_photos/<int:idaukcije>/', addPhotos_view, name='add_photos'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('auction-details/<int:idaukcije>/', auctionDetail_view, name='auction-details'),
    path('add_to_wishlist/<int:idaukcije>/', add_to_wishlist, name='add_to_wishlist'),
    path('show_wishlist/', show_wishlist_view, name='show_wishlist'),
    path('delete_from_wishlist/<int:idaukcije>/', delete_from_wishlist, name='delete_from_wishlist'),
    path('bought_list/', bought_list_view, name='bought_list'),
    path('sold_list/', sold_list_view, name='sold_list'),
    path('ocenjivanje/<int:idprodaja>/', ocenjivanje_view, name='ocenjivanje'),
    path('prikaz_korisnika/<int:idkorisnika>/', prikaz_korisnika_view, name='prikaz_korisnika'),
    path('kupi_odmah/<int:idaukcije>/', kupi_odmah_view, name='kupi_odmah'),
    
]
