from tkinter import Frame
from tkcalendar import Calendar
from plugin_manager import plugin_manager
from datetime import datetime, timedelta  # timedelta hinzufügen

class KalenderPlugin:
    def __init__(self):
        plugin_manager.register_plugin('Kalender', self)
        plugin_manager.register_hook('on_article_add', self.on_article_add)
        self.cal = None  # Kalender-Objekt

    def initialize_calendar(self, main_app):
        """Initialisiert den Kalender in der Hauptanwendung."""
        frame_calendar = Frame(main_app)
        frame_calendar.pack(pady=20)
        self.cal = Calendar(frame_calendar, selectmode='day', year=2024, month=10, day=5)
        self.cal.pack()

    def add_project_to_calendar(self, projektname, startdatum, enddatum):
        """Fügt ein Projekt in den Kalender ein."""
        start = datetime.strptime(startdatum, '%Y-%m-%d').date()
        end = datetime.strptime(enddatum, '%Y-%m-%d').date()
        current_date = start

        # Füge das Projekt zu jedem Tag im Zeitraum zwischen Startdatum und Enddatum hinzu
        while current_date <= end:
            self.cal.calevent_create(current_date, projektname, 'Projekt')
            current_date += timedelta(days=1)

        print(f'Projekt {projektname} von {startdatum} bis {enddatum} in den Kalender eingetragen.')

    def update_project_in_calendar(self, projektname, startdatum, enddatum):
        """Aktualisiert ein Projekt im Kalender."""
        self.remove_project_from_calendar(projektname)  # Erst entfernen
        self.add_project_to_calendar(projektname, startdatum, enddatum)  # Dann neu hinzufügen

    def remove_project_from_calendar(self, projektname):
        """Entfernt ein Projekt aus dem Kalender."""
        events = self.cal.get_calevents()
        for event in events:
            if self.cal.calevent_cget(event, 'text') == projektname:
                self.cal.calevent_remove(event)

        print(f'Projekt {projektname} aus dem Kalender entfernt.')

    def on_article_add(self, article):
        """Wird aufgerufen, wenn ein Artikel hinzugefügt wird (Hook)."""
        print(f'Kalender-Plugin: Artikel {article["name"]} wurde hinzugefügt.')

kalender_plugin = KalenderPlugin()
