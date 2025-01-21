### **Technische Dokumentation: Zusammenführung mehrerer Datenquellen**

#### **Zweck**

Dieses Modul kombiniert Daten aus drei verschiedenen Quellen (MongoDB, XML und Excel) in ein einheitliches  **Pandas DataFrame** , um eine ganzheitliche Datenanalyse zu ermöglichen.

---

#### **Funktion**

**`get_full_dataframe()`**

* **Aufgabe** :
* Lädt Daten aus den drei Quellen:
  1. **MongoDB** (Benutzerinformationen)
  2. **XML** (Benutzer und Hobbys)
  3. **Excel** (Benutzer, Hobbys und Prioritäten)
* Bereinigt und vereinheitlicht die Daten:
  * Spalten umbenennen.
  * Unnötige Spalten entfernen.
  * Hobbys und Prioritäten aus der Excel-Datei extrahieren.
* Führt die Datenquellen anhand der gemeinsamen ID (`_id`) zusammen.
* **Rückgabe** :
  Ein kombiniertes **Pandas DataFrame** , das Daten aus allen Quellen enthält.

---

#### **Ablauf**

1. **Daten laden** :

* **`get_data_frame_from_db()`** : Lädt MongoDB-Daten.
* **`get_dataframe_from_xml()`** : Lädt XML-Daten.
* **`get_data_frame_from_xlsx()`** : Lädt Excel-Daten.

1. **Datenaufbereitung** :

* Spalten aus XML und Excel vereinheitlichen, z. B. Umbenennung der Spalte `email` zu `_id`.
* Zerlegung der Hobby- und Prioritätsdaten aus der Excel-Spalte `Hobbies`.

1. **Datenzusammenführung** :

* Zusammenführung der Datenquellen mit **`pd.merge()`** auf Basis der gemeinsamen Spalte `_id`.
* Verwendung des `outer`-Joins, um Daten aus allen Quellen zu behalten.

---

#### **Beispiel**

* **Zusammengeführte Daten abrufen** :

```python
  full_df = get_full_dataframe()
  print(full_df.head())
```

---
