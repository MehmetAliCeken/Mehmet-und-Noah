#Mehmet Ali Ceken und Noah Mulaosmanovic
#21.05.2026 (Noah)
#28.05.2026 (Mehmet, erste zwei Stunden (KSN))
#28.05.2026 (Noah, letzten zwei Studen (FSST))


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
        self.Verbindung = sqlite3.connect(Datenbank)
        self.Datenbankzeiger = self.Verbindung.cursor()
        self.TabelleErstellen()

	#Erstellt die Notentabelle
    def TabelleErstellen(self):
        self.Datenbankzeiger.execute("""
            CREATE TABLE IF NOT EXISTS FächerNoten
                (Identifikationsnummer INTEGER PRIMARY KEY AUTOINCREMENT,
                Fach TEXT NOT NULL, Note INTEGER NOT NULL)
        """)
        self.Verbindung.commit()

	#Speichern der Noteninformationen
    def Speichern(self, Fach, Note):
        #Absicherung gegen die SQL-Injection mit "?"
        SQLBefehl = "INSERT INTO FächerNoten (Fach, Note) VALUES (?, ?)"
        self.Datenbankzeiger.execute(SQLBefehl, (Fach, Note))
        self.Verbindung.commit()

	#Slle gespeicherten Einträge aus der Datenbank werden geholt
    def Auslesen(self):
        self.Datenbankzeiger.execute("SELECT Identifikationsnummer, Fach, Note FROM FächerNoten ORDER BY Fach ASC")
        return self.Datenbankzeiger.fetchall()

	#Löscht einen Eintrag anhand seiner Identifikationsnummer
    def Löschen(self, EintragIdentifikationsnummer):
        SQLBefehl = "DELETE FROM FächerNoten WHERE Identifikationsnummer = ?"
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
        #Rahmen für die Eingabe
        EingabeRahmen = ttk.LabelFrame(self.Fenster, text="Neue Note erfassen")
        EingabeRahmen.pack(padx=15, pady=15, fill="x")

        #Eingabefeld für Schulfach
        ttk.Label(EingabeRahmen, text="Schulfach:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.EingabeFach = ttk.Entry(EingabeRahmen, width=25)
        self.EingabeFach.grid(row=0, column=1, padx=10, pady=10)

        #Auswahlmenü für die Schulnote in Reihenfolge
        ttk.Label(EingabeRahmen, text="Note:").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.AuswahlNote = ttk.Combobox(EingabeRahmen, values=[1, 2, 3, 4, 5], width=5, state="readonly")
        self.AuswahlNote.grid(row=0, column=3, padx=10, pady=10)

        #Knopf zum Speichern
        KnopfSpeichern = ttk.Button(EingabeRahmen, text="Speichern", command=self.AktionSpeichern)
        KnopfSpeichern.grid(row=0, column=4, padx=15, pady=10)

        #Rahmen für die Listenansicht
        AnsichtRahmen = ttk.LabelFrame(self.Fenster, text=" Gespeicherte Noten ")
        AnsichtRahmen.pack(padx=15, pady=5, fill="both", expand=True)

        #Erstellung einer Spaltentabelle zur Darstellung der Daten
        Spalten = ("Identifikationsnummer", "Fach", "Note")
        self.TabelleAnsicht = ttk.Treeview(AnsichtRahmen, columns=Spalten, show="headings", selectmode="browse")
        
        #Spaltenüberschriften und deren Breite
        self.TabelleAnsicht.heading("Identifikationsnummer", text="ID")
        self.TabelleAnsicht.heading("Fach", text="Fach / Gegenstand")
        self.TabelleAnsicht.heading("Note", text="Schulnote")
        
        self.TabelleAnsicht.column("Identifikationsnummer", width=50, anchor="center")
        self.TabelleAnsicht.column("Fach", width=350, anchor="w")
        self.TabelleAnsicht.column("Note", width=100, anchor="center")
        
        self.TabelleAnsicht.pack(padx=10, pady=10, fill="both", expand=True)

		#Knopf zum Löschen einer Note
        KnopfLöschen = ttk.Button(AnsichtRahmen, text="Ausgewählte Note löschen", command=self.AktionLöschen)
        KnopfLöschen.pack(pady=10)


    def AktionSpeichern(self):
		#Liest Werte aus den Eingabefeldern aus
        FachText = self.EingabeFach.get().strip()
        GewählteNote = self.AuswahlNote.get()

        #Überprüfung, sodass Felder nicht leer sind
        if not FachText:
            return messagebox.showwarning("Eingabefehler", "Bitte geben Sie einen Namen für das Fach ein.")

		#Daten über das Datenbankobjekt sicher speichern
        self.Datenbank.Speichern(FachText, int(GewählteNote))
        
        #Oberfläche bereinigen
        self.EingabeFach.delete(0, tk.END)
        self.NotenAnzeigeAktualisieren()
        messagebox.showinfo("Erfolg", f"Note für {FachText} wurde erfolgreich gespeichert.")


    def AktionLöschen(self):
        #Anklicken eines Eintrags
        AusgewählterEintrag = self.TabelleAnsicht.selection()
        if not AusgewählterEintrag:
            return messagebox.showwarning("Auswahlfehler", "Bitte wählen Sie zuerst einen Eintrag aus der Liste aus.")

        #Holt Daten des ausgewählten Datenbankeintrags
        EintragDaten = self.TabelleAnsicht.item(AusgewählterEintrag, "values")
        EintragIdentifikationsnummer = EintragDaten[0]

        #Eintrag löschen und Seite aktualiseren
        self.Datenbank.Löschen(EintragIdentifikationsnummer)
        self.NotenAnzeigeAktualisieren()
        messagebox.showinfo("Gelöscht", "Der Eintrag wurde erfolgreich aus der Datenbank entfernt.")


    def NotenAnzeigeAktualisieren(self):
		#Leert die Tabelle
        for Eintrag in self.TabelleAnsicht.get_children():
            self.TabelleAnsicht.delete(Eintrag)

		#Laden von allen aktuellen Daten aus der Datenbank
        NotenListe = self.Datenbank.Auslesen()
        for Datensatz in NotenListe:
            self.TabelleAnsicht.insert("", tk.END, values=Datensatz)


###Hauptprogramm starten
if __name__ == "__main__":
    # (1) Datenbankobjekt starten
    MeineDatenbank = NotenDatenbank()

    # (2) Grafische Hauptoberfläche erstellen
    Hauptfenster = tk.Tk()
	
	# (3) Datenbank und Benutzeroberfläche
    Anwendung = NotenAnwendung(Hauptfenster, MeineDatenbank)

	#Beenden der Datenbankverbindung beim Schließen des Fensters
    Hauptfenster.protocol("WM_DELETE_WINDOW", lambda:[MeineDatenbank.DatenbankSchließen(), Hauptfenster.destroy()])

    #Endlossschleife der Benutzeroberfläche
    Hauptfenster.mainloop()
