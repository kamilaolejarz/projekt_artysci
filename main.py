from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

artists: list = []

class Artist:
    def __init__(self, name, surname, location, posts):
        self.name = name
        self.surname = surname
        self.location = location
        self.posts = posts
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f'{self.name} {self.surname}')

    def get_coordinates(self) -> list:
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        response_html = BeautifulSoup(requests.get(adres_url).text, "html.parser")
        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]

def add_artist() -> None:
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    location = entry_miejscowosc.get()
    posts = entry_posts.get()

    artist = Artist(name=name, surname=surname, location=location, posts=posts)
    artists.append(artist)
    map_widget.set_marker(artist.coordinates[0], artist.coordinates[1], text=f"{name} {surname}")
    print(artists)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_posts.delete(0, END)

    entry_imie.focus()
    show_artists()

def show_artists() -> None:
    listbox_lista_obiektow.delete(0, END)
    for idx, artist in enumerate(artists):
        listbox_lista_obiektow.insert(idx, f'{idx + 1}. {artist.name} {artist.surname}')

def remove_artist() -> None:
    i = listbox_lista_obiektow.index(ACTIVE)
    artists[i].marker.delete()
    artists.pop(i)
    show_artists()

def edit_artist() -> None:
    i = listbox_lista_obiektow.index(ACTIVE)
    name = artists[i].name
    surname = artists[i].surname
    location = artists[i].location
    posts = artists[i].posts

    entry_imie.insert(0, name)
    entry_nazwisko.insert(0, surname)
    entry_miejscowosc.insert(0, location)
    entry_posts.insert(0, posts)

    button_dodaj_objekt.config(text='Zapisz', command=lambda: update_artist(i))

def update_artist(i) -> None:
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    location = entry_miejscowosc.get()
    posts = entry_posts.get()

    artists[i].name = name
    artists[i].surname = surname
    artists[i].location = location
    artists[i].posts = posts

    artists[i].coordinates = artists[i].get_coordinates()
    artists[i].marker.delete()
    artists[i].marker = map_widget.set_marker(artists[i].coordinates[0], artists[i].coordinates[1],
                                              text=f'{artists[i].name} {artists[i].surname}')

    show_artists()
    button_dodaj_objekt.config(text='Dodaj', command=add_artist)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_posts.delete(0, END)
    entry_imie.focus()

def show_artist_details() -> None:
    i = listbox_lista_obiektow.index(ACTIVE)
    label_szczegoly_obiektu_name_wartosc.config(text=artists[i].name)
    label_szczegoly_obiektu_surname_wartosc.config(text=artists[i].surname)
    label_szczegoly_obiektu_miejscowosc_wartosc.config(text=artists[i].location)
    label_szczegoly_obiektu_posts_wartosc.config(text=artists[i].posts)

    map_widget.set_zoom(15)
    map_widget.set_position(artists[i].coordinates[0], artists[i].coordinates[1])

root = Tk()
root.geometry("1200x700")
root.title("System Wydarzeń Kulturalnych i Artystów")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

label_lista_obiekow = Label(ramka_lista_obiektow, text="Lista artystów: ")
label_lista_obiekow.grid(row=0, column=0)

listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)

button_pokaz_szczeguly = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_artist_details)
button_pokaz_szczeguly.grid(row=2, column=0)
button_usun_obiekt = Button(ramka_lista_obiektow, text='Usuń', command=remove_artist)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text='Edytuj', command=edit_artist)
button_edytuj_obiekt.grid(row=2, column=2)

label_formularz = Label(ramka_formularz, text="Formularz: ")
label_formularz.grid(row=0, column=0)

label_imie = Label(ramka_formularz, text="Imie: ")
label_imie.grid(row=1, column=0, sticky=W)
label_nazwisko = Label(ramka_formularz, text="Nazwisko: ")
label_nazwisko.grid(row=2, column=0, sticky=W)
label_miejscowosc = Label(ramka_formularz, text="Miejscowość: ")
label_miejscowosc.grid(row=3, column=0, sticky=W)
label_posts = Label(ramka_formularz, text="Opis/Posts: ")
label_posts.grid(row=4, column=0, sticky=W)

entry_imie = Entry(ramka_formularz)
entry_imie.grid(row=1, column=1)
entry_nazwisko = Entry(ramka_formularz)
entry_nazwisko.grid(row=2, column=1)
entry_miejscowosc = Entry(ramka_formularz)
entry_miejscowosc.grid(row=3, column=1)
entry_posts = Entry(ramka_formularz)
entry_posts.grid(row=4, column=1)

button_dodaj_objekt = Button(ramka_formularz, text='Dodaj', command=add_artist)
button_dodaj_objekt.grid(row=5, column=0, columnspan=2)

label_pokaz_szczegoly = Label(ramka_szczegoly_obiektow, text="Szczegóły artysty: ")
label_pokaz_szczegoly.grid(row=0, column=0)

label_szczegoly_obiektu_name = Label(ramka_szczegoly_obiektow, text='Imię: ')
label_szczegoly_obiektu_name.grid(row=1, column=0)
label_szczegoly_obiektu_name_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_name_wartosc.grid(row=1, column=1)
label_szczegoly_obiektu_surname = Label(ramka_szczegoly_obiektow, text='Nazwisko: ')
label_szczegoly_obiektu_surname.grid(row=1, column=2)
label_szczegoly_obiektu_surname_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_surname_wartosc.grid(row=1, column=3)
label_szczegoly_obiektu_miejscowosc = Label(ramka_szczegoly_obiektow, text='Miejscowość: ')
label_szczegoly_obiektu_miejscowosc.grid(row=1, column=4)
label_szczegoly_obiektu_miejscowosc_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_miejscowosc_wartosc.grid(row=1, column=5)
label_szczegoly_obiektu_posts = Label(ramka_szczegoly_obiektow, text='Opis/Posts: ')
label_szczegoly_obiektu_posts.grid(row=1, column=6)
label_szczegoly_obiektu_posts_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_posts_wartosc.grid(row=1, column=7)

map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)

root.mainloop()