import csv
import os
import sqlite3
from plugin_manager import plugin_manager

DB_PATH = 'handwerker.db'
CSV_PATH = 'lager.csv'

class CSVImportPlugin:
    def __init__(self):
        plugin_manager.register_plugin('CSVImport', self)

    def import_csv_to_db(self):
        if not os.path.exists(CSV_PATH):
            print("CSV-Datei nicht gefunden.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            count = 0  # Zähler für importierte Datensätze
            for row in reader:
                cursor.execute('''INSERT INTO lager (art_nr, name, oberflaeche, format_in_mm, staerke_in_mm, artikel_id, kategorie, mass, gewicht, lagerbestand, lieferant, einkaufspreis, verkaufspreis, bestellnummer_lieferant, mindestbestellmenge, maximaler_lagerbestand, lieferzeit, verbrauchseinheit, verfallsdatum, lagerort, produktbild, sicherheitsdatenblatt, anwendungsbereich)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (row.get('Art. Nr.', ''),
                               row.get('Name', ''),
                               row.get('Oberfläche', ''),
                               row.get('Format in mm', ''),
                               row.get('Stärke in mm', '0'),
                               row.get('ArtikelID', ''),
                               row.get('Kategorie', ''),
                               row.get('Maße', ''),
                               row.get('Gewicht', '0'),
                               row.get('Lagerbestand', 0),
                               row.get('Lieferant', ''),
                               row.get('Einkaufspreis', '0.0'),
                               row.get('Verkaufspreis', '0.0'),
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
                count += 1  # Erhöhe den Zähler für jeden importierten Datensatz

        conn.commit()
        conn.close()
        print(f"{count} Datensätze aus der CSV-Datei erfolgreich importiert.")

csv_import_plugin = CSVImportPlugin()
