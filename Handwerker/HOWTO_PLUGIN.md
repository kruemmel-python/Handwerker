### Anleitung: Erstellen eines Plugins für das Handwerker-Software-Projekt

Die Handwerker-Software ist modular aufgebaut und basiert auf einem Plugin-System. Dies ermöglicht es Entwicklern, neue Funktionalitäten hinzuzufügen, ohne den Kerncode des Programms zu verändern. Diese Anleitung führt dich Schritt für Schritt durch den Prozess, wie du ein Plugin für das Handwerker-Software-Projekt schreiben kannst.

#### Voraussetzungen:
- Python 3.x installiert
- Grundkenntnisse in Python-Programmierung
- Das Projekt auf deinem lokalen Rechner mit einem Git-Repository eingerichtet
- Verständnis des Plugin-Managers des Projekts

### Plugin-Manager verstehen

Der Plugin-Manager verwaltet die Registrierung und Ausführung von Plugins. Er erlaubt es, verschiedene Plugins modular zu entwickeln und sie dynamisch zur Laufzeit in das Programm zu integrieren.

### Struktur eines Plugins

Jedes Plugin muss die folgenden Elemente enthalten:

1. **Plugin-Registrierung**: Das Plugin muss sich beim Plugin-Manager registrieren.
2. **Funktionen des Plugins**: Das Plugin kann beliebige Funktionen bereitstellen, die bei Bedarf vom Hauptprogramm oder anderen Plugins aufgerufen werden.
3. **Hook-Registrierung (optional)**: Plugins können Hooks bereitstellen, die an bestimmten Ereignissen im Hauptprogramm ausgeführt werden.

### Schritt 1: Erstellen des Plugin-Skeletts

Erstelle eine neue Python-Datei in dem Verzeichnis `plugins/` (oder einem entsprechenden Plugin-Verzeichnis). Diese Datei wird dein Plugin enthalten.

#### Beispiel: `mein_plugin.py`

```python
from plugin_manager import plugin_manager

class MeinPlugin:
    def __init__(self):
        # Plugin beim Plugin-Manager registrieren
        plugin_manager.register_plugin('MeinPlugin', self)

        # Optional: Ein Hook registrieren
        plugin_manager.register_hook('on_task_completed', self.on_task_completed)

    def run_task(self):
        # Beispiel einer Funktion des Plugins
        print("Das Plugin führt eine Aufgabe aus!")

    def on_task_completed(self, task_data):
        # Ein Hook, der aufgerufen wird, wenn eine Aufgabe im Hauptprogramm abgeschlossen wird
        print(f"Aufgabe abgeschlossen: {task_data}")

# Plugin-Instanz erstellen
mein_plugin = MeinPlugin()
```

### Schritt 2: Plugin registrieren

Damit dein Plugin vom Hauptprogramm erkannt wird, muss es sich beim Plugin-Manager registrieren. Dies geschieht in der `__init__()`-Methode, indem du die Methode `register_plugin()` des Plugin-Managers aufrufst.

```python
plugin_manager.register_plugin('MeinPlugin', self)
```

Der erste Parameter ist der Name des Plugins (dieser sollte eindeutig sein), und der zweite Parameter ist die Plugin-Instanz selbst.

### Schritt 3: Funktionalitäten definieren

Dein Plugin kann beliebige Funktionen enthalten. Diese Funktionen können vom Hauptprogramm oder anderen Plugins aufgerufen werden. In unserem Beispiel enthält das Plugin eine Methode `run_task()`, die eine Aufgabe ausführt.

```python
def run_task(self):
    print("Das Plugin führt eine Aufgabe aus!")
```

### Schritt 4: Hooks verwenden (optional)

Hooks ermöglichen es einem Plugin, auf Ereignisse im Hauptprogramm zu reagieren. Dies ist besonders nützlich, wenn dein Plugin auf bestimmte Aktionen im System reagieren soll, z.B. wenn ein neues Projekt erstellt oder ein Auftrag abgeschlossen wird.

Um einen Hook zu registrieren, verwende die Methode `register_hook()` des Plugin-Managers:

```python
plugin_manager.register_hook('on_task_completed', self.on_task_completed)
```

Hierbei wird die Methode `on_task_completed()` als Hook registriert, der aufgerufen wird, wenn die Aufgabe `on_task_completed` vom Hauptprogramm abgeschlossen ist.

### Schritt 5: Plugin testen

Nachdem du das Plugin erstellt hast, musst du sicherstellen, dass es richtig funktioniert. Starte die Anwendung und prüfe, ob das Plugin geladen wird und die entsprechenden Funktionen ausführt.

Falls dein Plugin von Hooks abhängig ist, musst du sicherstellen, dass das Hauptprogramm die entsprechenden Hooks auslöst. Beispielsweise könnte im Hauptprogramm eine Aufgabe wie folgt abgeschlossen werden:

```python
plugin_manager.trigger_hook('on_task_completed', {'task_name': 'Demo-Aufgabe'})
```

### Beispiel: Plugin für Rechnungen

Hier ist ein weiteres Beispiel, bei dem ein Plugin für die Handhabung von Rechnungen erstellt wird.

#### Beispiel: `rechnungen_plugin.py`

```python
import os
from plugin_manager import plugin_manager

class RechnungenPlugin:
    def __init__(self):
        # Plugin registrieren
        plugin_manager.register_plugin('RechnungenPlugin', self)

    def erstelle_rechnung(self, projekt_name, betrag):
        # Rechnung erstellen und speichern
        rechnungspfad = f"rechnungen/{projekt_name}_rechnung.txt"
        with open(rechnungspfad, 'w') as file:
            file.write(f"Rechnung für Projekt: {projekt_name}\nBetrag: {betrag} EUR\n")
        print(f"Rechnung für Projekt '{projekt_name}' erstellt!")

    def zeige_rechnungen(self):
        # Alle Rechnungen anzeigen
        print("Verfügbare Rechnungen:")
        for rechnung in os.listdir('rechnungen'):
            print(rechnung)

# Plugin-Instanz erstellen
rechnungen_plugin = RechnungenPlugin()
```

In diesem Plugin:
- Wird eine Rechnung für ein Projekt erstellt und in einem Dateipfad gespeichert.
- Gibt es eine Methode zum Anzeigen aller erstellten Rechnungen.

### Schritt 6: Erweiterungsideen

Das Plugin-System ist äußerst flexibel und ermöglicht dir, die Anwendung um viele verschiedene Module zu erweitern. Hier sind einige Ideen:

1. **Mitarbeiter-Plugin**: Verwaltung von Mitarbeiterdaten, Arbeitszeiten und Gehältern.
2. **Kunden-Plugin**: Verwaltung von Kundendaten, Aufträgen und Anfragen.
3. **Rechnungs-Plugin**: Erstellung und Verwaltung von Rechnungen für abgeschlossene Projekte.
4. **Mahnungs-Plugin**: Automatische Erstellung und Versand von Mahnungen bei Zahlungsverzug.
5. **Angebots-Plugin**: Erstellung von Angeboten basierend auf den Projektdaten.
6. **Kassensystem-Plugin**: Integration eines Kassensystems für direkte Zahlungen.
7. **Lager-Plugin**: Erweiterung der bestehenden Lagerverwaltung, um detaillierte Lagerbewegungen und Inventuren zu ermöglichen.

### Schritt 7: Ein Plugin einbinden

Um das Plugin in das Hauptprogramm zu integrieren, wird es automatisch vom `plugin_manager` erkannt, wenn es im richtigen Verzeichnis liegt und korrekt registriert ist. Der `plugin_manager` lädt alle Plugins beim Start des Programms.

### Fazit

Dank des modularen Aufbaus kannst du schnell neue Funktionen zur Handwerker-Software hinzufügen, ohne den bestehenden Code zu verändern. Dies macht das System flexibel und erweiterbar. Mit den oben genannten Schritten kannst du dein eigenes Plugin erstellen und problemlos in die Anwendung integrieren.
