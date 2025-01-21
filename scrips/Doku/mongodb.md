### **Technische Dokumentation: MongoDB-Datenverarbeitung**

#### **Zweck**

Das Modul verbindet sich mit einer MongoDB, ruft alle Daten aus einer angegebenen Sammlung ab und konvertiert diese in ein  **Pandas DataFrame** .

---

#### **Funktion**

**`get_data_frame_from_db()`**

* **Aufgabe** :
* Stellt eine Verbindung zu einer MongoDB-Datenbank her.
* Ruft Daten aus der angegebenen Sammlung (`users`) ab.
* Konvertiert die Daten in ein Pandas DataFrame.
* **Parameter** :
* `mongo_host`: Hostname der MongoDB (Standard: `localhost`).
* `mongo_port`: Port der MongoDB (Standard: `27017`).
* `db_name`: Name der Datenbank (Standard: `LetsMeet`).
* `collection_name`: Name der Sammlung (Standard: `users`).

---

#### **Beispiel**

* **Daten aus MongoDB abrufen** :

```python
  df = get_data_frame_from_db()
  print(df)
```
