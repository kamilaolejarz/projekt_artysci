from tkinter import *
from tkinter import ttk
import tkintermapview
import requests
from bs4 import BeautifulSoup

# Dane globalne
artists, events, employees = [], [], []
current_markers = []

# ===== MAPA FUNKCJE =====
def clear_map():
    for marker in current_markers:
        marker.delete()
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
        current_markers.append(map_widget.set_marker(e.coordinates[0], e.coordinates[1], text=f"{e.name} {e.surname} ({e.role})"))

def show_artists_for_event():
    clear_map()
    selected_event = combobox_events.get()
    for a in artists:
        if a.event_name == selected_event:
            current_markers.append(map_widget.set_marker(a.coordinates[0], a.coordinates[1], text=f"{a.name} {a.surname}"))

def show_employees_for_event():
    clear_map()
    selected_event = combobox_events.get()
    for e in employees:
        if e.event_name == selected_event:
            current_markers.append(map_widget.set_marker(e.coordinates[0], e.coordinates[1], text=f"{e.name} {e.surname} ({e.role})"))

# GUI
root = Tk()
root.geometry("1600x1000")
root.title("System Wydarzeń Kulturalnych")
root.grid_rowconfigure(3, weight=1)  # mapa rozszerza się do dołu
root.grid_columnconfigure(0, weight=1)

# Tytuł główny
Label(root, text="System Wydarzeń Kulturalnych", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=1, pady=(10, 0))

# FORMULARZE + PRZYCISKI W JEDNEJ LINII
frame_all_top = Frame(root)
frame_all_top.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
frame_all_top.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

# Wydarzenia
frame_event = Frame(frame_all_top)
frame_event.grid(row=0, column=0, columnspan=2, sticky="w", padx=10)
Label(frame_event, text="Dodaj wydarzenie").grid(row=0, column=0, columnspan=2)
Label(frame_event, text="Nazwa").grid(row=1, column=0)
entry_event_name = Entry(frame_event)
entry_event_name.grid(row=1, column=1)
Label(frame_event, text="Lokalizacja").grid(row=2, column=0)
entry_event_location = Entry(frame_event)
entry_event_location.grid(row=2, column=1)
Button(frame_event, text="Dodaj", command=lambda: print("Dodaj wydarzenie"), width=12).grid(row=1, column=2, padx=5)
Button(frame_event, text="Edytuj", command=lambda: print("Edytuj wydarzenie"), width=12).grid(row=2, column=2, padx=5)
Button(frame_event, text="Usuń", command=lambda: print("Usuń wydarzenie"), width=12).grid(row=3, column=2, padx=5)

# Artyści
frame_artist = Frame(frame_all_top)
frame_artist.grid(row=0, column=2, columnspan=2, sticky="n", padx=10)
Label(frame_artist, text="Dodaj artystę").grid(row=0, column=0, columnspan=2)
Label(frame_artist, text="Imię").grid(row=1, column=0)
entry_artist_name = Entry(frame_artist)
entry_artist_name.grid(row=1, column=1)
Label(frame_artist, text="Nazwisko").grid(row=2, column=0)
entry_artist_surname = Entry(frame_artist)
entry_artist_surname.grid(row=2, column=1)
Label(frame_artist, text="Lokalizacja").grid(row=3, column=0)
entry_artist_location = Entry(frame_artist)
entry_artist_location.grid(row=3, column=1)
Label(frame_artist, text="Opis/Posts").grid(row=4, column=0)
entry_artist_posts = Entry(frame_artist)
entry_artist_posts.grid(row=4, column=1)
Label(frame_artist, text="Wydarzenie").grid(row=5, column=0)
combobox_event_artist = ttk.Combobox(frame_artist, values=[], state="readonly")
combobox_event_artist.grid(row=5, column=1)
Button(frame_artist, text="Dodaj", command=lambda: print("Dodaj artystę"), width=12).grid(row=1, column=2, padx=5)
Button(frame_artist, text="Edytuj", command=lambda: print("Edytuj artystę"), width=12).grid(row=2, column=2, padx=5)
Button(frame_artist, text="Usuń", command=lambda: print("Usuń artystę"), width=12).grid(row=3, column=2, padx=5)

# Pracownicy
frame_employee = Frame(frame_all_top)
frame_employee.grid(row=0, column=4, columnspan=2, sticky="e", padx=10)
Label(frame_employee, text="Dodaj pracownika").grid(row=0, column=0, columnspan=2)
Label(frame_employee, text="Imię").grid(row=1, column=0)
entry_emp_name = Entry(frame_employee)
entry_emp_name.grid(row=1, column=1)
Label(frame_employee, text="Nazwisko").grid(row=2, column=0)
entry_emp_surname = Entry(frame_employee)
entry_emp_surname.grid(row=2, column=1)
Label(frame_employee, text="Rola").grid(row=3, column=0)
entry_emp_role = Entry(frame_employee)
entry_emp_role.grid(row=3, column=1)
Label(frame_employee, text="Lokalizacja").grid(row=4, column=0)
entry_emp_location = Entry(frame_employee)
entry_emp_location.grid(row=4, column=1)
Label(frame_employee, text="Wydarzenie").grid(row=5, column=0)
combobox_event_emp = ttk.Combobox(frame_employee, values=[], state="readonly")
combobox_event_emp.grid(row=5, column=1)
Button(frame_employee, text="Dodaj", command=lambda: print("Dodaj pracownika"), width=12).grid(row=1, column=2, padx=5)
Button(frame_employee, text="Edytuj", command=lambda: print("Edytuj pracownika"), width=12).grid(row=2, column=2, padx=5)
Button(frame_employee, text="Usuń", command=lambda: print("Usuń pracownika"), width=12).grid(row=3, column=2, padx=5)

# NAVIGATION BAR (pod formularzami, w jednej linii)
frame_nav = Frame(root)
frame_nav.grid(row=2, column=0, sticky="ew", pady=(0, 5), padx=10)
frame_nav.grid_columnconfigure((0,1,2,3,4,5), weight=1)
Button(frame_nav, text="Pokaż wydarzenia", command=show_all_events).grid(row=0, column=0, padx=5, pady=5)
Button(frame_nav, text="Pokaż artystów", command=show_all_artists).grid(row=0, column=1, padx=5, pady=5)
Button(frame_nav, text="Pokaż pracowników", command=show_all_employees).grid(row=0, column=2, padx=5, pady=5)
Label(frame_nav, text="Wybierz wydarzenie:").grid(row=0, column=3, padx=5, sticky="e")
combobox_events = ttk.Combobox(frame_nav, values=[], state="readonly")
combobox_events.grid(row=0, column=4, sticky="w")
Button(frame_nav, text="Mapa artystów wydarzenia", command=show_artists_for_event).grid(row=0, column=5, padx=5, pady=5)
Button(frame_nav, text="Mapa pracowników wydarzenia", command=show_employees_for_event).grid(row=0, column=6, padx=5, pady=5)

# MAPA (rozszerzona do dołu)
frame_map = Frame(root)
frame_map.grid(row=3, column=0, sticky="nsew")
map_widget = tkintermapview.TkinterMapView(frame_map, width=1500, height=400, corner_radius=0)
map_widget.pack(fill="both", expand=True)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)

root.mainloop()
