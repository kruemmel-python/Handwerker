from gui import start_gui
from login import login_plugin
from database import database_plugin  # Datenbank-Plugin importieren

def main_app():
    """Startet die Anwendung nach erfolgreichem Login."""
    database_plugin.initialize_database()  # Datenbank-Initialisierung
    start_gui()  # Startet die GUI nach erfolgreichem Login

if __name__ == "__main__":
    # Login-Funktion aufrufen und danach die Hauptanwendung öffnen
    login_plugin.login(main_app)
