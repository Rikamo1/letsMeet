from mongodb import get_data_frame_from_db
from xml_to_Dataframe import get_dataframe_from_xml
from xlsx_to_df import get_data_frame_from_xlsx

import pandas as pd
import numpy as np

def get_full_dataframe():
    db_df = get_data_frame_from_db()
    xml_df = get_dataframe_from_xml()
    xlsx_df = get_data_frame_from_xlsx()

    # print("DB:")
    # print(db_df.head().T)
    # print("XML:")
    # print(xml_df.head().T)
    # print("XLSX:")
    # print(xlsx_df.head().T)

    # print columns
    # print("DB:")
    # print(db_df.columns)
    # print("XML:")
    # print(xml_df.columns)
    # print("XLSX:")
    # print(xlsx_df.columns)

    # Vorbereitung auf merge

    # Rename XML and XLS E-Mail column to _id
    xml_df.rename(columns={"email": "_id"}, inplace=True)
    xlsx_df.rename(columns={"E-Mail": "_id"}, inplace=True)

    # Delete name from Database and XLSX
    db_df.drop(columns=["name"], inplace=True)
    xlsx_df.drop(columns=["Nachname, Vorname"], inplace=True)

    # rename XLSX Hobby1 %Prio1%; Hobby2 %Prio2%; Hobby3 %Prio3%; Hobby4 %Prio4%; Hobby5 %Prio5%; column to Hobbies
    xlsx_df.rename(columns={"Hobby1 %Prio1%; Hobby2 %Prio2%; Hobby3 %Prio3%; Hobby4 %Prio4%; Hobby5 %Prio5%;": "Hobbies"}, inplace=True)

    # Split Hobbies and Prio
    for row in xlsx_df.itertuples():
        
        hobbies = str(row.Hobbies).split(";")
        for i, hobby in enumerate(hobbies, start=6):
            # Split hobby and prio
            hobby = hobby.split(" %")
            # If hobby is not at least 2 elements long, fill with NaN
            if len(hobby) < 2:
                hobby.append(None)
            # Add hobby to xlsx_df
            xlsx_df.at[row.Index, f"hobby_{i}"] = hobby[0]
            # Add prio to xlsx_df
            xlsx_df.at[row.Index, f"prio_{i}"] = hobby[1]
            
    # Drop Hobbies column
    xlsx_df.drop(columns=["Hobbies"], inplace=True)



    # Create prio collumns for hobbies 1 - 5
    for i in range(1, 6):
        xlsx_df[f"prio_{i}"] = np.nan
        


    # Merge XML and XLSX
    full_df = pd.merge(xml_df, xlsx_df, on="_id", how="outer")

    # Merge full_df with db_df
    full_df = pd.merge(full_df, db_df, on="_id", how="outer")

    # print("Full:")
    # print(full_df.head().T)
    return full_df

