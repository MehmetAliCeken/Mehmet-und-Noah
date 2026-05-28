#Mehmet Ali Ceken und Noah Mulaosmanovic
#21.05.2026 (Noah)
#28.05.2026 (Mehmet, erste zwei Stunden)

#Programmierprojekt
#Ein Programm, indem eine Note mit dem Schulfach gespeichert werden kann.


import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

##Datenbank
class NotenDatenbank:
	#Herstellunng der Verbindung zur lokalen Datenbank
    def __init__(self, Datenbank="Schulnoten.db"):
        self.Verbindung=sqlite3.connect(Datenbank)
        self.Datenbankzeiger=self.Verbindung.cursor()
        self.TabelleErstellen()

	#Erstellt die Notentabelle
    def TabelleErstellen(self):
        self.Datenbankzeiger.execute("""
            CREATE TABLE IF NOT EXISTS FächerNoten (
                Identifikationsnummer INTEGER PRIMARY KEY AUTOINCREMENT,
                Fach TEXT NOT NULL,
                Note INTEGER NOT NULL
            )
        """)
        self.Verbindung.commit()

	#Speichern der Noteninformationen
    def NoteSpeichern(self, Fach, Note):
        #Absicherung gegen die SQL-Injection mit "?"
        SQLBefehl="INSERT INTO FächerNoten (Fach, Note) VALUES (?, ?)"
        self.Datenbankzeiger.execute(SQLBefehl, (Fach, Note))
        self.Verbindung.commit()

	#Slle gespeicherten Einträge aus der Datenbank werden geholt
    def AlleNotenAuslesen(self):
        self.Datenbankzeiger.execute("SELECT Identifikationsnummer, Fach, Note FROM FächerNoten ORDER BY Fach ASC")
        return self.Datenbankzeiger.fetchall()

	#Löscht einen Eintrag anhand seiner Identifikationsnummer
    def NoteLöschen(self, EintragIdentifikationsnummer):
        SQLBefehl="DELETE FROM FächerNoten WHERE Identifikationsnummer = ?"
        self.Datenbankzeiger.execute(SQLBefehl, (EintragIdentifikationsnummer))
        self.Verbindung.commit()

	#Schließt Verbindung beim Beenden des Programms
    def DatenbankSchließen(self):
        self.Verbindung.close()



###Anwendungsfenster verbunden mit der Datenbank
class NotenAnwendung:
    def __init__(self, Fenster, Datenbank):
        self.Fenster=Fenster
        self.Datenbank=Datenbank
        
        #Hauptfenster
        self.Fenster.title("Schulnoten Verwaltungssystem")
        self.Fenster.geometry("600x450")
        
        #Erstellung der grafischen Komponenten
        self.KomponentenErstellen()
        #Laden der bereits vorhandenen Noten in die Liste
        self.NotenAnzeigeAktualisieren()

    def KomponentenErstellen(self):
        #Hauptrahmen für die Eingabe
        EingabeRahmen = ttk.LabelFrame(self.Fenster, text=" Neue Note erfassen ")
        EingabeRahmen.pack(padx=15, pady=15, fill="x")

        #Eingabefeld für Schulfach
        ttk.Label(EingabeRahmen, text="Schulfach:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.EingabeFach = ttk.Entry(EingabeRahmen, width=25)
        self.EingabeFach.grid(row=0, column=1, padx=10, pady=10)

        #Auswahlmenü für die Schulnote in Reihenfolge
        ttk.Label(EingabeRahmen, text="Note:").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.AuswahlNote = ttk.Combobox(EingabeRahmen, values=[1, 2, 3, 4, 5, 6], width=5, state="readonly")
        self.AuswahlNote.grid(row=0, column=3, padx=10, pady=10)






