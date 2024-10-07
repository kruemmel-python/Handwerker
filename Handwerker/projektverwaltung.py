import sqlite3
from tkinter import Toplevel, Listbox, Button, simpledialog, END, messagebox, Entry, Label
from tkinter.ttk import Combobox  # Für die Kunden- und Mitarbeiterauswahl
from tkcalendar import DateEntry
from plugin_manager import plugin_manager
from lagerverwaltung import lager_plugin  # Um Artikel aus dem Lager auszuwählen
from kalender import kalender_plugin  # Kalenderintegration

DB_PATH = 'handwerker.db'

class ProjektPlugin:
    def __init__(self):
        plugin_manager.register_plugin('Projektverwaltung', self)

    def open_projektverwaltung(self):
        projekt_window = Toplevel()
        projekt_window.title("Projektverwaltung")

        # Verbindung zur Datenbank öffnen, wenn die Projektverwaltung geöffnet wird
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Funktion zum Schließen der Verbindung, wenn das Fenster geschlossen wird
        def on_close():
            self.conn.close()
            projekt_window.destroy()

        projekt_window.protocol("WM_DELETE_WINDOW", on_close)

        # GUI-Elemente für die Projektdetails
        listbox = Listbox(projekt_window, width=100)
        listbox.grid(row=0, column=0, columnspan=2)

        Label(projekt_window, text="Projektname").grid(row=1, column=0)
        entry_projektname = Entry(projekt_window)
        entry_projektname.grid(row=1, column=1)

        # Kunde auswählen (mit Combobox)
        Label(projekt_window, text="Kunde").grid(row=2, column=0)
        combobox_kunde = Combobox(projekt_window)
        combobox_kunde.grid(row=2, column=1)

        # Mitarbeiter auswählen (mit Combobox)
        Label(projekt_window, text="Mitarbeiter").grid(row=3, column=0)
        combobox_mitarbeiter = Combobox(projekt_window)
        combobox_mitarbeiter.grid(row=3, column=1)

        # Kunden und Mitarbeiter aus der Datenbank laden
        self.cursor.execute("SELECT vorname, nachname FROM kunden")
        kunden_liste = [f"{row[0]} {row[1]}" for row in self.cursor.fetchall()]
        combobox_kunde['values'] = kunden_liste

        self.cursor.execute("SELECT vorname, nachname FROM mitarbeiter")
        mitarbeiter_liste = [f"{row[0]} {row[1]}" for row in self.cursor.fetchall()]
        combobox_mitarbeiter['values'] = mitarbeiter_liste

        Label(projekt_window, text="Startdatum").grid(row=4, column=0)
        entry_startdatum = DateEntry(projekt_window, date_pattern='yyyy-mm-dd')
        entry_startdatum.grid(row=4, column=1)

        Label(projekt_window, text="Enddatum").grid(row=5, column=0)
        entry_enddatum = DateEntry(projekt_window, date_pattern='yyyy-mm-dd')
        entry_enddatum.grid(row=5, column=1)

        Label(projekt_window, text="Beschreibung").grid(row=6, column=0)
        entry_beschreibung = Entry(projekt_window)
        entry_beschreibung.grid(row=6, column=1)

        # Statusauswahl (offenes Projekt, beendetes Projekt, Anfrage)
        Label(projekt_window, text="Projektstatus").grid(row=7, column=0)
        combobox_status = Combobox(projekt_window, values=["Offen", "Beendet", "Anfrage"])
        combobox_status.grid(row=7, column=1)
        combobox_status.current(0)  # Standardmäßig "Offen"

        # Artikel hinzufügen: Auswahl von Lagerartikeln und Mengen
        def artikel_hinzufuegen():
            art_nr = simpledialog.askstring("Artikel auswählen", "Art. Nr. eingeben:")
            menge = simpledialog.askinteger("Menge hinzufügen", "Menge für das Projekt:")
            if art_nr and menge is not None:
                # Prüfe, ob der Artikel existiert und genug Bestand vorhanden ist
                self.cursor.execute("SELECT lagerbestand FROM lager WHERE art_nr = ?", (art_nr,))
                row = self.cursor.fetchone()
                if row and row[0] >= menge:
                    # Artikel aus dem Lagerbestand entnehmen
                    self.cursor.execute("UPDATE lager SET lagerbestand = lagerbestand - ? WHERE art_nr = ?", (menge, art_nr))
                    # Artikel dem Projekt zuordnen
                    self.cursor.execute('''INSERT INTO projekt_artikel (projekt_name, art_nr, menge)
                                           VALUES (?, ?, ?)''', (entry_projektname.get(), art_nr, menge))
                    self.conn.commit()
                    listbox.insert(END, f"Artikel: {art_nr}, Menge: {menge}")
                else:
                    messagebox.showerror("Fehler", "Artikel nicht gefunden oder nicht genug Bestand.")

        # Button, um Artikel hinzuzufügen
        Button(projekt_window, text="Artikel hinzufügen", command=artikel_hinzufuegen).grid(row=8, column=0, columnspan=2, pady=5)

        # Artikel ändern
        def artikel_aendern():
            selected_indices = listbox.curselection()

            if not selected_indices:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus der Liste aus.")
                return

            selected_item = listbox.get(selected_indices[0])
            projekt_name = selected_item.split(',')[0].split(':')[1].strip()

            self.cursor.execute("SELECT art_nr, menge FROM projekt_artikel WHERE projekt_name = ?", (projekt_name,))
            artikel_rows = self.cursor.fetchall()

            if not artikel_rows:
                messagebox.showerror("Fehler", "Keine Artikel für dieses Projekt gefunden.")
                return

            for artikel in artikel_rows:
                art_nr, alte_menge = artikel
                neue_menge = simpledialog.askinteger("Menge bearbeiten", f"Menge für Artikel {art_nr} ändern:", initialvalue=alte_menge)
                if neue_menge is not None:
                    differenz = neue_menge - alte_menge
                    if differenz > 0:
                        # Erhöhte Menge -> Lagerbestand reduzieren
                        self.cursor.execute("UPDATE lager SET lagerbestand = lagerbestand - ? WHERE art_nr = ?", (differenz, art_nr))
                    elif differenz < 0:
                        # Verringerte Menge -> Lagerbestand wieder auffüllen
                        self.cursor.execute("UPDATE lager SET lagerbestand = lagerbestand + ? WHERE art_nr = ?", (-differenz, art_nr))

                    self.cursor.execute("UPDATE projekt_artikel SET menge = ? WHERE projekt_name = ? AND art_nr = ?", (neue_menge, projekt_name, art_nr))

            self.conn.commit()
            messagebox.showinfo("Erfolg", "Artikelmengen aktualisiert!")
            refresh_projekt_list()

        # Button, um Artikel zu ändern
        Button(projekt_window, text="Artikel ändern", command=artikel_aendern).grid(row=9, column=0, columnspan=2, pady=5)

        # Neue Funktion für Aufmaß hinzufügen
        def aufmass_hinzufuegen():
            """Fügt eine Aufmaß-Eingabe hinzu und speichert sie in der Datenbank."""
            try:
                raumlaenge = simpledialog.askfloat("Raummaß", "Raumlänge (m):")
                raumbreite = simpledialog.askfloat("Raummaß", "Raumbreite (m):")
                raumhoehe = simpledialog.askfloat("Raummaß", "Raumhöhe (m):")

                if None in (raumlaenge, raumbreite, raumhoehe):
                    messagebox.showerror("Fehler", "Bitte alle Raummaße eingeben.")
                    return

                # Berechnungen für Bodenfläche und Wände
                bodenflaeche = raumlaenge * raumbreite
                wandflaeche1 = raumlaenge * raumhoehe
                wandflaeche2 = raumbreite * raumhoehe
                gesamt_wandflaeche = 2 * (wandflaeche1 + wandflaeche2)

                # Gesamtergebnis anzeigen
                aufmass_details = f"""
                Raummaße:
                Länge: {raumlaenge} m, Breite: {raumbreite} m, Höhe: {raumhoehe} m

                Bodenfläche: {bodenflaeche} m²
                Wandfläche (gesamt): {gesamt_wandflaeche} m²
                """
                messagebox.showinfo("Aufmaß-Ergebnis", aufmass_details)

                # Aufmaß in der Datenbank speichern
                kunde = combobox_kunde.get()
                datum = entry_startdatum.get()
                try:
                    self.cursor.execute('''
                        INSERT INTO aufmass (kunde, datum, raumlaenge, raumbreite, raumhoehe, bodenflaeche, wandflaeche)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (kunde, datum, raumlaenge, raumbreite, raumhoehe, bodenflaeche, gesamt_wandflaeche))
                    self.conn.commit()
                    messagebox.showinfo("Erfolg", "Aufmaß erfolgreich gespeichert!")
                except sqlite3.Error as e:
                    messagebox.showerror("Datenbankfehler", f"Fehler beim Speichern des Aufmaßes: {e}")
            except ValueError:
                messagebox.showerror("Fehler", "Bitte gültige Zahlen für die Raummaße eingeben.")

        # Button für Aufmaß hinzufügen
        Button(projekt_window, text="Aufmaß hinzufügen", command=aufmass_hinzufuegen).grid(row=10, column=0, columnspan=2, pady=10)

        # Aufmaß ändern
        def aufmass_aendern():
            selected_indices = listbox.curselection()

            if not selected_indices:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus der Liste aus.")
                return

            selected_item = listbox.get(selected_indices[0])
            projekt_name = selected_item.split(',')[0].split(':')[1].strip()

            self.cursor.execute("SELECT id, raumlaenge, raumbreite, raumhoehe FROM aufmass WHERE kunde = ? AND datum = ?", (combobox_kunde.get(), entry_startdatum.get()))
            aufmass_row = self.cursor.fetchone()

            if not aufmass_row:
                messagebox.showerror("Fehler", "Kein Aufmaß für dieses Projekt gefunden.")
                return

            aufmass_id, alte_laenge, alte_breite, alte_hoehe = aufmass_row

            neue_laenge = simpledialog.askfloat("Raummaß", "Raumlänge (m):", initialvalue=alte_laenge)
            neue_breite = simpledialog.askfloat("Raummaß", "Raumbreite (m):", initialvalue=alte_breite)
            neue_hoehe = simpledialog.askfloat("Raummaß", "Raumhöhe (m):", initialvalue=alte_hoehe)

            if None in (neue_laenge, neue_breite, neue_hoehe):
                messagebox.showerror("Fehler", "Bitte alle Raummaße eingeben.")
                return

            # Berechnungen für Bodenfläche und Wände
            bodenflaeche = neue_laenge * neue_breite
            wandflaeche1 = neue_laenge * neue_hoehe
            wandflaeche2 = neue_breite * neue_hoehe
            gesamt_wandflaeche = 2 * (wandflaeche1 + wandflaeche2)

            try:
                self.cursor.execute('''
                    UPDATE aufmass SET raumlaenge = ?, raumbreite = ?, raumhoehe = ?, bodenflaeche = ?, wandflaeche = ?
                    WHERE id = ?
                ''', (neue_laenge, neue_breite, neue_hoehe, bodenflaeche, gesamt_wandflaeche, aufmass_id))
                self.conn.commit()
                messagebox.showinfo("Erfolg", "Aufmaß erfolgreich aktualisiert!")
            except sqlite3.Error as e:
                messagebox.showerror("Datenbankfehler", f"Fehler beim Aktualisieren des Aufmaßes: {e}")

        # Button für Aufmaß ändern
        Button(projekt_window, text="Aufmaß ändern", command=aufmass_aendern).grid(row=11, column=0, columnspan=2, pady=10)

        def refresh_projekt_list():
            """Aktualisiert die Projektliste."""
            listbox.delete(0, END)
            self.cursor.execute("SELECT projekt_name, kunde, mitarbeiter FROM projekte")
            rows = self.cursor.fetchall()
            for row in rows:
                listbox.insert(END, f"Projekt: {row[0]}, Kunde: {row[1]}, Mitarbeiter: {row[2]}")

        def projekt_speichern():
            """Speichert ein neues Projekt oder aktualisiert ein bestehendes Projekt in der Datenbank und trägt es in den Kalender ein."""
            projektname = entry_projektname.get()
            kunde = combobox_kunde.get()  # Ausgewählter Kunde
            mitarbeiter = combobox_mitarbeiter.get()  # Ausgewählter Mitarbeiter
            startdatum = entry_startdatum.get()
            enddatum = entry_enddatum.get()
            beschreibung = entry_beschreibung.get()
            status = combobox_status.get()  # Projektstatus

            if not projektname:
                messagebox.showerror("Fehler", "Projektname darf nicht leer sein.")
                return

            # Prüfen, ob das Projekt bereits existiert
            self.cursor.execute("SELECT id FROM projekte WHERE projekt_name = ?", (projektname,))
            existing_project = self.cursor.fetchone()

            if existing_project:
                # Projekt existiert -> Update
                self.cursor.execute('''UPDATE projekte SET kunde = ?, mitarbeiter = ?, startdatum = ?, enddatum = ?, beschreibung = ?, status = ?
                                      WHERE projekt_name = ?''', (kunde, mitarbeiter, startdatum, enddatum, beschreibung, status, projektname))
                messagebox.showinfo("Erfolg", "Projekt aktualisiert!")
                kalender_plugin.update_project_in_calendar(projektname, startdatum, enddatum)  # Kalenderintegration
            else:
                # Projekt existiert nicht -> Neues Projekt einfügen
                self.cursor.execute('''INSERT INTO projekte (projekt_name, kunde, mitarbeiter, startdatum, enddatum, beschreibung, status)
                                      VALUES (?, ?, ?, ?, ?, ?, ?)''', (projektname, kunde, mitarbeiter, startdatum, enddatum, beschreibung, status))
                messagebox.showinfo("Erfolg", "Neues Projekt gespeichert!")
                kalender_plugin.add_project_to_calendar(projektname, startdatum, enddatum)  # Kalenderintegration

            self.conn.commit()
            refresh_projekt_list()

        def projekt_details(event):
            """Zeigt Details des ausgewählten Projekts an."""
            selected_indices = listbox.curselection()

            if not selected_indices:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus der Liste aus.")
                return

            selected_item = listbox.get(selected_indices[0])
            projekt_name = selected_item.split(',')[0].split(':')[1].strip()

            self.cursor.execute("SELECT * FROM projekte WHERE projekt_name = ?", (projekt_name,))
            row = self.cursor.fetchone()

            # Hole alle Artikel, die dem Projekt zugeordnet sind
            self.cursor.execute("SELECT art_nr, menge FROM projekt_artikel WHERE projekt_name = ?", (projekt_name,))
            artikel_rows = self.cursor.fetchall()
            artikel_details = "\n".join([f"Artikel: {artikel[0]}, Menge: {artikel[1]}" for artikel in artikel_rows])

            if row:
                details = f"Projektname: {row[1]}\nKunde: {row[2]}\nMitarbeiter: {row[3]}\nStartdatum: {row[4]}\nEnddatum: {row[5]}\nBeschreibung: {row[6]}\nStatus: {row[7]}\n\nArtikel:\n{artikel_details}"
                messagebox.showinfo("Projektdetails", details)

        def projekt_aendern():
            """Ändert ein ausgewähltes Projekt und aktualisiert die Kalenderanzeige."""
            selected_indices = listbox.curselection()

            if not selected_indices:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Projekt aus der Liste aus.")
                return

            selected_item = listbox.get(selected_indices[0])
            projekt_name = selected_item.split(',')[0].split(':')[1].strip()

            self.cursor.execute("SELECT * FROM projekte WHERE projekt_name = ?", (projekt_name,))
            row = self.cursor.fetchone()

            # Hole alle Artikel, die dem Projekt zugeordnet sind
            self.cursor.execute("SELECT art_nr, menge FROM projekt_artikel WHERE projekt_name = ?", (projekt_name,))
            artikel_rows = self.cursor.fetchall()

            if row:
                entry_projektname.delete(0, END)
                entry_projektname.insert(0, row[1])
                combobox_kunde.set(row[2])  # Kunde setzen
                combobox_mitarbeiter.set(row[3])  # Mitarbeiter setzen
                entry_startdatum.set_date(row[4])
                entry_enddatum.set_date(row[5])
                entry_beschreibung.delete(0, END)
                entry_beschreibung.insert(0, row[6])

                def update_projekt():
                    """Aktualisiert das Projekt in der Datenbank und im Kalender."""
                    projektname = entry_projektname.get()
                    kunde = combobox_kunde.get()  # Ausgewählter Kunde
                    mitarbeiter = combobox_mitarbeiter.get()  # Ausgewählter Mitarbeiter
                    startdatum = entry_startdatum.get()
                    enddatum = entry_enddatum.get()
                    beschreibung = entry_beschreibung.get()
                    status = combobox_status.get()

                    # Menge der Artikel überprüfen und anpassen
                    for artikel in artikel_rows:
                        art_nr, alte_menge = artikel
                        neue_menge = simpledialog.askinteger("Menge bearbeiten", f"Menge für Artikel {art_nr} ändern:", initialvalue=alte_menge)
                        if neue_menge is not None:
                            differenz = neue_menge - alte_menge
                            if differenz > 0:
                                # Erhöhte Menge -> Lagerbestand reduzieren
                                self.cursor.execute("UPDATE lager SET lagerbestand = lagerbestand - ? WHERE art_nr = ?", (differenz, art_nr))
                            elif differenz < 0:
                                # Verringerte Menge -> Lagerbestand wieder auffüllen
                                self.cursor.execute("UPDATE lager SET lagerbestand = lagerbestand + ? WHERE art_nr = ?", (-differenz, art_nr))

                            self.cursor.execute("UPDATE projekt_artikel SET menge = ? WHERE projekt_name = ? AND art_nr = ?", (neue_menge, projektname, art_nr))
                            refresh_projekt_list()
                    # Projekt aktualisieren
                    self.cursor.execute('''UPDATE projekte SET projekt_name = ?, kunde = ?, mitarbeiter = ?, startdatum = ?, enddatum = ?, beschreibung = ?, status = ?
                                          WHERE id = ?''', (projektname, kunde, mitarbeiter, startdatum, enddatum, beschreibung, status, row[0]))

                    self.conn.commit()
                    kalender_plugin.update_project_in_calendar(projektname, startdatum, enddatum)

                    messagebox.showinfo("Erfolg", "Projekt aktualisiert!")
                    refresh_projekt_list()

                Button(projekt_window, text="Projekt aktualisieren", command=update_projekt).grid(row=9, column=1)

        def projekt_loeschen():
            """Löscht das ausgewählte Projekt und entfernt es aus dem Kalender."""
            selected_item = listbox.get(listbox.curselection())
            projekt_name = selected_item.split(',')[0].split(':')[1].strip()

            # Stelle sicher, dass Artikel wieder ins Lager zurückgeführt werden
            self.cursor.execute("SELECT art_nr, menge FROM projekt_artikel WHERE projekt_name = ?", (projekt_name,))
            artikel_rows = self.cursor.fetchall()

            for artikel in artikel_rows:
                art_nr, menge = artikel
                # Artikel wieder ins Lager zurückführen
                self.cursor.execute("UPDATE lager SET lagerbestand = lagerbestand + ? WHERE art_nr = ?", (menge, art_nr))

            self.cursor.execute("DELETE FROM projekte WHERE projekt_name = ?", (projekt_name,))
            self.cursor.execute("DELETE FROM projekt_artikel WHERE projekt_name = ?", (projekt_name,))  # Löscht auch zugeordnete Artikel
            self.conn.commit()
            kalender_plugin.remove_project_from_calendar(projekt_name)  # Kalenderintegration
            messagebox.showinfo("Erfolg", "Projekt gelöscht!")
            refresh_projekt_list()

        def projekt_suchen():
            """Sucht ein Projekt nach Name oder Kunde."""
            suchbegriff = simpledialog.askstring("Projekt suchen", "Projektname oder Kunde eingeben:")
            if suchbegriff:
                listbox.delete(0, END)
                self.cursor.execute("SELECT projekt_name, kunde, mitarbeiter FROM projekte WHERE projekt_name LIKE ? OR kunde LIKE ?", (f"%{suchbegriff}%", f"%{suchbegriff}%"))
                rows = self.cursor.fetchall()
                for row in rows:
                    listbox.insert(END, f"Projekt: {row[0]}, Kunde: {row[1]}, Mitarbeiter: {row[2]}")

        Button(projekt_window, text="Projekt speichern", command=projekt_speichern).grid(row=12, column=0)
        Button(projekt_window, text="Projekt ändern", command=projekt_aendern).grid(row=12, column=1)
        Button(projekt_window, text="Projekt löschen", command=projekt_loeschen).grid(row=13, column=0)
        Button(projekt_window, text="Projekt suchen", command=projekt_suchen).grid(row=13, column=1)

        listbox.bind('<Double-1>', projekt_details)
        refresh_projekt_list()

# Datenbank für Aufmaß initialisieren
def initialize_aufmass_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS aufmass (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kunde TEXT,
            datum TEXT,
            raumlaenge REAL,
            raumbreite REAL,
            raumhoehe REAL,
            bodenflaeche REAL,
            wandflaeche REAL
        )
    ''')
    conn.commit()
    conn.close()

projekt_plugin = ProjektPlugin()
initialize_aufmass_database()
