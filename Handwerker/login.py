from tkinter import Tk, Label, Entry, Button, messagebox
from plugin_manager import plugin_manager

class LoginPlugin:
    def __init__(self):
        plugin_manager.register_plugin('Login', self)

    def login(self, on_success):
        def check_login():
            username = entry_username.get()
            password = entry_password.get()

            if username == "admin" and password == "admin":
                messagebox.showinfo("Login erfolgreich", "Willkommen!")
                root.destroy()  # Schließt das Login-Fenster
                on_success()  # Ruft die Funktion auf, die die Hauptanwendung öffnet
            else:
                messagebox.showerror("Fehler", "Ungültiger Benutzername oder Passwort")

        root = Tk()
        root.title("Anmeldung")
        Label(root, text="Benutzername").grid(row=0, column=0)
        entry_username = Entry(root)
        entry_username.grid(row=0, column=1)
        Label(root, text="Passwort").grid(row=1, column=0)
        entry_password = Entry(root, show="*")
        entry_password.grid(row=1, column=1)
        Button(root, text="Login", command=check_login).grid(row=2, column=1)
        root.mainloop()

login_plugin = LoginPlugin()
