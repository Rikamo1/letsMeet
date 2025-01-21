### **Technische Dokumentation: Excel-Datenverarbeitung**

#### **Zweck**

Das Modul liest eine Excel-Datei (`db_dump.xlsx`) ein und gibt deren Inhalt als **Pandas DataFrame** zurück.

---

#### **Funktion**

**`get_data_frame_from_xlsx()`**

* **Aufgabe** :
* Liest die Datei `db_dump.xlsx` aus dem übergeordneten Verzeichnis des Skripts ein.
* Gibt den Inhalt als DataFrame zurück.
* **Ablauf** :

1. Bestimmt den aktuellen Dateipfad des Skripts.
2. Lädt die Excel-Datei mit **Pandas** (`read_excel`).
3. Gibt das DataFrame zurück.

---

#### **Beispiel**

* **Excel-Daten laden** :

```python
  df = get_data_frame_from_xlsx()
  print(df)
```
