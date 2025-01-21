from mongodb import get_data_frame_from_db
from xml_to_Dataframe import get_dataframe_from_xml
from xlsx_to_df import get_data_frame_from_xlsx

import pandas as pd

db_df = get_data_frame_from_db()
xml_df = get_dataframe_from_xml()
xlsx_df = get_data_frame_from_xlsx()

print("DB:")
print(db_df.head())
print("XML:")
print(xml_df.head())
print("XLSX:")
print(xlsx_df.head())

# print columns
print("DB:")
print(db_df.columns)
print("XML:")
print(xml_df.columns)
print("XLSX:")
print(xlsx_df.columns)

print("Full:")
# print(full_df.head().T)

