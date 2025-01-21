from pandas import read_excel
from pathlib import Path
import pandas as pd
import os

def get_data_frame_from_xlsx():
    # Datei-Pfad
    current_dir = os.path.dirname(__file__)
    parant_dir_of_parant_dir = Path(current_dir).parent.parent
    file_path = Path(parant_dir_of_parant_dir, "db_dump.xlsx")

    if os.path.exists(file_path):
        print("XLSX-Datei gefunden. Pfad:", file_path)
        try:
            # Einlesen der Excel-Datei
            df = read_excel(file_path)
            # Ausgabe des DataFrames
            
            return df
        
        except:
            print("Fehler beim verarbeiten der XLSX-Datei.")
            return None
        
    else:
        print("XLSX-Datei nicht gefunden. Pfad:", file_path, "/db_dump.xlsx")
        return None
