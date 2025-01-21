Logisches Datenmodell
Tabelle: users

    Beschreibung: Speichert die Informationen über Benutzer.
    Felder:
        _id (SERIAL, PK): Eindeutige Benutzer-ID.
        first_name (VARCHAR(50)): Vorname des Benutzers.
        last_name (VARCHAR(50)): Nachname des Benutzers.
        address (VARCHAR(100)): Adresse des Benutzers.
        phone (VARCHAR(20)): Telefonnummer.
        gender (VARCHAR(20)): Geschlecht des Benutzers (m/w/nonbinary).
        interested_in (VARCHAR(20)): Bevorzugtes Geschlecht bei Interessen.
        birth_date (DATE): Geburtsdatum.
        created_at (TIMESTAMP): Erstellungszeitpunkt des Profils.
        updated_at (TIMESTAMP): Zeitpunkt der letzten Aktualisierung.

Tabelle: hobbies

    Beschreibung: Speichert die Hobbys der Benutzer mit Prioritäten.
    Felder:
        _id (SERIAL, PK): Eindeutige Hobby-ID.
        user_id (INT, FK users._id): Benutzer, dem das Hobby gehört.
        hobby (VARCHAR(50)): Name des Hobbys.
        priority (INT): Priorität des Hobbys (-100 bis 100).

Tabelle: friends

    Beschreibung: Speichert die Freundschaftsbeziehungen zwischen Benutzern.
    Felder:
        _id (SERIAL, PK): Eindeutige Freundschafts-ID.
        user_id (INT, FK users._id): Benutzer, der die Freundschaft anfordert.
        friend_id (INT, FK users._id): Benutzer, der die Freundschaft akzeptiert.
        is_accepted (BOOLEAN): Status der Freundschaft (akzeptiert/nicht akzeptiert).

Tabelle: likes

    Beschreibung: Speichert die "Likes", die Benutzer anderen Benutzern geben.
    Felder:
        _id (SERIAL, PK): Eindeutige Like-ID.
        user_id (INT, FK users._id): Benutzer, der den Like gibt.
        liked_user_id (INT, FK users._id): Benutzer, der den Like erhält.
        created_at (TIMESTAMP): Zeitpunkt des Likes.

Tabelle: messages

    Beschreibung: Speichert die Nachrichten zwischen Benutzern.
    Felder:
        _id (SERIAL, PK): Eindeutige Nachrichten-ID.
        sender_id (INT, FK users._id): Absender der Nachricht.
        receiver_id (INT, FK users._id): Empfänger der Nachricht.
        content (TEXT): Inhalt der Nachricht.
        sent_at (TIMESTAMP): Sendezeitpunkt.

Tabelle: photos

    Beschreibung: Speichert die Profilbilder und zusätzlichen Fotos der Benutzer.
    Felder:
        _id (SERIAL, PK): Eindeutige Foto-ID.
        user_id (INT, FK users._id): Benutzer, zu dem das Foto gehört.
        photo_data (BYTEA): Binärdaten des Fotos (Profilbild).
        photo_url (VARCHAR(255)): URL für zusätzliche Fotos.

Beziehungen

    users → hobbies:
        1:n-Beziehung (Ein Benutzer kann mehrere Hobbys haben).
        Fremdschlüssel: hobbies.user_id verweist auf users._id.

    users → friends:
        Selbstreferenzierende 1:n-Beziehung (Ein Benutzer kann viele Freunde haben).
        Fremdschlüssel: friends.user_id und friends.friend_id verweisen auf users._id.

    users → likes:
        1:n-Beziehung (Ein Benutzer kann viele Likes geben und erhalten).
        Fremdschlüssel: likes.user_id und likes.liked_user_id verweisen auf users._id.

    users → messages:
        1:n-Beziehung (Ein Benutzer kann viele Nachrichten senden und empfangen).
        Fremdschlüssel: messages.sender_id und messages.receiver_id verweisen auf users._id.

    users → photos:
        1:n-Beziehung (Ein Benutzer kann mehrere Fotos hochladen).
        Fremdschlüssel: photos.user_id verweist auf users._id.

