import os
import pandas as pd
import xml.etree.ElementTree as ET

# Datei-Pfad
current_dir = os.getcwd()
file_path = os.path.join(current_dir, 'Lets_Meet_Hobbies.xml')
global df
def get_dataframe_from_xml():
    if os.path.exists(file_path):
        print("XML-Datei gefunden. Einlesen...")
        try:
            # XML-Daten einlesen und Struktur prüfen
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Liste für Benutzer-Daten erstellen
            users = []

            for user in root.findall('user'):
                # Extrahiere E-Mail und Name
                email = user.find('email').text if user.find('email') is not None else None
                name = user.find('name').text if user.find('name') is not None else None

                # Extrahiere Hobbys, auch wenn die Liste leer ist
                hobbies_element = user.find('hobbies')
                if hobbies_element is not None:
                    hobbies = [hobby.text for hobby in hobbies_element.findall('hobby') if hobby.text]
                else:
                    hobbies = []  # Keine Hobbys

                # Benutzer-Daten zusammenstellen
                user_data = {'email': email, 'name': name}
                for i, hobby in enumerate(hobbies, start=1):
                    user_data[f'hobby_{i}'] = hobby

                users.append(user_data)

            # Konvertiere die Liste der Benutzer in ein DataFrame
            df = pd.DataFrame(users)

            # Vorname und Nachname aufteilen
            def split_name(full_name):
                if pd.isna(full_name):
                    return None, None
                try:
                    last_name, first_name = map(str.strip, full_name.split(',', 1))
                    return first_name, last_name
                except ValueError:
                    return full_name, None  # Falls das Format nicht stimmt

            df[['first_name', 'last_name']] = df['name'].apply(lambda x: pd.Series(split_name(x)))

            # Entferne die ursprüngliche "name"-Spalte
            df.drop(columns=['name'], inplace=True)
            
            # Gebe das dataframe zurück
            return df

        except ET.ParseError as e:
            print(f"Fehler beim Parsen der XML-Datei: {e}")
        except Exception as e:
            print(f"Allgemeiner Fehler: {e}")
    else:
        print(f"XML-Datei nicht gefunden: {file_path}")

def save_df_as_csv():
            # Speichere als CSV-Datei
            output_path = os.path.join(current_dir, 'Lets_Meet_Hobbies_XML_output.csv')
            df.to_csv(output_path, index=False)

            print(f"CSV-Datei wurde erfolgreich erstellt: {output_path}")
            print(df.head())
