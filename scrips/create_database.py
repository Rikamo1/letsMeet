import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from scrips import merge_dataframes

# Verbindung zur PostgreSQL-Datenbank herstellen
DATABASE_URL = "postgresql://user:secret@localhost:5432/lf8_lets_meet_db"
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

# Tabellen erstellen
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        _id SERIAL PRIMARY KEY,
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
    CREATE TABLE IF NOT EXISTS hobbies (
        _id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(_id),
        hobby VARCHAR(50),
        priority INT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS photos (
        _id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(_id),
        photo_url VARCHAR(255)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS friends (
        user_id INT REFERENCES users(_id),
        friend_id INT REFERENCES users(_id),
        PRIMARY KEY (user_id, friend_id)
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS likes (
        _id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(_id),
        liked_hobby VARCHAR(50),
        score INT
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
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
        INSERT INTO users (first_name, last_name, address, phone, gender, interested_in, birth_date, created_at, updated_at) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING _id
    """, (
        row['first_name'], 
        row['last_name'], 
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
    if pd.notnull(row.get('friends')):
        friends = row['friends'].split(',')  # Angenommen, Freunde sind durch Komma getrennt
        for friend_id in friends:
            cur.execute("""
                INSERT INTO friends (user_id, friend_id) 
                VALUES (%s, %s) ON CONFLICT DO NOTHING
            """, (user_id, int(friend_id)))

    # Daten einfügen: Likes
    if pd.notnull(row.get('likes')):
        likes = row['likes'].split(',')  # Angenommen, Likes sind durch Komma getrennt
        for like in likes:
            hobby, score = like.split(':')  # Angenommen, Format ist "hobby:score"
            cur.execute("""
                INSERT INTO likes (user_id, liked_hobby, score) 
                VALUES (%s, %s, %s)
            """, (user_id, hobby, int(score)))

    # Daten einfügen: Nachrichten
    if pd.notnull(row.get('messages')):
        messages = row['messages'].split(';')  # Angenommen, Nachrichten sind durch Semikolon getrennt
        for message in messages:
            receiver_id, text, sent_at = message.split('|')  # Angenommen, Format ist "receiver_id|text|sent_at"
            cur.execute("""
                INSERT INTO messages (sender_id, receiver_id, message_text, sent_at) 
                VALUES (%s, %s, %s, %s)
            """, (user_id, int(receiver_id), text, sent_at))

# Änderungen speichern und Verbindung schließen
conn.commit()
cur.close()
conn.close()