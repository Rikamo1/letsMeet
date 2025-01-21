1. Eigene Stammdaten bearbeiten

    Beschreibung: Ein Benutzer kann seine eigenen Stammdaten bearbeiten, einschließlich der Bearbeitung von Hobbys und Fotos.

    SQL-Querys:
        Um die Stammdaten eines Benutzers zu bearbeiten, könnte der Benutzer in der users-Tabelle aktualisiert werden:

UPDATE users
SET first_name = %s, last_name = %s, address = %s, phone = %s, gender = %s, interested_in = %s, birth_date = %s, updated_at = NOW()
WHERE _id = %s;

    Um ein Foto hinzuzufügen oder zu ändern, könnte das Profilbild des Benutzers in der users-Tabelle aktualisiert werden:

    UPDATE users
    SET profile_picture = %s, updated_at = NOW()
    WHERE _id = %s;

2. Hobbys bearbeiten, ergänzen, priorisieren

    Beschreibung: Ein Benutzer kann seine Hobbys bearbeiten, hinzufügen und die Priorität seiner Hobbys ändern.

    SQL-Querys:
        Um die Hobbys eines Benutzers zu aktualisieren oder hinzuzufügen:

    INSERT INTO hobbies (user_id, hobby, priority)
    VALUES (%s, %s, %s)
    ON CONFLICT (user_id, hobby) DO UPDATE
    SET priority = EXCLUDED.priority;

        Dies stellt sicher, dass ein Hobby entweder hinzugefügt oder die Priorität eines bestehenden Hobbys aktualisiert wird.

3. Name und Hobbys eines ausgewählten Nutzers ausgeben lassen

    Beschreibung: Ein Benutzer kann den Namen und die Hobbys eines anderen Benutzers einsehen.

    SQL-Query:
        Um den Namen und die Hobbys eines Benutzers anzuzeigen:

    SELECT u.first_name, u.last_name, h.hobby, h.priority
    FROM users u
    LEFT JOIN hobbies h ON u._id = h.user_id
    WHERE u._id = %s;

4. Andere Teilnehmer kontaktieren

    Beschreibung: Ein Benutzer kann andere Teilnehmer (Benutzer) kontaktieren.

    SQL-Query:
        Dies könnte durch die Verwendung der Nachrichten-Tabelle erfolgen:

    INSERT INTO messages (user_id, message_text, created_at)
    VALUES (%s, %s, NOW());

5. Nutzer mit ähnlichen Interessen finden

    Beschreibung: Ein Benutzer kann nach anderen Benutzern mit ähnlichen Interessen suchen.

    SQL-Query:
        Eine einfache Suche nach Nutzern mit ähnlichen Interessen (z.B. Hobbys):

    SELECT u.first_name, u.last_name
    FROM users u
    JOIN hobbies h ON u._id = h.user_id
    WHERE h.hobby IN (SELECT hobby FROM hobbies WHERE user_id = %s)
    AND u._id != %s;

6. Freundesliste beiderseitig zustimmen

    Beschreibung: Ein Benutzer kann einen anderen Benutzer zu seiner Freundesliste hinzufügen, aber es muss eine beidseitige Zustimmung geben.

    SQL-Query:
        Um eine Freundschaft zu erstellen:

INSERT INTO friends (user_id, friend_id)
VALUES (%s, %s)
ON CONFLICT (user_id, friend_id) DO NOTHING;

    Die Bedingung, dass beide Nutzer zustimmen müssen, könnte durch die doppelte Einfügung überprüft werden, aber das könnte auch auf Anwendungsebene durch die Benutzeroberfläche geregelt werden.