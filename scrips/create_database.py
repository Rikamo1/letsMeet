import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from scrips import merge_dataframes

# Verbindung zur neuen PostgreSQL-Datenbank (z.B. "test_db") herstellen
DATABASE_URL = "postgresql://username:password@localhost:5432/test_db"  # Neue DB 'test_db'
engine = create_engine(DATABASE_URL)

# Beispiel-DataFrame (mit echten Daten ersetzen)
df = merge_dataframes.get_full_dataframe()

# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
    dbname="lf8_lets_meet_db", 
    user="user", 
    password="secret", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

#erstellen von Tabelle hobbies
cur.execute("""
    CREATE TABLE hobbies (
        _id SERIAL PRIMARY KEY,
        hobby VARCHAR(50),
        prio INT,
    )
""")
# erstellen von Tabelle Photos
cur.execute("""
    CREATE TABLE photos (
        user_id INT REFERENCES users(_id),
        _id SERIAL PRIMARY KEY,
        photo VARCHAR(100),
    )
""")

#erstellen von Tabelle users
cur.execute("""
    CREATE TABLE users (
        _id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        address VARCHAR(100),
        phone VARCHAR(20),
        Gender,
        Interested_in,
        Birth_date,
        Created_at TIMESTAMP,
        Updated_at TIMESTAMP
        Hobbies VARCHAR(100),""")


# Beispiel: Insert Daten in die "users"-Tabelle
for index, row in df.iterrows():
    cur.execute("""
        INSERT INTO users (first_name, last_name, address, phone, gender, interested_in, birth_date, created_at, updated_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['first_name'], 
        row['last_name'], 
        row['Straße Nr, PLZ Ort'], 
        row['phone'], 
   

# Verbindung schließen
cur.close()
conn.close()
