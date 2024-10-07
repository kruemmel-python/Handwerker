import csv
import os
import sqlite3
from plugin_manager import plugin_manager

DB_PATH = 'handwerker.db'
LAGER_CSV_PATH = 'lager.csv'

class CSVImportPlugin:
    def __init__(self):
        plugin_manager.register_plugin('CSVImport', self)

    def create_lager_table_if_not_exists(self):
        """Erstellt die Tabelle 'lager', falls sie nicht existiert."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lager (
                art_nr TEXT PRIMARY KEY,
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
            )
        ''')
        conn.commit()
        conn.close()

    def import_lager_csv_to_db(self):
        """Importiert die Lagerdaten aus der CSV-Datei in die Datenbank."""
        self.create_lager_table_if_not_exists()  # Stelle sicher, dass die Tabelle existiert

        if not os.path.exists(LAGER_CSV_PATH):
            print("Lager CSV-Datei nicht gefunden.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        with open(LAGER_CSV_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            count = 0  # Zähler für importierte Datensätze
            for row in reader:
                cursor.execute('''
                    INSERT OR REPLACE INTO lager (
                        art_nr, name, oberflaeche, format_in_mm, staerke_in_mm, artikel_id, kategorie, mass, gewicht, lagerbestand,
                        lieferant, einkaufspreis, verkaufspreis, bestellnummer_lieferant, mindestbestellmenge, maximaler_lagerbestand,
                        lieferzeit, verbrauchseinheit, verfallsdatum, lagerort, produktbild, sicherheitsdatenblatt, anwendungsbereich
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('Art. Nr.', ''),
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
                    row.get('Anwendungsbereich', '')
                ))
                count += 1  # Zähler erhöhen

        conn.commit()
        conn.close()
        print(f"{count} Lager-Datensätze aus der CSV-Datei erfolgreich importiert.")

# Plugin-Instanz erstellen
csv_import_plugin = CSVImportPlugin()

# CSV-Import für Lagerdaten ausführen
csv_import_plugin.import_lager_csv_to_db()