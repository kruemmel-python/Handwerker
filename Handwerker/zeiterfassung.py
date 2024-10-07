import sqlite3
from tkinter import Toplevel, Button, Listbox, Label, Entry, messagebox, END
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
from plugin_manager import plugin_manager
from datetime import datetime

DB_PATH = 'handwerker.db'

class ZeiterfassungPlugin:
    def __init__(self):
        plugin_manager.register_plugin('MitarbeiterZeiterfassung', self)

    def open_zeiterfassung(self, root=None):
        zeiterfassung_window = Toplevel(root)
        zeiterfassung_window.title("Mitarbeiter Zeiterfassung")

        # Verbindung zur Datenbank herstellen
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Funktion zum Schließen der Verbindung, wenn das Fenster geschlossen wird
        def on_close():
            self.conn.close()
            zeiterfassung_window.destroy()

        zeiterfassung_window.protocol("WM_DELETE_WINDOW", on_close)

        # GUI-Elemente zur Zeiterfassung
        Label(zeiterfassung_window, text="Mitarbeiter").grid(row=0, column=0)
        self.mitarbeiter_combobox = Combobox(zeiterfassung_window)
        self.mitarbeiter_combobox.grid(row=0, column=1)

        # Mitarbeiter in die Combobox laden
        self.cursor.execute("SELECT vorname, nachname FROM mitarbeiter")
        mitarbeiter_list = [f"{row[0]} {row[1]}" for row in self.cursor.fetchall()]
        self.mitarbeiter_combobox['values'] = mitarbeiter_list

        Label(zeiterfassung_window, text="Datum").grid(row=1, column=0)
        self.datum_entry = DateEntry(zeiterfassung_window, date_pattern='yyyy-mm-dd')
        self.datum_entry.grid(row=1, column=1)

        Label(zeiterfassung_window, text="Startzeit (HH:MM)").grid(row=2, column=0)
        self.startzeit_entry = Entry(zeiterfassung_window)
        self.startzeit_entry.grid(row=2, column=1)

        Label(zeiterfassung_window, text="Endzeit (HH:MM)").grid(row=3, column=0)
        self.endzeit_entry = Entry(zeiterfassung_window)
        self.endzeit_entry.grid(row=3, column=1)

        Label(zeiterfassung_window, text="Pausenstart (HH:MM)").grid(row=4, column=0)
        self.pausenstart_entry = Entry(zeiterfassung_window)
        self.pausenstart_entry.grid(row=4, column=1)

        Label(zeiterfassung_window, text="Pausenende (HH:MM)").grid(row=5, column=0)
        self.pausenende_entry = Entry(zeiterfassung_window)
        self.pausenende_entry.grid(row=5, column=1)

        Button(zeiterfassung_window, text="Zeit erfassen", command=self.zeit_erfassen).grid(row=6, column=0, columnspan=2, pady=10)

        # Listbox zur Anzeige der erfassten Zeiten
        self.zeit_listbox = Listbox(zeiterfassung_window, width=80)
        self.zeit_listbox.grid(row=7, column=0, columnspan=2)

        Button(zeiterfassung_window, text="Zeiten anzeigen", command=self.zeiten_anzeigen).grid(row=8, column=0, columnspan=2, pady=10)

        # Listbox-Eintrag anklickbar machen
        self.zeit_listbox.bind("<<ListboxSelect>>", self.zeige_tag_details)

    def zeit_erfassen(self):
        mitarbeiter = self.mitarbeiter_combobox.get()
        datum = self.datum_entry.get()
        startzeit = self.startzeit_entry.get()
        endzeit = self.endzeit_entry.get()
        pausenstart = self.pausenstart_entry.get()
        pausenende = self.pausenende_entry.get()

        if not mitarbeiter or not datum or not startzeit or not endzeit or not pausenstart or not pausenende:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt sein.")
            return

        vorname, nachname = mitarbeiter.split()

        try:
            # Mitarbeiter-ID abrufen
            self.cursor.execute("SELECT rowid FROM mitarbeiter WHERE vorname = ? AND nachname = ?", (vorname, nachname))
            mitarbeiter_id = self.cursor.fetchone()
            if not mitarbeiter_id:
                messagebox.showerror("Fehler", "Mitarbeiter nicht gefunden.")
                return

            mitarbeiter_id = mitarbeiter_id[0]

            # Projektzuordnung prüfen
            self.cursor.execute("SELECT projekt_name FROM projekte WHERE mitarbeiter LIKE ?", (f"%{mitarbeiter}%",))
            projekt = self.cursor.fetchone()
            projekt_name = projekt[0] if projekt else None

            # Arbeitszeit in der Datenbank speichern
            self.cursor.execute('''
                INSERT INTO zeiterfassung (mitarbeiter_id, datum, startzeit, endzeit, pausenstart, pausenende, projekt_name)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (mitarbeiter_id, datum, startzeit, endzeit, pausenstart, pausenende, projekt_name))
            self.conn.commit()

            messagebox.showinfo("Erfolg", "Arbeitszeit wurde erfolgreich erfasst!")
        except sqlite3.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Erfassen der Arbeitszeit: {e}")

    def zeiten_anzeigen(self):
        self.zeit_listbox.delete(0, END)
        try:
            self.cursor.execute('''
                SELECT m.vorname, m.nachname, z.datum, z.startzeit, z.endzeit, z.pausenstart, z.pausenende, z.projekt_name
                FROM zeiterfassung z
                JOIN mitarbeiter m ON z.mitarbeiter_id = m.rowid
            ''')
            rows = self.cursor.fetchall()
            for row in rows:
                self.zeit_listbox.insert(END, f"{row[0]} {row[1]} - Datum: {row[2]}, Startzeit: {row[3]}, Endzeit: {row[4]}, Pausen: {row[5]} - {row[6]}, Projekt: {row[7]}")
        except sqlite3.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Arbeitszeiten: {e}")

    def zeige_tag_details(self, event):
        selected_index = self.zeit_listbox.curselection()
        if not selected_index:
            return
        selected_text = self.zeit_listbox.get(selected_index[0])
        datum = selected_text.split("- Datum: ")[1].split(",")[0]  # Extrahiere das Datum

        try:
            self.cursor.execute('''
                SELECT z.startzeit, z.endzeit, z.pausenstart, z.pausenende
                FROM zeiterfassung z
                WHERE z.datum = ?
            ''', (datum,))
            zeiten = self.cursor.fetchall()
            for zeit in zeiten:
                startzeit, endzeit, pausenstart, pausenende = zeit
                brutto_zeit = self.zeitdifferenz(startzeit, endzeit)
                pause = self.zeitdifferenz(pausenstart, pausenende)
                netto_zeit = brutto_zeit - pause

                messagebox.showinfo("Tagesdetails", f"Bruttoarbeitszeit: {brutto_zeit}\nPause: {pause}\nNettoarbeitszeit: {netto_zeit}")
        except sqlite3.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Tagesdetails: {e}")

    def zeitdifferenz(self, start, ende):
        FMT = '%H:%M'
        tdelta = datetime.strptime(ende, FMT) - datetime.strptime(start, FMT)
        return tdelta.total_seconds() / 3600  # Stunden zurückgeben

# Tabelle für die Zeiterfassung erstellen, falls sie noch nicht existiert
def initialize_zeiterfassung_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS zeiterfassung (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mitarbeiter_id INTEGER,
                datum TEXT,
                startzeit TEXT,
                endzeit TEXT,
                pausenstart TEXT,
                pausenende TEXT,
                projekt_name TEXT,
                FOREIGN KEY (mitarbeiter_id) REFERENCES mitarbeiter (rowid)
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Datenbankfehler", f"Fehler beim Initialisieren der Zeiterfassungs-Datenbank: {e}")

# Plugin-Instanz erstellen
zeiterfassung_plugin = ZeiterfassungPlugin()
initialize_zeiterfassung_database()
