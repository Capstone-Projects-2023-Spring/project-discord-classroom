---
sidebar_position: 1
---

# Unit tests

Unit tests will be written with pytest for Discord Classroom to test correct functionality of bot and API.

# testPing()

Test: If the bot returns the string "pong" in response to "ping" command<br/>
Return: Will return true if the bot returns the string "pong, otherwise returns false.

# testHelp()

Test: Whether a list of commands is sucessfully returned by the bot.<br/>
Return: True if a string containing the list of commands is returned, otherwise false.

# testDatabaseConnection()

Test: Tests whether the database is able to be connected to.<br/>
Return: True if database connection was successful, otherwise returns false

# testInsert()

Test: Whether the bot successfuly inserted a user into the database.<br/>
Return: True if the string "Inserted new student" is returned, else false.
