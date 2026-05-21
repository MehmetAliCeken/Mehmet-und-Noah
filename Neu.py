#Mehmet und Noah
# 21.05.2026
#Wir wollen eine NotenDatenBank erstellen wo die Schüler angezeigt werden und ihre Noten

import sqlite3       # Für die "mariadb/sqlite" Datenbank-Anforderung
import tkinter as tk        #Importiert das tkinter-Modul für die grafische Oberfläche unter dem Kürzel tk
from tkinter import messagebox      # Für Fehlermeldungen und Erfolgs-Pop-ups
from tkinter import ttk     # für schönere UI-Elemente (wie das Dropdown-Menü)

class NotenDatenbank:       #Klasse 'NotenDatenBank erstellt'
    def _init_(self, dateiname="schulnoten.db"):        # Konstruktor: Erstellt die datenbankverbindung beim rogrammstart
        self.verbindung = sqlite3.connect(dateiname)         #'self.verbindung' ist ein sauberer, sprechender Variablenname
        self.cursor = self.verbindung.cursor()
        self.tabelle_erstellen():
    
    # Methode zur Erstellung der Tabelle, falls sie noch nicht existiert
    def tabelle_erstellen(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS facher_noten (
                id integer primary key autoincrement,
                fach TEXT NOT NULL,
                note integer NOT NULL
            )
        """)
        self.verbindung.commit()