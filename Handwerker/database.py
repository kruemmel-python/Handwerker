import sqlite3  # sqlite3 importieren
from plugin_manager import plugin_manager
from csv_import import CSVImportPlugin  # CSV Import Plugin importieren

DB_PATH = 'handwerker.db'

class DatabasePlugin:
    def __init__(self):
        plugin_manager.register_plugin('Database', self)

    def initialize_database(self):
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

        # Tabelle Projektverwaltung erstellen (Sicherstellen, dass die Tabelle existiert)
        cursor.execute('''CREATE TABLE IF NOT EXISTS projekte (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            projekt_name TEXT,
                            kunde TEXT,
                            mitarbeiter TEXT,
                            startdatum TEXT,
                            enddatum TEXT,
                            beschreibung TEXT,
                            status TEXT  -- Status des Projekts (Offen, Beendet, Anfrage)
                        )''')

        # Tabelle projekt_artikel hinzufügen, um Artikel einem Projekt zuzuordnen
        cursor.execute('''CREATE TABLE IF NOT EXISTS projekt_artikel (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            projekt_name TEXT,
                            art_nr TEXT,
                            menge INTEGER,
                            FOREIGN KEY (projekt_name) REFERENCES projekte(projekt_name),
                            FOREIGN KEY (art_nr) REFERENCES lager(art_nr)
                        )''')

        conn.commit()

        # Prüfen, ob Daten in der Lager-Tabelle vorhanden sind
        cursor.execute("SELECT COUNT(*) FROM lager")
        if cursor.fetchone()[0] == 0:
            print("Lager ist leer. CSV-Daten werden importiert.")
            csv_import_plugin.import_csv_to_db()  # Importiere CSV-Daten, wenn Tabelle leer ist
        else:
            print("Daten bereits in der Lager-Tabelle vorhanden, CSV-Import übersprungen.")

        conn.close()

database_plugin = DatabasePlugin()
