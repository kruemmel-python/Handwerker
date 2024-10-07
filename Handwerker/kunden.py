import sqlite3
from tkinter import Toplevel, Label, Entry, Button, Listbox, END, messagebox
from tkinter import N, E, W, S  # Für bessere Ausrichtung
from plugin_manager import plugin_manager

# Pfad zur SQLite-Datenbank
DB_PATH = 'handwerker.db'

class KundenPlugin:
    def __init__(self):
        # Plugin registrieren
        plugin_manager.register_plugin('KundenPlugin', self)

        # Initialisiere die Kundendatenbank und füge Kunden hinzu
        self.initialize_database()
        self.insert_initial_kunden()

    def initialize_database(self):
        """Erstellt die Kundendatenbank und Tabelle, falls sie nicht existiert."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Kundentabelle erstellen
        cursor.execute('''CREATE TABLE IF NOT EXISTS kunden (
                            kundenID INTEGER PRIMARY KEY AUTOINCREMENT,
                            vorname TEXT,
                            nachname TEXT,
                            strasse TEXT,
                            hausnummer TEXT,
                            plz TEXT,
                            ort TEXT,
                            telefonnummer TEXT,
                            email TEXT
                        )''')
        conn.commit()
        conn.close()

    def insert_initial_kunden(self):
        """Fügt eine Liste von Beispielkunden in die Datenbank ein, falls noch keine Einträge existieren."""
        kunden_liste = [
            ("Max", "Mustermann", "Musterstraße", "1", "12345", "Musterstadt", "0123456789", "max.mustermann@example.com"),
            ("Erika", "Beispiel", "Beispielweg", "2", "67890", "Beispielort", "0987654321", "erika.beispiel@example.com"),
            ("Hans", "Müller", "Müllerstraße", "3", "54321", "Müllerstadt", "0123456789", "hans.mueller@example.com"),
            ("Anna", "Schmidt", "Schmidtstraße", "4", "98765", "Schmidtstadt", "0987654321", "anna.schmidt@example.com"),
            ("Klaus", "Weber", "Weberweg", "5", "43210", "Weberort", "0123456789", "klaus.weber@example.com"),
            ("Maria", "Schneider", "Schneiderstraße", "6", "87654", "Schneiderstadt", "0987654321", "maria.schneider@example.com"),
            ("Peter", "Fischer", "Fischerweg", "7", "32109", "Fischerort", "0123456789", "peter.fischer@example.com"),
            ("Susanne", "Meyer", "Meyerstraße", "8", "76543", "Meyerstadt", "0987654321", "susanne.meyer@example.com"),
            ("Thomas", "Wagner", "Wagnerweg", "9", "21098", "Wagnerort", "0123456789", "thomas.wagner@example.com"),
            ("Karin", "Becker", "Beckerstraße", "10", "65432", "Beckerstadt", "0987654321", "karin.becker@example.com"),
            ("Michael", "Schulz", "Schulzweg", "11", "10987", "Schulzort", "0123456789", "michael.schulz@example.com"),
            ("Sabine", "Hoffmann", "Hoffmannstraße", "12", "54321", "Hoffmannstadt", "0987654321", "sabine.hoffmann@example.com"),
            ("Stefan", "Schäfer", "Schäferweg", "13", "98765", "Schäferort", "0123456789", "stefan.schaefer@example.com"),
            ("Petra", "Koch", "Kochstraße", "14", "43210", "Kochstadt", "0987654321", "petra.koch@example.com"),
            ("Markus", "Bauer", "Bauerweg", "15", "87654", "Bauerort", "0123456789", "markus.bauer@example.com")
        ]

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Prüfe, ob bereits Kunden in der Datenbank sind, um doppelte Einträge zu vermeiden
        cursor.execute("SELECT COUNT(*) FROM kunden")
        kunden_count = cursor.fetchone()[0]

        if kunden_count == 0:
            for kunde in kunden_liste:
                cursor.execute('''INSERT INTO kunden (vorname, nachname, strasse, hausnummer, plz, ort, telefonnummer, email)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', kunde)

            # Änderungen speichern und Verbindung schließen
            conn.commit()
            print("15 Kunden wurden erfolgreich in die Datenbank eingefügt.")
        else:
            print("Die Kunden sind bereits in der Datenbank vorhanden.")

        conn.close()



    def open_kundenverwaltung(self):
        """Öffnet das Fenster zur Kundenverwaltung."""
        kunden_window = Toplevel()
        kunden_window.title("Kundenverwaltung")

        # Layout-Optionen für bessere Ausrichtung
        padding_x = 10
        padding_y = 5

        # GUI-Elemente mit erweiterter Ausrichtung
        Label(kunden_window, text="Vorname").grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky=E)
        entry_vorname = Entry(kunden_window)
        entry_vorname.grid(row=0, column=1, padx=padding_x, pady=padding_y, sticky=W)

        Label(kunden_window, text="Nachname").grid(row=1, column=0, padx=padding_x, pady=padding_y, sticky=E)
        entry_nachname = Entry(kunden_window)
        entry_nachname.grid(row=1, column=1, padx=padding_x, pady=padding_y, sticky=W)

        Label(kunden_window, text="Straße").grid(row=2, column=0, padx=padding_x, pady=padding_y, sticky=E)
        entry_strasse = Entry(kunden_window)
        entry_strasse.grid(row=2, column=1, padx=padding_x, pady=padding_y, sticky=W)

        Label(kunden_window, text="Hausnummer").grid(row=3, column=0, padx=padding_x, pady=padding_y, sticky=E)
        entry_hausnummer = Entry(kunden_window)
        entry_hausnummer.grid(row=3, column=1, padx=padding_x, pady=padding_y, sticky=W)

        Label(kunden_window, text="PLZ").grid(row=4, column=0, padx=padding_x, pady=padding_y, sticky=E)
        entry_plz = Entry(kunden_window)
        entry_plz.grid(row=4, column=1, padx=padding_x, pady=padding_y, sticky=W)

        Label(kunden_window, text="Ort").grid(row=5, column=0, padx=padding_x, pady=padding_y, sticky=E)
        entry_ort = Entry(kunden_window)
        entry_ort.grid(row=5, column=1, padx=padding_x, pady=padding_y, sticky=W)

        Label(kunden_window, text="Telefonnummer").grid(row=6, column=0, padx=padding_x, pady=padding_y, sticky=E)
        entry_telefonnummer = Entry(kunden_window)
        entry_telefonnummer.grid(row=6, column=1, padx=padding_x, pady=padding_y, sticky=W)

        Label(kunden_window, text="E-Mail").grid(row=7, column=0, padx=padding_x, pady=padding_y, sticky=E)
        entry_email = Entry(kunden_window)
        entry_email.grid(row=7, column=1, padx=padding_x, pady=padding_y, sticky=W)

        # Kundenliste mit verbesserter Größe
        listbox = Listbox(kunden_window, width=50, height=10)
        listbox.grid(row=0, column=2, rowspan=8, padx=padding_x, pady=padding_y, sticky=N+S)

        # Funktionen für die CRUD-Operationen
        def kunde_hinzufuegen():
            """Fügt einen neuen Kunden hinzu."""
            vorname = entry_vorname.get()
            nachname = entry_nachname.get()
            strasse = entry_strasse.get()
            hausnummer = entry_hausnummer.get()
            plz = entry_plz.get()
            ort = entry_ort.get()
            telefonnummer = entry_telefonnummer.get()
            email = entry_email.get()

            if not vorname or not nachname:
                messagebox.showerror("Fehler", "Vorname und Nachname müssen angegeben werden.")
                return

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO kunden (vorname, nachname, strasse, hausnummer, plz, ort, telefonnummer, email)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                           (vorname, nachname, strasse, hausnummer, plz, ort, telefonnummer, email))
            conn.commit()
            conn.close()

            messagebox.showinfo("Erfolg", "Kunde hinzugefügt!")
            kundenliste_aktualisieren()

        def kundenliste_aktualisieren():
            """Aktualisiert die Kundenliste in der Listbox."""
            listbox.delete(0, END)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT kundenID, vorname, nachname FROM kunden")
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                listbox.insert(END, f"{row[0]}: {row[1]} {row[2]}")

        def kunde_loeschen():
            """Löscht einen ausgewählten Kunden."""
            selected = listbox.curselection()
            if not selected:
                messagebox.showerror("Fehler", "Bitte wählen Sie einen Kunden aus der Liste aus.")
                return

            kunde_id = listbox.get(selected).split(":")[0]

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM kunden WHERE kundenID = ?", (kunde_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Erfolg", "Kunde gelöscht!")
            kundenliste_aktualisieren()

        def kunde_aendern():
            """Ändert die Daten des ausgewählten Kunden."""
            selected = listbox.curselection()
            if not selected:
                messagebox.showerror("Fehler", "Bitte wählen Sie einen Kunden aus der Liste aus.")
                return

            kunde_id = listbox.get(selected).split(":")[0]

            # Hole die aktuellen Kundendaten aus der Datenbank
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kunden WHERE kundenID = ?", (kunde_id,))
            kunde = cursor.fetchone()

            if kunde:
                # Fülle die Felder mit den aktuellen Daten
                entry_vorname.delete(0, END)
                entry_vorname.insert(0, kunde[1])
                entry_nachname.delete(0, END)
                entry_nachname.insert(0, kunde[2])
                entry_strasse.delete(0, END)
                entry_strasse.insert(0, kunde[3])
                entry_hausnummer.delete(0, END)
                entry_hausnummer.insert(0, kunde[4])
                entry_plz.delete(0, END)
                entry_plz.insert(0, kunde[5])
                entry_ort.delete(0, END)
                entry_ort.insert(0, kunde[6])
                entry_telefonnummer.delete(0, END)
                entry_telefonnummer.insert(0, kunde[7])
                entry_email.delete(0, END)
                entry_email.insert(0, kunde[8])

                def speichern_aenderungen():
                    """Speichert die geänderten Kundendaten."""
                    vorname = entry_vorname.get()
                    nachname = entry_nachname.get()
                    strasse = entry_strasse.get()
                    hausnummer = entry_hausnummer.get()
                    plz = entry_plz.get()
                    ort = entry_ort.get()
                    telefonnummer = entry_telefonnummer.get()
                    email = entry_email.get()

                    cursor.execute('''UPDATE kunden SET vorname = ?, nachname = ?, strasse = ?, hausnummer = ?, plz = ?, ort = ?, telefonnummer = ?, email = ? 
                                      WHERE kundenID = ?''',
                                   (vorname, nachname, strasse, hausnummer, plz, ort, telefonnummer, email, kunde_id))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Erfolg", "Kundendaten aktualisiert!")
                    kundenliste_aktualisieren()

                # Speichern-Button für Änderungen
                Button(kunden_window, text="Änderungen speichern", command=speichern_aenderungen).grid(row=8, column=1)

        def kunde_anzeigen(event):
            """Zeigt alle Informationen eines Kunden bei Doppelklick auf den Kundennamen an."""
            selected = listbox.curselection()
            if not selected:
                return

            kunde_id = listbox.get(selected).split(":")[0]

            # Hole die Kundendaten aus der Datenbank
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM kunden WHERE kundenID = ?", (kunde_id,))
            kunde = cursor.fetchone()
            conn.close()

            if kunde:
                details = (f"ID: {kunde[0]}\nVorname: {kunde[1]}\nNachname: {kunde[2]}\n"
                           f"Straße: {kunde[3]} {kunde[4]}\nPLZ: {kunde[5]}\nOrt: {kunde[6]}\n"
                           f"Telefonnummer: {kunde[7]}\nE-Mail: {kunde[8]}")
                messagebox.showinfo("Kundendetails", details)

        # Bind Doppelklick-Event für die Listbox
        listbox.bind('<Double-1>', kunde_anzeigen)

        # Buttons zur Kundenverwaltung
        Button(kunden_window, text="Kunde hinzufügen", command=kunde_hinzufuegen).grid(row=8, column=0, padx=padding_x, pady=padding_y)
        Button(kunden_window, text="Kunde ändern", command=kunde_aendern).grid(row=9, column=0, padx=padding_x, pady=padding_y)
        Button(kunden_window, text="Kunde löschen", command=kunde_loeschen).grid(row=9, column=1, padx=padding_x, pady=padding_y)

        # Kundenliste beim Öffnen des Fensters aktualisieren
        kundenliste_aktualisieren()

# Plugin-Instanz erstellen
kunden_plugin = KundenPlugin()
