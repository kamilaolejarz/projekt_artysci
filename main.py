from tkinter import *
from tkinter import ttk
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
    def __init__(self, name, surname, location, posts, event_name):
        self.name, self.surname, self.location, self.posts, self.event_name = name, surname, location, posts, event_name
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        url = f'https://pl.wikipedia.org/wiki/{self.location}'
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        return [float(soup.select('.latitude')[1].text.replace(',', '.')),
                float(soup.select('.longitude')[1].text.replace(',', '.'))]


class Employee:
    def __init__(self, name, surname, role, location, event_name):
        self.name, self.surname, self.role, self.location, self.event_name = name, surname, role, location, event_name
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


def show_artists_for_event():
    clear_map()
    selected_event = combobox_events.get()
    for a in artists:
        if a.event_name == selected_event:
            current_markers.append(
                map_widget.set_marker(a.coordinates[0], a.coordinates[1], text=f"{a.name} {a.surname}"))


def show_employees_for_event():
    clear_map()
    selected_event = combobox_events.get()
    for e in employees:
        if e.event_name == selected_event:
            current_markers.append(
                map_widget.set_marker(e.coordinates[0], e.coordinates[1], text=f"{e.name} {e.surname} ({e.role})"))


def update_comboboxes():
    event_names = [e.name for e in events]
    combobox_events['values'] = event_names
    combobox_event_artist['values'] = event_names
    combobox_event_emp['values'] = event_names


def clear_artist_form():
    entry_artist_name.delete(0, END)
    entry_artist_surname.delete(0, END)
    entry_artist_location.delete(0, END)
    entry_artist_posts.delete(0, END)
    combobox_event_artist.set('')


def clear_event_form():
    entry_event_name.delete(0, END)
    entry_event_location.delete(0, END)


def clear_employee_form():
    entry_emp_name.delete(0, END)
    entry_emp_surname.delete(0, END)
    entry_emp_role.delete(0, END)
    entry_emp_location.delete(0, END)
    combobox_event_emp.set('')


def show_artists():
    listbox_artists.delete(0, END)
    for i, a in enumerate(artists): listbox_artists.insert(i, f"{i + 1}. {a.name} {a.surname}")


def show_events():
    listbox_events.delete(0, END)
    for i, e in enumerate(events): listbox_events.insert(i, f"{i + 1}. {e.name}")


def show_employees():
    listbox_employees.delete(0, END)
    for i, e in enumerate(employees): listbox_employees.insert(i, f"{i + 1}. {e.name} {e.surname} ({e.role})")


def add_event():
    e = Event(entry_event_name.get(), entry_event_location.get())
    events.append(e)
    clear_event_form()
    update_comboboxes()
    show_events()


def add_artist():
    if combobox_event_artist.get():
        a = Artist(entry_artist_name.get(), entry_artist_surname.get(), entry_artist_location.get(),
                   entry_artist_posts.get(), combobox_event_artist.get())
        artists.append(a)
        clear_artist_form()
        show_artists()


def add_employee():
    if combobox_event_emp.get():
        e = Employee(entry_emp_name.get(), entry_emp_surname.get(), entry_emp_role.get(), entry_emp_location.get(),
                     combobox_event_emp.get())
        employees.append(e)
        clear_employee_form()
        show_employees()


def remove_artist():
    if listbox_artists.curselection():
        i = listbox_artists.curselection()[0]
        artists.pop(i)
        show_artists()
        clear_artist_form()


def remove_event():
    if listbox_events.curselection():
        i = listbox_events.curselection()[0]
        events.pop(i)
        update_comboboxes()
        show_events()
        clear_event_form()


def remove_employee():
    if listbox_employees.curselection():
        i = listbox_employees.curselection()[0]
        employees.pop(i)
        show_employees()
        clear_employee_form()


def edit_artist():
    global selected_artist_index
    if listbox_artists.curselection():
        selected_artist_index = listbox_artists.curselection()[0]
        a = artists[selected_artist_index]
        entry_artist_name.delete(0, END)
        entry_artist_name.insert(0, a.name)
        entry_artist_surname.delete(0, END)
        entry_artist_surname.insert(0, a.surname)
        entry_artist_location.delete(0, END)
        entry_artist_location.insert(0, a.location)
        entry_artist_posts.delete(0, END)
        entry_artist_posts.insert(0, a.posts)
        combobox_event_artist.set(a.event_name)
        btn_add_artist.config(text="Zapisz", command=update_artist)


def update_artist():
    a = artists[selected_artist_index]
    a.name = entry_artist_name.get()
    a.surname = entry_artist_surname.get()
    a.location = entry_artist_location.get()
    a.posts = entry_artist_posts.get()
    a.event_name = combobox_event_artist.get()
    a.coordinates = a.get_coordinates()
    show_artists()
    clear_artist_form()
    btn_add_artist.config(text="Dodaj artystę", command=add_artist)


def edit_event():
    global selected_event_index
    if listbox_events.curselection():
        selected_event_index = listbox_events.curselection()[0]
        e = events[selected_event_index]
        entry_event_name.delete(0, END)
        entry_event_name.insert(0, e.name)
        entry_event_location.delete(0, END)
        entry_event_location.insert(0, e.location)
        btn_add_event.config(text="Zapisz", command=update_event)


def update_event():
    e = events[selected_event_index]
    e.name = entry_event_name.get()
    e.location = entry_event_location.get()
    e.coordinates = e.get_coordinates()
    update_comboboxes()
    show_events()
    clear_event_form()
    btn_add_event.config(text="Dodaj wydarzenie", command=add_event)


def edit_employee():
    global selected_employee_index
    if listbox_employees.curselection():
        selected_employee_index = listbox_employees.curselection()[0]
        e = employees[selected_employee_index]
        entry_emp_name.delete(0, END)
        entry_emp_name.insert(0, e.name)
        entry_emp_surname.delete(0, END)
        entry_emp_surname.insert(0, e.surname)
        entry_emp_role.delete(0, END)
        entry_emp_role.insert(0, e.role)
        entry_emp_location.delete(0, END)
        entry_emp_location.insert(0, e.location)
        combobox_event_emp.set(e.event_name)
        btn_add_employee.config(text="Zapisz", command=update_employee)


def update_employee():
    e = employees[selected_employee_index]
    e.name = entry_emp_name.get()
    e.surname = entry_emp_surname.get()
    e.role = entry_emp_role.get()
    e.location = entry_emp_location.get()
    e.event_name = combobox_event_emp.get()
    e.coordinates = e.get_coordinates()
    show_employees()
    clear_employee_form()
    btn_add_employee.config(text="Dodaj pracownika", command=add_employee)


# GUI
root = Tk()
root.geometry("1600x1000")
root.title("System Wydarzeń Kulturalnych")

Label(root, text="System Wydarzeń Kulturalnych", font=("Helvetica", 24, "bold")).grid(row=0, column=0, columnspan=6,
                                                                                      pady=10)

for i in range(6):
    root.grid_columnconfigure(i, weight=1)

# Wydarzenia
frame_event_list = Frame(root)
frame_event_list.grid(row=1, column=0, padx=5, pady=5)
Label(frame_event_list, text="Lista wydarzeń:").pack()
listbox_events = Listbox(frame_event_list, width=25)
listbox_events.pack()

frame_events = Frame(root)
frame_events.grid(row=1, column=1, padx=5, pady=5)
Label(frame_events, text="Nazwa wydarzenia:").grid(row=0, column=0)
entry_event_name = Entry(frame_events)
entry_event_name.grid(row=0, column=1)
Label(frame_events, text="Lokalizacja:").grid(row=1, column=0)
entry_event_location = Entry(frame_events)
entry_event_location.grid(row=1, column=1)
btn_add_event = Button(frame_events, text="Dodaj wydarzenie", command=add_event)
btn_add_event.grid(row=2, column=0, columnspan=2)
Button(frame_events, text="Edytuj wydarzenie", command=edit_event).grid(row=3, column=0, columnspan=2)
Button(frame_events, text="Usuń wydarzenie", command=remove_event).grid(row=4, column=0, columnspan=2)

# Artyści
frame_artist_list = Frame(root)
frame_artist_list.grid(row=1, column=2, padx=5, pady=5)
Label(frame_artist_list, text="Lista artystów:").pack()
listbox_artists = Listbox(frame_artist_list, width=25)
listbox_artists.pack()

frame_artists = Frame(root)
frame_artists.grid(row=1, column=3, padx=5, pady=5)
Label(frame_artists, text="Imię:").grid(row=0, column=0)
entry_artist_name = Entry(frame_artists)
entry_artist_name.grid(row=0, column=1)
Label(frame_artists, text="Nazwisko:").grid(row=1, column=0)
entry_artist_surname = Entry(frame_artists)
entry_artist_surname.grid(row=1, column=1)
Label(frame_artists, text="Lokalizacja:").grid(row=2, column=0)
entry_artist_location = Entry(frame_artists)
entry_artist_location.grid(row=2, column=1)
Label(frame_artists, text="Opis/Posts:").grid(row=3, column=0)
entry_artist_posts = Entry(frame_artists)
entry_artist_posts.grid(row=3, column=1)
Label(frame_artists, text="Wydarzenie:").grid(row=4, column=0)
combobox_event_artist = ttk.Combobox(frame_artists, values=[], state="readonly")
combobox_event_artist.grid(row=4, column=1)
btn_add_artist = Button(frame_artists, text="Dodaj artystę", command=add_artist)
btn_add_artist.grid(row=5, column=0, columnspan=2)
Button(frame_artists, text="Edytuj artystę", command=edit_artist).grid(row=6, column=0, columnspan=2)
Button(frame_artists, text="Usuń artystę", command=remove_artist).grid(row=7, column=0, columnspan=2)

# Pracownicy
frame_employee_list = Frame(root)
frame_employee_list.grid(row=1, column=4, padx=5, pady=5)
Label(frame_employee_list, text="Lista pracowników:").pack()
listbox_employees = Listbox(frame_employee_list, width=25)
listbox_employees.pack()

frame_employees = Frame(root)
frame_employees.grid(row=1, column=5, padx=5, pady=5)
Label(frame_employees, text="Imię:").grid(row=0, column=0)
entry_emp_name = Entry(frame_employees)
entry_emp_name.grid(row=0, column=1)
Label(frame_employees, text="Nazwisko:").grid(row=1, column=0)
entry_emp_surname = Entry(frame_employees)
entry_emp_surname.grid(row=1, column=1)
Label(frame_employees, text="Rola:").grid(row=2, column=0)
entry_emp_role = Entry(frame_employees)
entry_emp_role.grid(row=2, column=1)
Label(frame_employees, text="Lokalizacja:").grid(row=3, column=0)
entry_emp_location = Entry(frame_employees)
entry_emp_location.grid(row=3, column=1)
Label(frame_employees, text="Wydarzenie:").grid(row=4, column=0)
combobox_event_emp = ttk.Combobox(frame_employees, values=[], state="readonly")
combobox_event_emp.grid(row=4, column=1)
btn_add_employee = Button(frame_employees, text="Dodaj pracownika", command=add_employee)
btn_add_employee.grid(row=5, column=0, columnspan=2)
Button(frame_employees, text="Edytuj pracownika", command=edit_employee).grid(row=6, column=0, columnspan=2)
Button(frame_employees, text="Usuń pracownika", command=remove_employee).grid(row=7, column=0, columnspan=2)

# Funkcjonalność mapy(przyciski)
frame_buttons = Frame(root)
frame_buttons.grid(row=2, column=0, columnspan=2, pady=10)
Button(frame_buttons, text="Pokaż wydarzenia", command=show_all_events).grid(row=0, column=0, padx=5)
Button(frame_buttons, text="Pokaż artystów", command=show_all_artists).grid(row=0, column=1, padx=5)
Button(frame_buttons, text="Pokaż pracowników", command=show_all_employees).grid(row=0, column=2, padx=5)

frame_map_buttons = Frame(root)
frame_map_buttons.grid(row=2, column=3, columnspan=3, pady=10)
Label(frame_map_buttons, text="Wybierz wydarzenie: ").grid(row=0, column=0, padx=5)
combobox_events = ttk.Combobox(frame_map_buttons, values=[], state="readonly")
combobox_events.grid(row=0, column=1)
Button(frame_map_buttons, text="Mapa artystów wydarzenia", command=show_artists_for_event).grid(row=0, column=2, padx=5)
Button(frame_map_buttons, text="Mapa pracowników wydarzenia", command=show_employees_for_event).grid(row=0, column=3,
                                                                                                     padx=5)

frame_map = Frame(root)
frame_map.grid(row=3, column=0, columnspan=6, sticky="nsew")
root.grid_rowconfigure(3, weight=1)
map_widget = tkintermapview.TkinterMapView(frame_map)
map_widget.pack(fill="both", expand=True)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)

root.mainloop()
