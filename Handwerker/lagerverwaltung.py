import sqlite3
from tkinter import Toplevel, Listbox, Scrollbar, Button, simpledialog, END, messagebox
from plugin_manager import plugin_manager

DB_PATH = 'handwerker.db'

class LagerPlugin:
    def __init__(self):
        plugin_manager.register_plugin('Lagerverwaltung', self)
        plugin_manager.register_hook('on_article_add', self.on_article_added)
        self.listbox = None  # Hier wird die Listbox als Instanzvariable definiert

    def open_lagerverwaltung(self):
        """Öffnet das Fenster für die Lagerverwaltung"""
        lager_window = Toplevel()
        lager_window.title("Lagerverwaltung")

        # Listbox als Instanzvariable speichern
        self.listbox = Listbox(lager_window, width=100)
        self.listbox.pack(side="left", fill="y")
        self.listbox.bind('<Double-1>', self.artikel_details)

        scrollbar = Scrollbar(lager_window, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")

        self.listbox.config(yscrollcommand=scrollbar.set)

        Button(lager_window, text="Artikel hinzufügen", command=self.artikel_hinzufuegen).pack(pady=5)
        Button(lager_window, text="Artikel entnehmen", command=self.artikel_entnehmen).pack(pady=5)
        Button(lager_window, text="Bestand bearbeiten", command=self.artikel_bestand_bearbeiten).pack(pady=5)
        Button(lager_window, text="Artikel suchen", command=self.artikel_suchen).pack(pady=5)
        Button(lager_window, text="Artikel löschen", command=self.artikel_loeschen).pack(pady=5)

        self.refresh_lager_list()

    def refresh_lager_list(self):
        """Aktualisiert die Liste aller Artikel im Lager."""
        self.listbox.delete(0, END)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT art_nr, name, lagerbestand FROM lager")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self.listbox.insert(END, f"Art. Nr.: {row[0]}, Name: {row[1]}, Lagerbestand: {row[2]}")

    def artikel_hinzufuegen(self):
        """Fügt einen neuen Artikel ins Lager hinzu."""
        art_nr = simpledialog.askstring("Artikel hinzufügen", "Art. Nr.:")
        beschreibung = simpledialog.askstring("Artikel hinzufügen", "Beschreibung:")
        lagerbestand = simpledialog.askinteger("Artikel hinzufügen", "Lagerbestand:")
        if art_nr and beschreibung and lagerbestand is not None:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO lager (art_nr, name, lagerbestand)
                              VALUES (?, ?, ?)''', (art_nr, beschreibung, lagerbestand))
            conn.commit()
            conn.close()
            messagebox.showinfo("Erfolg", "Artikel hinzugefügt!")
            plugin_manager.trigger_hook('on_article_add', {'art_nr': art_nr, 'name': beschreibung})
            self.refresh_lager_list()

    def artikel_entnehmen(self):
        """Entnimmt eine bestimmte Menge eines Artikels."""
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
            self.refresh_lager_list()

    def artikel_bestand_bearbeiten(self):
        """Aktualisiert den Bestand eines Artikels."""
        art_nr = simpledialog.askstring("Bestand bearbeiten", "Art. Nr.:")
        neuer_bestand = simpledialog.askinteger("Bestand bearbeiten", "Neuer Lagerbestand:")
        if art_nr and neuer_bestand is not None:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("UPDATE lager SET lagerbestand = ? WHERE art_nr = ?", (neuer_bestand, art_nr))
            conn.commit()
            conn.close()
            messagebox.showinfo("Erfolg", "Lagerbestand aktualisiert!")
            self.refresh_lager_list()

    def artikel_suchen(self):
        """Sucht einen Artikel nach Artikelnummer oder Name."""
        suchbegriff = simpledialog.askstring("Artikel suchen", "Art. Nr. oder Name eingeben:")
        if suchbegriff:
            self.listbox.delete(0, END)
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT art_nr, name, lagerbestand FROM lager WHERE art_nr LIKE ? OR name LIKE ?", (f"%{suchbegriff}%", f"%{suchbegriff}%"))
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                self.listbox.insert(END, f"Art. Nr.: {row[0]}, Beschreibung: {row[1]}, Lagerbestand: {row[2]}")

    def artikel_details(self, event):
        """Zeigt Details eines ausgewählten Artikels an."""
        selected_item = self.listbox.get(self.listbox.curselection())
        art_nr = selected_item.split(',')[0].split(':')[1].strip()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lager WHERE art_nr = ?", (art_nr,))
        row = cursor.fetchone()
        conn.close()
        if row:
            details = f"Art. Nr.: {row[1]}\nName: {row[2]}\nOberfläche: {row[3]}\nFormat: {row[4]}\nStärke: {row[5]}\nKategorie: {row[7]}\nLagerbestand: {row[10]}\nLieferant: {row[11]}\nEinkaufspreis: {row[12]}\nVerkaufspreis: {row[13]}\nLagerort: {row[20]}"
            messagebox.showinfo("Artikeldetails", details)

    def artikel_loeschen(self):
        """Löscht einen Artikel aus dem Lager, wenn einer ausgewählt wurde."""
        selected_indices = self.listbox.curselection()
    
        if not selected_indices:
            messagebox.showerror("Fehler", "Bitte wählen Sie einen Artikel aus der Liste aus.")
            return

        selected_item = self.listbox.get(selected_indices[0])
        art_nr = selected_item.split(',')[0].split(':')[1].strip()
    
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lager WHERE art_nr = ?", (art_nr,))
        conn.commit()
        conn.close()
    
        messagebox.showinfo("Erfolg", "Artikel gelöscht!")
        self.refresh_lager_list()


    def on_article_added(self, article):
        """Wird aufgerufen, wenn ein Artikel hinzugefügt wurde (Hook)."""
        print(f'Neuer Artikel hinzugefügt: {article["name"]}')

# Lager Plugin Instanz
lager_plugin = LagerPlugin()
