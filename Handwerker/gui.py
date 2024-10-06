from tkinter import Tk, Button
from plugin_manager import plugin_manager
from kalender import kalender_plugin
from lagerverwaltung import lager_plugin
from projektverwaltung import projekt_plugin

class GuiPlugin:
    def __init__(self):
        # Registriere das Plugin beim Plugin-Manager
        plugin_manager.register_plugin('GUI', self)
        self.main_app = None  # Hauptfenster wird hier zunächst nicht erstellt

    def initialize_gui(self):
        """Initialisiert die GUI-Komponenten und Plugins."""
        self.main_app = Tk()  # Hauptfenster wird hier nach dem Login erstellt
        self.main_app.title("Handwerkersoftware")

        # Initialisiert den Kalender
        kalender_plugin.initialize_calendar(self.main_app)

        # Erstellt Buttons für die Lager- und Projektverwaltung
        Button(self.main_app, text="Lagerverwaltung", command=lager_plugin.open_lagerverwaltung).pack(pady=10)
        Button(self.main_app, text="Projektverwaltung", command=projekt_plugin.open_projektverwaltung).pack(pady=10)

    def run(self):
        """Startet die Haupt-Event-Schleife der GUI."""
        if self.main_app is not None:
            self.main_app.mainloop()

# GUI-Plugin erstellen
gui_plugin = GuiPlugin()

def start_gui():
    """Startet die GUI."""
    gui_plugin.initialize_gui()
    gui_plugin.run()
