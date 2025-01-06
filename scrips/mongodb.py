import pandas as pd
import sqlite3
import os
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import pymongo

# MongoDB-Verbindungsdetails
mongo_host = 'localhost'  # Hostname der MongoDB
mongo_port = 27017        # Standardport von MongoDB
db_name = 'LetsMeet'      # Name der MongoDB-Datenbank
collection_name = 'users' # Name der Sammlung

# Verbindung zur MongoDB aufbauen
client = pymongo.MongoClient(f'mongodb://{mongo_host}:{mongo_port}/')
db = client[db_name]
collection = db[collection_name]

# Alle Daten aus der Sammlung abrufen
data = list(collection.find())

# Überprüfen, ob Daten vorhanden sind
if data:
    # Umwandlung der Daten in ein Pandas DataFrame
    df = pd.DataFrame(data)

    # Ausgabe des DataFrames
    print(df)
else:
    print("Keine Daten gefunden.")