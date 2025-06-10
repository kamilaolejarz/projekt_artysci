from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

artists, events, employees = [], [], []
current_markers = []
selected_artist_index = None
selected_event_index = None
selected_employee_index = None


class Event:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        url = f'https://pl.wikipedia.org/wiki/{self.location}'
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        return [float(soup.select('.latitude')[1].text.replace(',', '.')),
                float(soup.select('.longitude')[1].text.replace(',', '.'))]


class Artist:
    def __init__(self, name, surname, location, posts):
        self.name, self.surname, self.location, self.posts = name, surname, location, posts
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        url = f'https://pl.wikipedia.org/wiki/{self.location}'
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        return [float(soup.select('.latitude')[1].text.replace(',', '.')),
                float(soup.select('.longitude')[1].text.replace(',', '.'))]


class Employee:
    def __init__(self, name, surname, role, location):
        self.name, self.surname, self.role, self.location = name, surname, role, location
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        url = f'https://pl.wikipedia.org/wiki/{self.location}'
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        return [float(soup.select('.latitude')[1].text.replace(',', '.')),
                float(soup.select('.longitude')[1].text.replace(',', '.'))]


def clear_map():
    for marker in current_markers: marker.delete()
    current_markers.clear()


def show_all_events():
    clear_map()
    for e in events:
        current_markers.append(map_widget.set_marker(e.coordinates[0], e.coordinates[1], text=f"Wydarzenie: {e.name}"))


def show_all_artists():
    clear_map()
    for a in artists:
        current_markers.append(map_widget.set_marker(a.coordinates[0], a.coordinates[1], text=f"{a.name} {a.surname}"))


def show_all_employees():
    clear_map()
    for e in employees:
        current_markers.append(
            map_widget.set_marker(e.coordinates[0], e.coordinates[1], text=f"{e.name} {e.surname} ({e.role})"))


def add_artist():
    a = Artist(entry_artist_name.get(), entry_artist_surname.get(), entry_artist_location.get(),
               entry_artist_posts.get())
    artists.append(a)
    [entry_artist_name.delete(0, END), entry_artist_surname.delete(0, END),
     entry_artist_location.delete(0, END), entry_artist_posts.delete(0, END)]
    show_artists()


def show_artists():
    listbox_artists.delete(0, END)
    for i, a in enumerate(artists): listbox_artists.insert(i, f"{i + 1}. {a.name} {a.surname}")


def remove_artist():
    i = listbox_artists.index(ACTIVE)
    artists.pop(i)
    show_artists()


def edit_artist():
    global selected_artist_index
    selected_artist_index = listbox_artists.index(ACTIVE)
    a = artists[selected_artist_index]
    entry_artist_name.delete(0, END);
    entry_artist_name.insert(0, a.name)
    entry_artist_surname.delete(0, END);
    entry_artist_surname.insert(0, a.surname)
    entry_artist_location.delete(0, END);
    entry_artist_location.insert(0, a.location)
    entry_artist_posts.delete(0, END);
    entry_artist_posts.insert(0, a.posts)
    btn_add_artist.config(text="Zapisz artystę", command=update_artist)


def update_artist():
    a = artists[selected_artist_index]
    a.name, a.surname, a.location, a.posts = entry_artist_name.get(), entry_artist_surname.get(), entry_artist_location.get(), entry_artist_posts.get()
    a.coordinates = a.get_coordinates()
    show_artists()
    btn_add_artist.config(text="Dodaj artystę", command=add_artist)


def add_event():
    e = Event(entry_event_name.get(), entry_event_location.get())
    events.append(e)
    entry_event_name.delete(0, END);
    entry_event_location.delete(0, END)
    show_events()


def show_events():
    listbox_events.delete(0, END)
    for i, e in enumerate(events): listbox_events.insert(i, f"{i + 1}. {e.name}")


def remove_event():
    i = listbox_events.index(ACTIVE)
    events.pop(i)
    show_events()


def edit_event():
    global selected_event_index
    selected_event_index = listbox_events.index(ACTIVE)
    e = events[selected_event_index]
    entry_event_name.delete(0, END);
    entry_event_name.insert(0, e.name)
    entry_event_location.delete(0, END);
    entry_event_location.insert(0, e.location)
    btn_add_event.config(text="Zapisz wydarzenie", command=update_event)


def update_event():
    e = events[selected_event_index]
    e.name, e.location = entry_event_name.get(), entry_event_location.get()
    e.coordinates = e.get_coordinates()
    show_events()
    btn_add_event.config(text="Dodaj wydarzenie", command=add_event)


def add_employee():
    e = Employee(entry_emp_name.get(), entry_emp_surname.get(), entry_emp_role.get(), entry_emp_location.get())
    employees.append(e)
    [entry_emp_name.delete(0, END), entry_emp_surname.delete(0, END), entry_emp_role.delete(0, END),
     entry_emp_location.delete(0, END)]
    show_employees()


def show_employees():
    listbox_employees.delete(0, END)
    for i, e in enumerate(employees): listbox_employees.insert(i, f"{i + 1}. {e.name} {e.surname} ({e.role})")


def remove_employee():
    i = listbox_employees.index(ACTIVE)
    employees.pop(i)
    show_employees()


def edit_employee():
    global selected_employee_index
    selected_employee_index = listbox_employees.index(ACTIVE)
    e = employees[selected_employee_index]
    entry_emp_name.delete(0, END);
    entry_emp_name.insert(0, e.name)
    entry_emp_surname.delete(0, END);
    entry_emp_surname.insert(0, e.surname)
    entry_emp_role.delete(0, END);
    entry_emp_role.insert(0, e.role)
    entry_emp_location.delete(0, END);
    entry_emp_location.insert(0, e.location)
    btn_add_employee.config(text="Zapisz pracownika", command=update_employee)


def update_employee():
    e = employees[selected_employee_index]
    e.name, e.surname, e.role, e.location = entry_emp_name.get(), entry_emp_surname.get(), entry_emp_role.get(), entry_emp_location.get()
    e.coordinates = e.get_coordinates()
    show_employees()
    btn_add_employee.config(text="Dodaj pracownika", command=add_employee)


# GUI

root = Tk()
root.geometry("1600x1000")
root.title("System Wydarzeń Kulturalnych")

# Przełączanie widoków mapy — na górze
frame_buttons = Frame(root)
frame_buttons.grid(row=0, column=0, columnspan=3, pady=10)
Button(frame_buttons, text="Pokaż wydarzenia", command=show_all_events).grid(row=0, column=0, padx=5)
Button(frame_buttons, text="Pokaż artystów", command=show_all_artists).grid(row=0, column=1, padx=5)
Button(frame_buttons, text="Pokaż pracowników", command=show_all_employees).grid(row=0, column=2, padx=5)

# Artyści
frame_artists = Frame(root)
frame_artists.grid(row=1, column=0, padx=10, sticky=N)
Label(frame_artists, text="Lista artystów:").grid(row=0, column=0, columnspan=2)
listbox_artists = Listbox(frame_artists, width=40)
listbox_artists.grid(row=1, column=0, columnspan=2)
Label(frame_artists, text="Imię:").grid(row=2, column=0)
entry_artist_name = Entry(frame_artists)
entry_artist_name.grid(row=2, column=1)
Label(frame_artists, text="Nazwisko:").grid(row=3, column=0)
entry_artist_surname = Entry(frame_artists)
entry_artist_surname.grid(row=3, column=1)
Label(frame_artists, text="Lokalizacja:").grid(row=4, column=0)
entry_artist_location = Entry(frame_artists)
entry_artist_location.grid(row=4, column=1)
Label(frame_artists, text="Opis/Posts:").grid(row=5, column=0)
entry_artist_posts = Entry(frame_artists)
entry_artist_posts.grid(row=5, column=1)
btn_add_artist = Button(frame_artists, text="Dodaj artystę", command=add_artist)
btn_add_artist.grid(row=6, column=0, columnspan=2)
Button(frame_artists, text="Edytuj artystę", command=edit_artist).grid(row=7, column=0, columnspan=2)
Button(frame_artists, text="Usuń artystę", command=remove_artist).grid(row=8, column=0, columnspan=2)

# Wydarzenia
frame_events = Frame(root)
frame_events.grid(row=1, column=1, padx=10, sticky=N)
Label(frame_events, text="Lista wydarzeń:").grid(row=0, column=0, columnspan=2)
listbox_events = Listbox(frame_events, width=40)
listbox_events.grid(row=1, column=0, columnspan=2)
Label(frame_events, text="Nazwa wydarzenia:").grid(row=2, column=0)
entry_event_name = Entry(frame_events)
entry_event_name.grid(row=2, column=1)
Label(frame_events, text="Lokalizacja:").grid(row=3, column=0)
entry_event_location = Entry(frame_events)
entry_event_location.grid(row=3, column=1)
btn_add_event = Button(frame_events, text="Dodaj wydarzenie", command=add_event)
btn_add_event.grid(row=4, column=0, columnspan=2)
Button(frame_events, text="Edytuj wydarzenie", command=edit_event).grid(row=5, column=0, columnspan=2)
Button(frame_events, text="Usuń wydarzenie", command=remove_event).grid(row=6, column=0, columnspan=2)

# Pracownicy
frame_employees = Frame(root)
frame_employees.grid(row=1, column=2, padx=10, sticky=N)
Label(frame_employees, text="Lista pracowników:").grid(row=0, column=0, columnspan=2)
listbox_employees = Listbox(frame_employees, width=40)
listbox_employees.grid(row=1, column=0, columnspan=2)
Label(frame_employees, text="Imię:").grid(row=2, column=0)
entry_emp_name = Entry(frame_employees)
entry_emp_name.grid(row=2, column=1)
Label(frame_employees, text="Nazwisko:").grid(row=3, column=0)
entry_emp_surname = Entry(frame_employees)
entry_emp_surname.grid(row=3, column=1)
Label(frame_employees, text="Rola:").grid(row=4, column=0)
entry_emp_role = Entry(frame_employees)
entry_emp_role.grid(row=4, column=1)
Label(frame_employees, text="Lokalizacja:").grid(row=5, column=0)
entry_emp_location = Entry(frame_employees)
entry_emp_location.grid(row=5, column=1)
btn_add_employee = Button(frame_employees, text="Dodaj pracownika", command=add_employee)
btn_add_employee.grid(row=6, column=0, columnspan=2)
Button(frame_employees, text="Edytuj pracownika", command=edit_employee).grid(row=7, column=0, columnspan=2)
Button(frame_employees, text="Usuń pracownika", command=remove_employee).grid(row=8, column=0, columnspan=2)

# Mapa na dole
frame_map = Frame(root)
frame_map.grid(row=2, column=0, columnspan=3)
map_widget = tkintermapview.TkinterMapView(frame_map, width=1500, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, columnspan=3)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)

root.mainloop()
