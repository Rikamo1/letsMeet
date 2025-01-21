from pandas import read_excel
from pathlib import Path
import pandas as pd

def get_data_frame_from_xlsx():
    
    aktueller_pfad = Path(__file__).resolve().parent

    # Einlesen der Excel-Datei
    df = read_excel(aktueller_pfad.parent / "db_dump.xlsx")
    # Ausgabe des DataFrames
    print("XLSX-Datei gefunden.")
    return df
