SELECT
    datetime (message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
    message.text,
    message.is_from_me,
    chat.chat_identifier
FROM
    chat
    JOIN chat_message_join ON chat. "ROWID" = chat_message_join.chat_id
    JOIN message ON chat_message_join.message_id = message. "ROWID"
WHERE
	chat.chat_identifier == -- Partner's phone number goes here in quotes
ORDER BY
    message_date ASC;