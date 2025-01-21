#### Technische Dokumentation: XML-Datenverarbeitung

#### **Zweck**

Das Modul liest eine XML-Datei (`Lets_Meet_Hobbies.xml`) ein, extrahiert Benutzer- und Hobbydaten, konvertiert sie in ein **Pandas DataFrame** und speichert die Ergebnisse optional als CSV.

---

#### **Funktionen**

1. **`get_dataframe_from_xml()`**
   * Liest die XML-Datei ein und prüft deren Existenz.
   * Extrahiert Daten (E-Mail, Name, Hobbys).
   * Teilt Namen in `first_name` und `last_name`.
   * Gibt ein DataFrame zurück.
2. **`save_df_as_csv()`**
   * Speichert das DataFrame als `Lets_Meet_Hobbies_XML_output.csv`.

---

#### **Beispiele**

* **Daten laden** :

```python
  df = get_dataframe_from_xml()
```
