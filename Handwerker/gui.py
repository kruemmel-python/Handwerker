from tkinter import Tk, Menu
from plugin_manager import plugin_manager
from kalender import kalender_plugin
from lagerverwaltung import lager_plugin
from projektverwaltung import projekt_plugin
from kunden import KundenPlugin  # Stelle sicher, dass KundenPlugin importiert wird
from personal import MitarbeiterPlugin
from zeiterfassung import ZeiterfassungPlugin

class GuiPlugin:
    def __init__(self):
        # Registriere das Plugin beim Plugin-Manager
        plugin_manager.register_plugin('GUI', self)
        self.main_app = None  # Hauptfenster wird hier zunächst nicht erstellt
        self.kunden_plugin = KundenPlugin()  # Instanz von KundenPlugin erstellen
        self.mitarbeiter_plugin = MitarbeiterPlugin()  # Instanz von MitarbeiterPlugin erstellen
        self.zeiterfassung_plugin = ZeiterfassungPlugin()  # Instanz des ZeiterfassungPlugins erstellen

    def initialize_gui(self):
        """Initialisiert die GUI-Komponenten und Plugins."""
        self.main_app = Tk()  # Hauptfenster wird hier nach dem Login erstellt
        self.main_app.title("Handwerkersoftware")

        # Initialisiert den Kalender
        kalender_plugin.initialize_calendar(self.main_app)

        # Menüleiste erstellen
        menuleiste = Menu(self.main_app)
        self.main_app.config(menu=menuleiste)

        # "Verwaltung"-Menü hinzufügen
        verwaltung_menu = Menu(menuleiste, tearoff=0)
        menuleiste.add_cascade(label="Verwaltung", menu=verwaltung_menu)

        # Einträge für Verwaltung hinzufügen
        verwaltung_menu.add_command(label="Lagerverwaltung", command=lager_plugin.open_lagerverwaltung)
        verwaltung_menu.add_command(label="Projektverwaltung", command=projekt_plugin.open_projektverwaltung)
        verwaltung_menu.add_command(label="Personalverwaltung", command=self.mitarbeiter_plugin.open_mitarbeiterverwaltung)
        verwaltung_menu.add_command(label="Kundenverwaltung", command=self.kunden_plugin.open_kundenverwaltung)
        
        # Zeiterfassung zum Menü hinzufügen
        verwaltung_menu.add_command(label="Zeiterfassung", command=lambda: self.zeiterfassung_plugin.open_zeiterfassung(self.main_app))

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
