import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import merge_dataframes
import json

# Verbindung zur PostgreSQL-Datenbank herstellen
DATABASE_URL = "postgresql://user:secret@localhost:5432/lf8_lets_meet_db"
engine = create_engine(DATABASE_URL)

# Beispiel-DataFrame (mit echten Daten ersetzen)
df = merge_dataframes.get_full_dataframe()

df['Geburtsdatum'] = pd.to_datetime(df['Geburtsdatum'], format='%d.%m.%Y').dt.strftime('%Y-%m-%d')


# Verbindung zur PostgreSQL-Datenbank herstellen
conn = psycopg2.connect(
    dbname="lf8_lets_meet_db",
    user="user",
    password="secret",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
# Alle tabellen löschen (wir brauchen mehrere versuche, da die tabellen fehlerhaft waren)
cur.execute("DROP TABLE IF EXISTS users, hobbies, photos, friends, likes, messages CASCADE")
# Tabellen erstellen
cur.execute("""
    CREATE TABLE users (
        _id SERIAL PRIMARY KEY,
        email VARCHAR(50) UNIQUE,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        address VARCHAR(100),
        phone VARCHAR(20),
        gender VARCHAR(20),
        interested_in VARCHAR(20),
        birth_date DATE,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
""")

cur.execute("""
    CREATE TABLE hobbies (
        _id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(_id),
        hobby VARCHAR(255),
        priority VARCHAR(16)
    )
""")

cur.execute("""
    CREATE TABLE photos (
        _id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(_id),
        photo_url VARCHAR(255)
    )
""")

cur.execute("""
    CREATE TABLE friends (
        user_id INT REFERENCES users(_id),
        friend_id INT REFERENCES users(_id),
        PRIMARY KEY (user_id, friend_id)
    )
""")

cur.execute("""
    CREATE TABLE likes (
        _id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(_id),
        liked_email VARCHAR(50),
        status VARCHAR(20),
        timestamp TIMESTAMP
    )
""")

cur.execute("""
    CREATE TABLE messages (
        _id SERIAL PRIMARY KEY,
        sender_id INT REFERENCES users(_id),
        receiver_id INT REFERENCES users(_id),
        message_text TEXT,
        sent_at TIMESTAMP
    )
""")

# Daten einfügen: Users
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO users (email, first_name, last_name, address, phone, gender, interested_in, birth_date, created_at, updated_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING _id
    """, (
        row['_id'],
        row['first_name_y'], 
        row['last_name_y'], 
        row['Straße Nr, PLZ Ort'], 
        row['phone'], 
        row['Geschlecht (m/w/nonbinary)'], 
        row['Interessiert an'], 
        row['Geburtsdatum'], 
        row['createdAt'], 
        row['updatedAt']
    ))
    user_id = cur.fetchone()[0]

    # Daten einfügen: Hobbies
    for i in range(1, 12):
        hobby_col = f'hobby_{i}'
        prio_col = f'prio_{i}'
        if pd.notnull(row.get(hobby_col)):
            cur.execute("""
                INSERT INTO hobbies (user_id, hobby, priority) 
                VALUES (%s, %s, %s)
            """, (user_id, row[hobby_col], row.get(prio_col, 0)))

    # Daten einfügen: Photos
    if pd.notnull(row.get('photo')):
        cur.execute("""
            INSERT INTO photos (user_id, photo_url) 
            VALUES (%s, %s)
        """, (user_id, row['photo']))

    # Daten einfügen: Freunde
    if row.get('friends') and pd.notnull(row.get('friends')):
        friends = row['friends'].split(',')  # Angenommen, Freunde sind durch Komma getrennt
        for friend_id in friends:
            cur.execute("""
                INSERT INTO friends (user_id, friend_id) 
                VALUES (%s, %s) ON CONFLICT DO NOTHING
            """, (user_id, int(friend_id)))

    # Daten einfügen: Likes
    likes_data = row.get('likes')

    # Überprüfen, ob likes_data eine nicht-leere Liste oder ein String ist
    if likes_data and (isinstance(likes_data, str) or (isinstance(likes_data, list) and len(likes_data) > 0)):
        try:
            # Versuche, den Wert als JSON zu parsen, falls es ein String ist
            likes = json.loads(likes_data) if isinstance(likes_data, str) else likes_data
            if isinstance(likes, list):  # Falls `likes` eine Liste von Objekten ist
                for like in likes:
                    # if like is not null
                    if like:
                        cur.execute("""
                            INSERT INTO likes (user_id, liked_email, status, timestamp) 
                            VALUES (%s, %s, %s, %s)
                        """, (user_id, like['liked_email'], like['status'], like['timestamp']))
                    else:
                        print(f"Ungültiges Like-Format: {likes}")
                
            else:
                print(f"Ungültiges Like-Format: {likes}")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Fehler beim Verarbeiten von Likes: {e}")
    else:
        print(f"Likes-Feld fehlt oder ist leer: {likes_data}")

    # Daten einfügen: Nachrichten
    if row.get('messages'):
        try:
            if isinstance(row['messages'], str) and row['messages'].strip():
                messages = row['messages'].split(';')  # Angenommen, Nachrichten sind durch Semikolon getrennt
                for message in messages:
                    if '|' in message:  # Sicherstellen, dass das Format korrekt ist
                        receiver_id, text, sent_at = message.split('|', 2)  # Maximal 2 Splits
                        cur.execute("""
                            INSERT INTO messages (sender_id, receiver_id, message_text, sent_at) 
                            VALUES (%s, %s, %s, %s)
                        """, (user_id, int(receiver_id), text.strip(), sent_at.strip()))
                    else:
                        print(f"Ungültiges Nachrichten-Format: {message}")
            elif isinstance(row['messages'], list) and len(row['messages']) > 0:
                for message in row['messages']:
                    if isinstance(message, dict) and 'receiver_id' in message and 'message_text' in message and 'sent_at' in message:
                        cur.execute("""
                            INSERT INTO messages (sender_id, receiver_id, message_text, sent_at) 
                            VALUES (%s, %s, %s, %s)
                        """, (user_id, int(message['receiver_id']), message['message_text'].strip(), message['sent_at'].strip()))
            else:
                print(f"Ungültiges oder leeres Nachrichtenfeld: {row['messages']}")
        except ValueError as e:
            print(f"Fehler beim Verarbeiten von Nachrichten: {e}")
    else:
        print(f"Nachrichtenfeld fehlt oder ist null: {row.get('messages')}")

# Änderungen speichern und Verbindung schließen
conn.commit()
cur.close()
conn.close()
