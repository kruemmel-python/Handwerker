import sqlite3
import csv
import os
from tkinter import Tk, Label, Entry, Button, messagebox, Frame, Listbox, Scrollbar, Toplevel, END, simpledialog, Menu
from tkcalendar import Calendar, DateEntry
from datetime import datetime, timedelta  # Importiere das datetime-Modul

# --- Datenbank Setup ---
DB_PATH = 'handwerker.db'
CSV_PATH = 'lager.csv'

# Funktion zum Initialisieren der Datenbank
def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabelle Lager erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS lager (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        art_nr TEXT,
                        name TEXT,
                        oberflaeche TEXT,
                        format_in_mm TEXT,
                        staerke_in_mm REAL,
                        artikel_id TEXT,
                        kategorie TEXT,
                        mass TEXT,
                        gewicht REAL,
                        lagerbestand INTEGER,
                        lieferant TEXT,
                        einkaufspreis REAL,
                        verkaufspreis REAL,
                        bestellnummer_lieferant TEXT,
                        mindestbestellmenge INTEGER,
                        maximaler_lagerbestand INTEGER,
                        lieferzeit TEXT,
                        verbrauchseinheit TEXT,
                        verfallsdatum TEXT,
                        lagerort TEXT,
                        produktbild TEXT,
                        sicherheitsdatenblatt TEXT,
                        anwendungsbereich TEXT
                    )''')

    # Tabelle Projektverwaltung erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS projekte (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        projekt_name TEXT,
                        kunde TEXT,
                        mitarbeiter TEXT,
                        startdatum TEXT,
                        enddatum TEXT,
                        beschreibung TEXT
                    )''')
    conn.commit()
    conn.close()

# Funktion zum Importieren der CSV-Daten in die Datenbank
def import_csv_to_db():
    if not os.path.exists(CSV_PATH):
        print("CSV-Datei nicht gefunden.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            cursor.execute('''INSERT INTO lager (art_nr, name, oberflaeche, format_in_mm, staerke_in_mm, artikel_id, kategorie, mass, gewicht, lagerbestand, lieferant, einkaufspreis, verkaufspreis, bestellnummer_lieferant, mindestbestellmenge, maximaler_lagerbestand, lieferzeit, verbrauchseinheit, verfallsdatum, lagerort, produktbild, sicherheitsdatenblatt, anwendungsbereich)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                          (row.get('Art. Nr.', ''),
                           row.get('Name', ''),
                           row.get('Oberfläche', ''),
                           row.get('Format in mm', ''),
                           row.get('Stärke in mm', '0'),  # Standardwert '0'
                           row.get('ArtikelID', ''),
                           row.get('Kategorie', ''),
                           row.get('Maße', ''),
                           row.get('Gewicht', '0'),  # Standardwert '0'
                           row.get('Lagerbestand', 0),
                           row.get('Lieferant', ''),
                           row.get('Einkaufspreis', '0.0'),  # Standardwert '0.0'
                           row.get('Verkaufspreis', '0.0'),  # Standardwert '0.0'
                           row.get('BestellnummerLieferant', ''),
                           row.get('Mindestbestellmenge', 0),
                           row.get('MaximalerLagerbestand', 0),
                           row.get('Lieferzeit', ''),
                           row.get('Verbrauchseinheit', ''),
                           row.get('Verfallsdatum', ''),
                           row.get('Lagerort', ''),
                           row.get('Produktbild', ''),
                           row.get('Sicherheitsdatenblatt', ''),
                           row.get('Anwendungsbereich', '')))

    conn.commit()
    conn.close()

# --- Benutzeranmeldung ---
def login():
    def check_login():
        username = entry_username.get()
        password = entry_password.get()

        # Beispielhafte Benutzer-Validierung (sollte durch Datenbank-Validierung ersetzt werden)
        if username == "admin" and password == "admin":
            messagebox.showinfo("Login erfolgreich", "Willkommen!")
            root.destroy()
            open_main_app()
        else:
            messagebox.showerror("Fehler", "Ungültiger Benutzername oder Passwort")

    root = Tk()
    root.title("Anmeldung")
    Label(root, text="Benutzername").grid(row=0, column=0)
    entry_username = Entry(root)
    entry_username.grid(row=0, column=1)
    Label(root, text="Passwort").grid(row=1, column=0)
    entry_password = Entry(root, show="*")
    entry_password.grid(row=1, column=1)
    Button(root, text="Login", command=check_login).grid(row=2, column=1)
    root.mainloop()

# --- Haupt-GUI ---
def open_main_app():
    def kalender_projekt_details(event):
        selected_date = cal.get_date()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projekte WHERE startdatum <= ? AND enddatum >= ?", (selected_date, selected_date))
        rows = cursor.fetchall()
        conn.close()
        if rows:
            open_projektverwaltung(selected_date)

    def open_lagerverwaltung():
        def artikel_hinzufuegen():
            art_nr = simpledialog.askstring("Artikel hinzufügen", "Art. Nr.:")
            beschreibung = simpledialog.askstring("Artikel hinzufügen", "Beschreibung:")
            lagerbestand = simpledialog.askinteger("Artikel hinzufügen", "Lagerbestand:")
            if art_nr and beschreibung and lagerbestand is not None:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO lager (art_nr, beschreibung, lagerbestand)
                                  VALUES (?, ?, ?)''', (art_nr, beschreibung, lagerbestand))
                conn.commit()
                conn.close()
                messagebox.showinfo("Erfolg", "Artikel hinzugefügt!")
                refresh_lager_list()

        def artikel_entnehmen():
            art_nr = simpledialog.askstring("Artikel entnehmen", "Art. Nr.:")
            menge = simpledialog.askinteger("Artikel entnehmen", "Menge zu entnehmen:")
            if art_nr and menge is not None:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT lagerbestand FROM lager WHERE art_nr = ?", (art_nr,))
                row = cursor.fetchone()
                if row and row[0] >= menge:
                    cursor.execute("UPDATE lager SET lagerbestand = lagerbestand - ? WHERE art_nr = ?", (menge, art_nr))
                    conn.commit()
                    messagebox.showinfo("Erfolg", "Artikel entnommen!")
                else:
                    messagebox.showerror("Fehler", "Nicht genügend Lagerbestand oder Artikel nicht gefunden.")
                conn.close()
                refresh_lager_list()

        def artikel_bestand_bearbeiten():
            art_nr = simpledialog.askstring("Bestand bearbeiten", "Art. Nr.:")
            neuer_bestand = simpledialog.askinteger("Bestand bearbeiten", "Neuer Lagerbestand:")
            if art_nr and neuer_bestand is not None:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("UPDATE lager SET lagerbestand = ? WHERE art_nr = ?", (neuer_bestand, art_nr))
                conn.commit()
                conn.close()
                messagebox.showinfo("Erfolg", "Lagerbestand aktualisiert!")
                refresh_lager_list()

        def artikel_suchen():
            suchbegriff = simpledialog.askstring("Artikel suchen", "Art. Nr. oder Name eingeben:")
            if suchbegriff:
                listbox.delete(0, END)
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT art_nr, name, lagerbestand FROM lager WHERE art_nr LIKE ? OR name LIKE ?", (f"%{suchbegriff}%", f"%{suchbegriff}%"))
                rows = cursor.fetchall()
                conn.close()
                for row in rows:
                    listbox.insert(END, f"Art. Nr.: {row[0]}, Beschreibung: {row[1]}, Lagerbestand: {row[2]}")

        def artikel_details(event):
            selected_item = listbox.get(listbox.curselection())
            art_nr = selected_item.split(',')[0].split(':')[1].strip()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lager WHERE art_nr = ?", (art_nr,))
            row = cursor.fetchone()
            conn.close()
            if row:
                details = f"Art. Nr.: {row[1] if row[1] else 'N/A'}\nName: {row[2] if row[2] else 'N/A'}\nOberfläche: {row[3] if row[3] else 'N/A'}\nFormat: {row[4] if row[4] else 'N/A'}\nStärke: {row[5] if row[5] else 'N/A'}\nKategorie: {row[7] if row[7] else 'N/A'}\nLagerbestand: {row[10] if row[10] else '0'}\nLieferant: {row[11] if row[11] else 'N/A'}\nEinkaufspreis: {row[12] if row[12] else '0.0'}\nVerkaufspreis: {row[13] if row[13] else '0.0'}\nLagerort: {row[20] if row[20] else 'N/A'}"
                messagebox.showinfo("Artikeldetails", details)

        def artikel_bearbeiten():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showerror("Fehler", "Bitte wählen Sie einen Artikel aus der Liste aus.")
                return

            selected_item = listbox.get(selected_indices[0])
            art_nr = selected_item.split(',')[0].split(':')[1].strip()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lager WHERE art_nr = ?", (art_nr,))
            row = cursor.fetchone()
            if row:
                art_nr_neu = simpledialog.askstring("Artikel bearbeiten", "Art. Nr.:", initialvalue=row[1])
                beschreibung_neu = simpledialog.askstring("Artikel bearbeiten", "Name:", initialvalue=row[2])
                lagerbestand_neu = simpledialog.askinteger("Artikel bearbeiten", "Lagerbestand:", initialvalue=row[10])
                if art_nr_neu and beschreibung_neu and lagerbestand_neu is not None:
                    cursor.execute('''UPDATE lager SET art_nr = ?, name = ?, lagerbestand = ? WHERE id = ?''',
                                   (art_nr_neu, beschreibung_neu, lagerbestand_neu, row[0]))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Erfolg", "Artikel aktualisiert!")
                    refresh_lager_list()

        def artikel_loeschen():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showerror("Fehler", "Bitte wählen Sie einen Artikel aus der Liste aus.")
                return

            selected_item = listbox.get(selected_indices[0])
            art_nr = selected_item.split(',')[0].split(':')[1].strip()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM lager WHERE art_nr = ?", (art_nr,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Erfolg", "Artikel gelöscht!")
            refresh_lager_list()

        def refresh_lager_list():
            listbox.delete(0, END)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT art_nr, name FROM lager")
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                listbox.insert(END, f"Art. Nr.: {row[0]}, Name: {row[1]}")

        lager_window = Toplevel(main_app)
        lager_window.title("Lagerverwaltung")

        listbox = Listbox(lager_window, width=100)
        listbox.pack(side="left", fill="y")
        listbox.bind('<Double-1>', artikel_details)

        scrollbar = Scrollbar(lager_window, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side="right", fill="y")

        listbox.config(yscrollcommand=scrollbar.set)

        Button(lager_window, text="Artikel hinzufügen", command=artikel_hinzufuegen).pack(pady=5)
        Button(lager_window, text="Artikel entnehmen", command=artikel_entnehmen).pack(pady=5)
        Button(lager_window, text="Bestand bearbeiten", command=artikel_bestand_bearbeiten).pack(pady=5)
        Button(lager_window, text="Artikel suchen", command=artikel_suchen).pack(pady=5)
        Button(lager_window, text="Artikel bearbeiten", command=artikel_bearbeiten).pack(pady=5)
        Button(lager_window, text="Artikel löschen", command=artikel_loeschen).pack(pady=5)

        refresh_lager_list()

    def open_projektverwaltung(selected_date=None):
        def refresh_projekt_list():
            listbox.delete(0, END)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT projekt_name, kunde, mitarbeiter FROM projekte")
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                listbox.insert(END, f"Projekt: {row[0]}, Kunde: {row[1]}, Mitarbeiter: {row[2]}")

        def projekt_suchen():
            suchbegriff = simpledialog.askstring("Projekt suchen", "Projektname oder Kunde eingeben:")
            if suchbegriff:
                listbox.delete(0, END)
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT projekt_name, kunde, mitarbeiter FROM projekte WHERE projekt_name LIKE ? OR kunde LIKE ?", (f"%{suchbegriff}%", f"%{suchbegriff}%"))
                rows = cursor.fetchall()
                conn.close()
                for row in rows:
                    listbox.insert(END, f"Projekt: {row[0]}, Kunde: {row[1]}, Mitarbeiter: {row[2]}")

        def projekt_details(event):
            selected_item = listbox.get(listbox.curselection())
            projekt_name = selected_item.split(',')[0].split(':')[1].strip()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projekte WHERE projekt_name = ?", (projekt_name,))
            row = cursor.fetchone()
            conn.close()
            if row:
                details = f"Projektname: {row[1]}\nKunde: {row[2]}\nMitarbeiter: {row[3]}\nStartdatum: {row[4]}\nEnddatum: {row[5]}\nBeschreibung: {row[6]}"
                messagebox.showinfo("Projektdetails", details)

        def projekt_aendern():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus der Liste aus.")
                return

            selected_item = listbox.get(selected_indices[0])
            projekt_name = selected_item.split(',')[0].split(':')[1].strip()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projekte WHERE projekt_name = ?", (projekt_name,))
            row = cursor.fetchone()
            if row:
                entry_projektname.delete(0, END)
                entry_projektname.insert(0, row[1])
                entry_kunde.delete(0, END)
                entry_kunde.insert(0, row[2])
                entry_mitarbeiter.delete(0, END)
                entry_mitarbeiter.insert(0, row[3])

                # Konvertiere das Datum vom Format YYYY-MM-DD zu YYYY-MM-DD
                startdatum = datetime.strptime(row[4], '%Y-%m-%d').date()
                enddatum = datetime.strptime(row[5], '%Y-%m-%d').date()

                entry_startdatum.set_date(startdatum)
                entry_enddatum.set_date(enddatum)

                entry_beschreibung.delete(0, END)
                entry_beschreibung.insert(0, row[6])

                def update_projekt():
                    projektname = entry_projektname.get()
                    kunde = entry_kunde.get()
                    mitarbeiter = entry_mitarbeiter.get()
                    startdatum = entry_startdatum.get()
                    enddatum = entry_enddatum.get()
                    beschreibung = entry_beschreibung.get()

                    cursor.execute('''UPDATE projekte SET projekt_name = ?, kunde = ?, mitarbeiter = ?, startdatum = ?, enddatum = ?, beschreibung = ? WHERE id = ?''',
                                   (projektname, kunde, mitarbeiter, startdatum, enddatum, beschreibung, row[0]))
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Erfolg", "Projekt aktualisiert!")
                    projekt_window.destroy()
                    open_projektverwaltung()

                Button(projekt_window, text="Projekt aktualisieren", command=update_projekt).grid(row=9, column=1)
            else:
                messagebox.showerror("Fehler", "Projekt nicht gefunden.")

        def projekt_loeschen():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus der Liste aus.")
                return

            selected_item = listbox.get(selected_indices[0])
            projekt_name = selected_item.split(',')[0].split(':')[1].strip()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT startdatum, enddatum FROM projekte WHERE projekt_name = ?", (projekt_name,))
            row = cursor.fetchone()
            if row:
                startdatum = row[0]
                enddatum = row[1]
                cursor.execute("DELETE FROM projekte WHERE projekt_name = ?", (projekt_name,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Erfolg", "Projekt gelöscht!")
                open_projektverwaltung()

                # Entferne den Kalendereintrag
                cal.calevent_remove(startdatum)
                cal.calevent_remove(enddatum)

        def markiere_projekte_im_kalender():
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT projekt_name, startdatum, enddatum FROM projekte")
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                projekt_name = row[0]
                startdatum = row[1]
                enddatum = row[2]

                # Versuche zuerst das ISO-Format zu konvertieren, dann das deutsche Format
                try:
                    startdatum_obj = datetime.strptime(startdatum, '%Y-%m-%d').date()
                    enddatum_obj = datetime.strptime(enddatum, '%Y-%m-%d').date()
                except ValueError:
                    try:
                        startdatum_obj = datetime.strptime(startdatum, '%d.%m.%Y').date()
                        enddatum_obj = datetime.strptime(enddatum, '%d.%m.%Y').date()
                    except ValueError:
                        messagebox.showerror("Fehler", f"Falsches Datumsformat für Projekt {projekt_name}: {startdatum} oder {enddatum}")
                        continue

                # Erstelle Kalendereinträge für den gesamten Zeitraum
                current_date = startdatum_obj
                while current_date <= enddatum_obj:
                    cal.calevent_create(current_date, projekt_name, 'Projekt')
                    current_date += timedelta(days=1)

        def kalender_projekt_details(event):
            selected_date = cal.get_date()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projekte WHERE startdatum <= ? AND enddatum >= ?", (selected_date, selected_date))
            rows = cursor.fetchall()
            conn.close()
            if rows:
                open_projektverwaltung(selected_date)

        projekt_window = Toplevel(main_app)
        projekt_window.title("Projektverwaltung")

        Label(projekt_window, text="Projektname").grid(row=0, column=0)
        entry_projektname = Entry(projekt_window)
        entry_projektname.grid(row=0, column=1)

        Label(projekt_window, text="Kunde").grid(row=1, column=0)
        entry_kunde = Entry(projekt_window)
        entry_kunde.grid(row=1, column=1)

        Label(projekt_window, text="Mitarbeiter").grid(row=2, column=0)
        entry_mitarbeiter = Entry(projekt_window)
        entry_mitarbeiter.grid(row=2, column=1)

        Label(projekt_window, text="Startdatum").grid(row=3, column=0)
        entry_startdatum = DateEntry(projekt_window, date_pattern='yyyy-mm-dd')
        entry_startdatum.grid(row=3, column=1)

        Label(projekt_window, text="Enddatum").grid(row=4, column=0)
        entry_enddatum = DateEntry(projekt_window, date_pattern='yyyy-mm-dd')
        entry_enddatum.grid(row=4, column=1)

        Label(projekt_window, text="Beschreibung").grid(row=5, column=0)
        entry_beschreibung = Entry(projekt_window)
        entry_beschreibung.grid(row=5, column=1)

        def save_projekt():
            projektname = entry_projektname.get()
            kunde = entry_kunde.get()
            mitarbeiter = entry_mitarbeiter.get()
            startdatum = entry_startdatum.get()
            enddatum = entry_enddatum.get()
            beschreibung = entry_beschreibung.get()

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO projekte (projekt_name, kunde, mitarbeiter, startdatum, enddatum, beschreibung)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (projektname, kunde, mitarbeiter, startdatum, enddatum, beschreibung))
            conn.commit()
            conn.close()
            messagebox.showinfo("Erfolg", "Projekt gespeichert!")
            projekt_window.destroy()
            open_projektverwaltung()

        listbox = Listbox(projekt_window, width=100)
        listbox.grid(row=7, column=0, columnspan=2)
        listbox.bind('<Double-1>', projekt_details)

        Button(projekt_window, text="Speichern", command=save_projekt).grid(row=6, column=1)
        Button(projekt_window, text="Projekt suchen", command=projekt_suchen).grid(row=8, column=0, columnspan=2, pady=5)
        Button(projekt_window, text="Projekt ändern", command=projekt_aendern).grid(row=9, column=0, columnspan=2, pady=5)
        Button(projekt_window, text="Projekt löschen", command=projekt_loeschen).grid(row=10, column=0, columnspan=2, pady=5)

        # Fülle die Projektliste beim Öffnen der Projektverwaltung
        refresh_projekt_list()

        markiere_projekte_im_kalender()

    main_app = Tk()
    main_app.title("Handwerkersoftware")

    # Kalender Integration
    frame_calendar = Frame(main_app)
    frame_calendar.pack(pady=20)
    cal = Calendar(frame_calendar, selectmode='day', year=2024, month=10, day=5)
    cal.pack()
    cal.bind('<<CalendarSelected>>', kalender_projekt_details)

    # Buttons für Lager- und Projektverwaltung
    Button(main_app, text="Lagerverwaltung", command=open_lagerverwaltung).pack(pady=10)
    Button(main_app, text="Projektverwaltung", command=open_projektverwaltung).pack(pady=10)

    main_app.mainloop()

if __name__ == "__main__":
    initialize_database()
    import_csv_to_db()
    login()
