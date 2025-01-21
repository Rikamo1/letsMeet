import pandas as pd
import os
import xml.etree.ElementTree as ET

# Aktuelles Verzeichnis und XML-Dateipfad
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, 'Lets_Meet_Hobbies.xml')

if os.path.exists(file_path):
    print("XML-Datei gefunden. Einlesen...")
    try:
        # XML in DataFrame laden (benutze //user für alle Benutzer)
        df = pd.read_xml(file_path, xpath=".//user")

        # Funktion, um die Hobbys aus dem XML zu extrahieren
        def extract_hobbies(hobbies_xml):
            if pd.isna(hobbies_xml):  # Falls keine Hobbys vorhanden sind
                return []
            hobbies = ET.fromstring(hobbies_xml).findall('hobby')
            return [hobby.text for hobby in hobbies]

        # Extrahiere Hobbys und füge dynamisch Spalten hinzu
        df['hobbies'] = df['hobbies'].apply(extract_hobbies)
        max_hobbies = df['hobbies'].apply(len).max()  # Maximale Anzahl Hobbys ermitteln

        for i in range(max_hobbies):
            df[f'hobby_{i + 1}'] = df['hobbies'].apply(lambda x: x[i] if i < len(x) else None)

        # Entferne die ursprüngliche 'hobbies'-Spalte
        df.drop(columns=['hobbies'], inplace=True)

        # Speichern als CSV
        output_path = os.path.join(parent_dir, 'Lets_Meet_Hobbies_output.csv')
        df.to_csv(output_path, index=False)

        print(f"CSV-Datei wurde erfolgreich erstellt: {output_path}")
        print(df.head())  # Zeige die ersten Zeilen des DataFrames

    except Exception as e:
        print("Fehler beim Verarbeiten der XML-Datei:", e)

else:
    print(f"XML-Datei nicht gefunden: {file_path}")
