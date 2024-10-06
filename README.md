
---

# Handwerker Projektverwaltung

Ein **modulares** Projektverwaltungssystem für Handwerksbetriebe, das auf einer **Plugin-Basis** aufbaut. Dieses System erlaubt es, Projekte, Kunden, Mitarbeiter und Lagerbestände effizient zu verwalten. Es ist in **Python** entwickelt und verwendet **SQLite** als Datenbank zur Speicherung von Projekt- und Lagerinformationen.

## Projektübersicht

Das **Handwerker Projektverwaltungssystem** bietet eine intuitive Benutzeroberfläche zur Verwaltung von Handwerksprojekten, Materialien und Kunden. Es erlaubt Benutzern:

- **Projekte** zu erstellen, zu bearbeiten und zu löschen.
- **Materialien aus dem Lager** hinzuzufügen und deren Bestände automatisch anzupassen.
- **Projektstatus** zu verwalten (Offen, Beendet, Anfrage).
- Eine **Kalenderintegration** zur Verfolgung von Projekten zu nutzen.
- Eine **Lagerverwaltung**, die Materialbestände in Echtzeit anpasst, wenn Projekte bearbeitet oder gelöscht werden.
  
## Funktionen

### 1. **Projektverwaltung**
   - **Erstellen**: Projekte können angelegt werden, indem der Projektname, Kunde, Mitarbeiter, Start- und Enddatum, Beschreibung sowie Projektstatus eingegeben werden.
   - **Ändern**: Bereits bestehende Projekte können bearbeitet werden, wobei Änderungen an der Menge von Materialien im Projekt sofort im Lagerbestand angepasst werden.
   - **Löschen**: Projekte können vollständig gelöscht werden. Reservierte Materialien werden automatisch wieder dem Lagerbestand hinzugefügt.
   
### 2. **Lagerverwaltung**
   - **Artikel hinzufügen**: Es können neue Artikel ins Lager eingepflegt werden.
   - **Lagerbestand anpassen**: Wird ein Material zu einem Projekt hinzugefügt oder entfernt, wird der Lagerbestand automatisch aktualisiert.
   - **Artikel suchen**: Ermöglicht eine schnelle Suche nach Artikeln im Lager.

### 3. **Kalenderintegration**
   - Projekte werden automatisch im Kalender angezeigt und Änderungen an Projekten aktualisieren die Kalenderansicht.

### 4. **CSV-Import**
   - Import von Artikeldaten über eine CSV-Datei, die die Lagerverwaltung initialisiert und den Lagerbestand auffüllt, wenn die Datenbank leer ist.

## Architektur

Das Projekt basiert auf einer **modularen Plugin-Struktur**, was bedeutet, dass jede Funktion in einem separaten **Plugin** gekapselt ist. Dies fördert die Erweiterbarkeit und Wartbarkeit des Codes. Die wichtigsten Module sind:

### Plugins

- **Projektverwaltung**: Verwaltet die Erstellung, Bearbeitung und Löschung von Projekten.
- **Lagerverwaltung**: Verwalten von Materialien, Lagerbeständen und Artikelsuchen.
- **Kalenderplugin**: Ermöglicht die Integration von Projektdaten in eine Kalenderansicht.
- **CSV-Import**: Ermöglicht den Import von Artikeldaten aus CSV-Dateien.
- **Datenbankplugin**: Verwalten der SQLite-Datenbank und Erstellen der notwendigen Tabellen.

## Installation

### Voraussetzungen

- **Python 3.12+**
- **Tkinter** (für die GUI)
- **SQLite** (für die Datenbank)

### Setup

1. **Clone das Repository**:
    ```bash
    git clone https://github.com/kruemmel-python/Handwerker.git
    ```

2. **Abhängigkeiten installieren**:
   Stelle sicher, dass die benötigten Bibliotheken installiert sind. Falls nicht:
   ```bash
   pip install tk
   ```

3. **CSV-Datei für Lagerbestand**:
   Stelle sicher, dass sich eine CSV-Datei namens `lager.csv` im Projektverzeichnis befindet. Diese Datei wird verwendet, um initiale Lagerdaten zu importieren, falls das Lager leer ist.

4. **Starten der Anwendung**:
   Starte die Anwendung über die Kommandozeile:
   ```bash
   python main_app.py
   ```

## Projektstruktur

Das Projekt folgt einer klar strukturierten Modularität, was bedeutet, dass jede Funktion in einem separaten Modul (Plugin) gekapselt ist. Dies fördert die Erweiterbarkeit und Wartbarkeit des Codes. Die wichtigsten Module sind:

```plaintext
.
├── Handwerker.pyproj         # Projektdatei
├── csv_import.py             # Plugin für CSV-Import
├── database.py               # Datenbank Plugin
├── gui.py                    # Haupt-GUI Logik
├── handwerker.db             # SQLite-Datenbankdatei
├── kalender.py               # Kalenderplugin für Projektintegration
├── lager.csv                 # CSV-Datei für Lagerartikel
├── lagerverwaltung.py        # Plugin für Lagerverwaltung
├── login.py                  # Login-Verwaltung
├── main_app.py               # Startpunkt der Anwendung
├── plugin_manager.py         # Plugin-Manager, der Plugins registriert und verwaltet
└── projektverwaltung.py      # Plugin für die Projektverwaltung
```

### Modulare Architektur

Die Verwendung von Plugins ermöglicht die einfache Erweiterung des Systems durch das Hinzufügen neuer Funktionen. Jedes Plugin wird über den **Plugin Manager** registriert, wodurch die Verwaltung zentralisiert wird. Der Plugin-Manager sorgt dafür, dass alle Plugins zur Laufzeit geladen und verwendet werden können.

### Vorteile der Modularität

- **Erweiterbarkeit**: Neue Funktionen können als Plugins hinzugefügt werden, ohne den bestehenden Code zu ändern.
- **Wartbarkeit**: Jedes Modul ist unabhängig und kapselt seine eigene Funktionalität, was die Fehlerbehebung vereinfacht.
- **Flexibilität**: Verschiedene Teams oder Entwickler können an unterschiedlichen Modulen arbeiten, ohne Konflikte zu verursachen.

## Verwendung

### Projekte erstellen

1. Klicke auf "Projekt erstellen".
2. Fülle die Projektdetails wie Name, Kunde, Mitarbeiter, Startdatum und Enddatum aus.
3. Füge Artikel aus dem Lager zum Projekt hinzu.
4. Speichere das Projekt und es wird im Kalender sowie in der Liste der laufenden Projekte angezeigt.

### Lager verwalten

1. Öffne die Lagerverwaltung.
2. Füge neue Artikel hinzu oder suche nach vorhandenen Artikeln.
3. Bearbeite Lagerbestände manuell oder lass sie automatisch über die Projektverwaltung anpassen.

## Mögliche Erweiterungen

Um die Anwendung zu einer vollwertigen **Handwerkersoftware** zu erweitern, können folgende Funktionen hinzugefügt werden:

### 1. **Mitarbeiterverwaltung**
   - **Mitarbeiterdaten** speichern: Persönliche Informationen, Arbeitszeiten und Qualifikationen.
   - **Arbeitszeitverwaltung**: Ein Plugin, das es ermöglicht, Arbeitsstunden für Projekte zu erfassen und zu verwalten.
   - **Urlaubs- und Abwesenheitsmanagement**: Verwaltung von Urlaubsanträgen und Krankheitsausfällen.
  
### 2. **Kundendatenverwaltung**
   - Speichere **Kundendaten**, um eine Historie der Aufträge und Projekte zu führen.
   - **CRM-Funktionalitäten**: Eine Kundenhistorie mit Angeboten, Projekten und Rechnungen könnte integriert werden.

### 3. **Rechnungen & Mahnungen**
   - **Rechnungserstellung**: Automatisierte Rechnungsgenerierung basierend auf abgeschlossenen Projekten und der verwendeten Materialien.
   - **Mahnwesen**: Verwalte offene Rechnungen und generiere Mahnungen bei Zahlungsverzug.

### 4. **Angebote**
   - **Angebotserstellung**: Plugin zur Erstellung von Angeboten für Kunden, die in Aufträge umgewandelt werden können.
   - **PDF-Export**: Angebote und Rechnungen könnten automatisch als PDF erstellt und per E-Mail versendet werden.

### 5. **Kassensystem**
   - Ein **Kassensystem** könnte integriert werden, das Zahlungen in Echtzeit erfasst und den Lagerbestand entsprechend anpasst.
   - **Belege drucken**: Druckfunktion für Quittungen und Rechnungen direkt aus dem System.

### 6. **Mobile App Integration**
   - Eine mobile App für Mitarbeiter, um Arbeitszeiten zu erfassen, Projekte zu verwalten und den Lagerbestand einzusehen.
   - Echtzeit-Synchronisation zwischen App und Hauptsystem.

### 7. **Berichterstattung & Analysen**
   - Ein Plugin für **Berichte und Statistiken** über abgeschlossene Projekte, finanzielle Auswertungen und Lagerbewegungen.
   - Integration von **Dashboards** zur Visualisierung von Projektfortschritt, Lagerbeständen und Umsätzen.

### 8. **Kundenportal**
   - Ein **Online-Kundenportal**, in dem Kunden den Status ihrer Projekte sehen, Rechnungen herunterladen und Feedback geben können.

### 9. **Datensicherung**
   - Ein **Datensicherungsplugin**, das automatisch Backups der Datenbank erstellt und eine Wiederherstellung bei Datenverlust ermöglicht.

### 10. **Cloud-Integration**
   - Integration eines **Cloud-basierten Speichersystems**, um Projekte und Lagerbestände online zu verwalten und von verschiedenen Standorten darauf zuzugreifen.

## Contributing

Beiträge zu diesem Projekt sind willkommen! Wenn du neue Features hinzufügen oder Fehler beheben möchtest, kannst du einen Pull-Request erstellen oder ein Issue melden.

## Lizenz

Dieses Projekt steht unter der **MIT Lizenz**.

---
