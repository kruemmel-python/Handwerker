import sqlite3
import csv
from tkinter import Toplevel, Label, Entry, Button, Text, Scrollbar, END, messagebox
from tkinter import N, E, W, S  # Für bessere Ausrichtung
from tkinter import ttk
from plugin_manager import plugin_manager

# Pfad zur SQLite-Datenbank
DB_PATH = 'handwerker.db'

class MitarbeiterPlugin:
    def __init__(self):
        # Plugin registrieren
        plugin_manager.register_plugin('MitarbeiterPlugin', self)

        # Initialisiere die Mitarbeiterdatenbank und Tabelle
        self.initialize_database()

        # Importiere die Daten aus der CSV-Datei
        self.import_csv_to_database()

    def initialize_database(self):
        """Erstellt die Mitarbeiterdatenbank und Tabelle, falls sie nicht existiert."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Mitarbeitertabelle erstellen, falls nicht vorhanden
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mitarbeiter (
                    vorname TEXT,
                    nachname TEXT,
                    strasse TEXT,
                    hausnummer TEXT,
                    plz TEXT,
                    ort TEXT,
                    telefonnummer TEXT,
                    handynummer TEXT,
                    email TEXT,
                    geburtsdatum TEXT,
                    geburtsort TEXT,
                    staatsangehoerigkeit TEXT,
                    geschlecht TEXT,
                    familienstand TEXT,
                    steuerklasse TEXT,
                    sozialversicherungsnummer TEXT,
                    krankenkasse TEXT,
                    krankenkassen_versicherungsnummer TEXT,
                    stundenlohn_brutto REAL,
                    eintrittsdatum TEXT,
                    austrittsdatum TEXT,
                    probezeitende TEXT,
                    benutzername TEXT,
                    passwort TEXT,
                    firmenfahrzeug_kennzeichen TEXT,
                    religion TEXT,
                    arbeitserlaubnis_gueltig_bis TEXT,
                    notfallkontakt_name TEXT,
                    notfallkontakt_telefon TEXT,
                    bankname TEXT,
                    iban TEXT,
                    bic TEXT,
                    PRIMARY KEY (vorname, nachname)
                )
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Initialisieren der Datenbank: {e}")

    def import_csv_to_database(self):
        """Importiert Mitarbeiterdaten aus einer CSV-Datei in die Datenbank."""
        csv_file_path = 'mitarbeiter.csv'  # Pfad zur CSV-Datei
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Öffne die CSV-Datei und lese die Daten
            with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
                csvreader = csv.DictReader(csvfile, delimiter=';')

                # Prüfen, ob alle erforderlichen Spalten vorhanden sind
                required_columns = [
                    'vorname', 'nachname', 'strasse', 'hausnummer', 'plz', 'ort', 'telefonnummer', 'handynummer',
                    'email', 'geburtsdatum', 'geburtsort', 'staatsangehoerigkeit', 'geschlecht', 'familienstand',
                    'steuerklasse', 'sozialversicherungsnummer', 'krankenkasse', 'krankenkassen_versicherungsnummer',
                    'stundenlohn_brutto', 'eintrittsdatum', 'austrittsdatum', 'probezeitende', 'benutzername', 'passwort',
                    'firmenfahrzeug_kennzeichen', 'religion', 'arbeitserlaubnis_gueltig_bis', 'notfallkontakt_name',
                    'notfallkontakt_telefon', 'bankname', 'iban', 'bic'
                ]

                csv_columns = [col.strip().lower() for col in csvreader.fieldnames if col is not None]
                required_columns = [col.lower() for col in required_columns]

                missing_columns = [col for col in required_columns if col not in csv_columns]
                if missing_columns:
                    messagebox.showerror("CSV-Fehler", f"Die CSV-Datei enthält nicht alle erforderlichen Spalten: {', '.join(missing_columns)}")
                    return

                # Gehe durch jede Zeile und füge sie in die Datenbank ein
                for row in csvreader:
                    try:
                        cursor.execute('''
                            INSERT OR IGNORE INTO mitarbeiter (
                                vorname, nachname, strasse, hausnummer, plz, ort, telefonnummer, handynummer, email,
                                geburtsdatum, geburtsort, staatsangehoerigkeit, geschlecht, familienstand, steuerklasse,
                                sozialversicherungsnummer, krankenkasse, krankenkassen_versicherungsnummer, stundenlohn_brutto,
                                eintrittsdatum, austrittsdatum, probezeitende, benutzername, passwort, firmenfahrzeug_kennzeichen,
                                religion, arbeitserlaubnis_gueltig_bis, notfallkontakt_name, notfallkontakt_telefon, bankname, iban, bic
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            row['vorname'], row['nachname'], row['strasse'], row['hausnummer'], row['plz'], row['ort'],
                            row['telefonnummer'], row['handynummer'], row['email'], row['geburtsdatum'], row['geburtsort'],
                            row['staatsangehoerigkeit'], row['geschlecht'], row['familienstand'], row['steuerklasse'],
                            row['sozialversicherungsnummer'], row['krankenkasse'], row['krankenkassen_versicherungsnummer'],
                            float(row['stundenlohn_brutto']) if row['stundenlohn_brutto'] else None, row['eintrittsdatum'],
                            row['austrittsdatum'], row['probezeitende'], row['benutzername'], row['passwort'],
                            row['firmenfahrzeug_kennzeichen'], row['religion'], row['arbeitserlaubnis_gueltig_bis'],
                            row['notfallkontakt_name'], row['notfallkontakt_telefon'], row['bankname'], row['iban'], row['bic']
                        ))
                    except sqlite3.Error as db_error:
                        messagebox.showerror("Datenbankfehler", f"Fehler beim Einfügen der Daten: {db_error}")
                    except ValueError as value_error:
                        messagebox.showerror("Datenfehler", f"Fehler bei der Datenkonvertierung: {value_error}")

            conn.commit()
            conn.close()
            print("Daten wurden erfolgreich importiert.")

        except FileNotFoundError:
            messagebox.showerror("Dateifehler", f"Die Datei '{csv_file_path}' wurde nicht gefunden.")
        except sqlite3.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Importieren der Daten in die Datenbank: {e}")

    def open_mitarbeiterverwaltung(self):
        """Öffnet das Fenster zur Mitarbeiterverwaltung."""
        mitarbeiter_window = Toplevel()
        mitarbeiter_window.title("Mitarbeiterverwaltung")

        # Layout-Optionen für bessere Ausrichtung
        padding_x = 10
        padding_y = 5

        # Erstelle einen Frame für die Textbox und den Scrollbar
        top_frame = ttk.Frame(mitarbeiter_window)
        top_frame.grid(row=0, column=0, columnspan=4, padx=padding_x, pady=padding_y, sticky=W+E)

        # Textbox, um den Inhalt der Tabelle anzuzeigen
        text_box = Text(top_frame, height=10, width=100)
        text_box.grid(row=0, column=0, sticky=W+E)

        # Scrollbar für die Textbox
        scrollbar = Scrollbar(top_frame)
        scrollbar.grid(row=0, column=1, sticky=N+S)
        text_box.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_box.yview)

        # Fülle die Textbox mit den Mitarbeitern beim Öffnen
        self.mitarbeiterliste_anzeigen(text_box)

        # Doppelklick-Event für die Textbox
        def on_double_click(event):
            try:
                # Hole die Zeile, die doppelt angeklickt wurde
                selected_line = text_box.get("@%d,%d linestart" % (event.x, event.y), "@%d,%d lineend" % (event.x, event.y)).strip()
                if not selected_line:
                    return

                # Extrahiere den Namen (Vorname und Nachname)
                name_parts = selected_line.split('-')[0].strip().split()
                if len(name_parts) < 2:
                    return

                vorname, nachname = name_parts[0], name_parts[1]

                # Hole die vollständigen Informationen des Mitarbeiters aus der Datenbank
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM mitarbeiter WHERE vorname = ? AND nachname = ?
                ''', (vorname, nachname))
                mitarbeiter = cursor.fetchone()
                conn.close()

                if mitarbeiter:
                    for i, label_text in enumerate(labels):
                        entries[label_text].delete(0, END)
                        entries[label_text].insert(0, mitarbeiter[i])
            except sqlite3.Error as e:
                messagebox.showerror("Datenbankfehler", f"Fehler beim Abrufen der Mitarbeiterdaten: {e}")

        text_box.bind("<Double-1>", on_double_click)

        # Frame für Eingabefelder erstellen
        input_frame = ttk.Frame(mitarbeiter_window)
        input_frame.grid(row=1, column=0, columnspan=4, padx=padding_x, pady=padding_y, sticky=W+E)

        # GUI-Elemente für Eingabefelder, 2 Spalten mit 16 Reihen
        labels = [
            "Vorname", "Nachname", "Straße", "Hausnummer", "PLZ", "Ort", "Telefonnummer", "Handynummer", "Email",
            "Geburtsdatum", "Geburtsort", "Staatsangehörigkeit", "Geschlecht", "Familienstand", "Steuerklasse",
            "Sozialversicherungsnummer", "Krankenkasse", "Krankenkassen-Versicherungsnummer", "Stundenlohn (Brutto)",
            "Eintrittsdatum", "Austrittsdatum", "Probezeitende", "Benutzername", "Passwort",
            "Firmenfahrzeug-Kennzeichen", "Religion", "Arbeitserlaubnis gültig bis", "Notfallkontakt Name",
            "Notfallkontakt Telefon", "Bankname", "IBAN", "BIC"
        ]

        entries = {}
        for i, label_text in enumerate(labels):
            row = i // 2
            column = i % 2
            label = Label(input_frame, text=label_text)
            label.grid(row=row, column=column*2, padx=padding_x, pady=padding_y, sticky=E)
            entry = Entry(input_frame, width=40)
            entry.grid(row=row, column=column*2+1, padx=padding_x, pady=padding_y, sticky=W)
            entries[label_text] = entry

        # Funktionen zur Mitarbeiterverwaltung
        def mitarbeiter_hinzufuegen():
            """Fügt einen neuen Mitarbeiter hinzu."""
            data = [entries[label].get() for label in labels]

            if not data[0] or not data[1]:
                messagebox.showerror("Fehler", "Vorname und Nachname müssen angegeben werden.")
                return

            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO mitarbeiter (
                        vorname, nachname, strasse, hausnummer, plz, ort, telefonnummer, handynummer, email,
                        geburtsdatum, geburtsort, staatsangehoerigkeit, geschlecht, familienstand, steuerklasse,
                        sozialversicherungsnummer, krankenkasse, krankenkassen_versicherungsnummer, stundenlohn_brutto,
                        eintrittsdatum, austrittsdatum, probezeitende, benutzername, passwort, firmenfahrzeug_kennzeichen,
                        religion, arbeitserlaubnis_gueltig_bis, notfallkontakt_name, notfallkontakt_telefon, bankname, iban, bic
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', data)
                conn.commit()
                conn.close()

                messagebox.showinfo("Erfolg", "Mitarbeiter hinzugefügt!")
                self.mitarbeiterliste_anzeigen(text_box)
            except sqlite3.Error as e:
                messagebox.showerror("Datenbankfehler", f"Fehler beim Hinzufügen des Mitarbeiters: {e}")

        def mitarbeiter_aendern():
            """Ändert die Daten des ausgewählten Mitarbeiters."""
            selected = text_box.get("1.0", "end-1c").strip()
            if not selected:
                messagebox.showerror("Fehler", "Bitte wählen Sie einen Mitarbeiter aus der Liste aus.")
                return

            # Extrahiere den Namen (Vorname und Nachname)
            name_parts = selected.split('-')[0].strip().split()
            if len(name_parts) < 2:
                return

            vorname, nachname = name_parts[0], name_parts[1]

            data = [entries[label].get() for label in labels]

            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE mitarbeiter SET
                        strasse = ?, hausnummer = ?, plz = ?, ort = ?, telefonnummer = ?, handynummer = ?, email = ?,
                        geburtsdatum = ?, geburtsort = ?, staatsangehoerigkeit = ?, geschlecht = ?, familienstand = ?,
                        steuerklasse = ?, sozialversicherungsnummer = ?, krankenkasse = ?, krankenkassen_versicherungsnummer = ?,
                        stundenlohn_brutto = ?, eintrittsdatum = ?, austrittsdatum = ?, probezeitende = ?, benutzername = ?,
                        passwort = ?, firmenfahrzeug_kennzeichen = ?, religion = ?, arbeitserlaubnis_gueltig_bis = ?,
                        notfallkontakt_name = ?, notfallkontakt_telefon = ?, bankname = ?, iban = ?, bic = ?
                    WHERE vorname = ? AND nachname = ?
                ''', data[2:] + [vorname, nachname])
                conn.commit()
                conn.close()

                messagebox.showinfo("Erfolg", "Mitarbeiterdaten wurden aktualisiert!")
                self.mitarbeiterliste_anzeigen(text_box)
            except sqlite3.Error as e:
                messagebox.showerror("Datenbankfehler", f"Fehler beim Ändern des Mitarbeiters: {e}")

        def mitarbeiter_loeschen():
            """Löscht einen ausgewählten Mitarbeiter."""
            selected = text_box.get("1.0", "end-1c").strip()
            if not selected:
                messagebox.showerror("Fehler", "Bitte wählen Sie einen Mitarbeiter aus der Liste aus.")
                return

            # Extrahiere den Namen (Vorname und Nachname)
            name_parts = selected.split('-')[0].strip().split()
            if len(name_parts) < 2:
                return

            vorname, nachname = name_parts[0], name_parts[1]

            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM mitarbeiter WHERE vorname = ? AND nachname = ?
                ''', (vorname, nachname))
                conn.commit()
                conn.close()

                messagebox.showinfo("Erfolg", "Mitarbeiter gelöscht!")
                self.mitarbeiterliste_anzeigen(text_box)
            except sqlite3.Error as e:
                messagebox.showerror("Datenbankfehler", f"Fehler beim Löschen des Mitarbeiters: {e}")

        # Buttons zur Mitarbeiterverwaltung
        button_frame = ttk.Frame(mitarbeiter_window)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)

        Button(button_frame, text="Mitarbeiter hinzufügen", command=mitarbeiter_hinzufuegen).pack(side="left", padx=10)
        Button(button_frame, text="Mitarbeiter ändern", command=mitarbeiter_aendern).pack(side="left", padx=10)
        Button(button_frame, text="Mitarbeiter löschen", command=mitarbeiter_loeschen).pack(side="left", padx=10)

    def mitarbeiterliste_anzeigen(self, text_box):
        """Zeigt die Liste der Mitarbeiter in der Textbox an."""
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT vorname, nachname, email FROM mitarbeiter")
            rows = cursor.fetchall()
            conn.close()

            # Lösche den vorherigen Inhalt der Textbox
            text_box.delete("1.0", END)

            # Füge die Mitarbeiter in die Textbox ein
            for row in rows:
                text_box.insert(END, f"{row[0]} {row[1]} - {row[2]}\n")
        except sqlite3.Error as e:
            messagebox.showerror("Datenbankfehler", f"Fehler beim Anzeigen der Mitarbeiterliste: {e}")


# Plugin-Instanz erstellen und Menü hinzufügen, falls in eine bestehende GUI integriert
if __name__ != "__main__":
    def start_plugin(root):
        plugin = MitarbeiterPlugin()