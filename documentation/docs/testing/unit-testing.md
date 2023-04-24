---
sidebar_position: 1
---

# Unit tests

Unit tests will be written with pytest for Discord Classroom to test correct functionality of bot and the database.

# test_add_member_to_table()

Test: Tests whether a member was added to the database table related to their role.<br/>
Return: True if the student's attendance is 0, otherwise false

# test_increment_attendance()

Test: Tests whether a student's attendance field was incremented by one.<br/>
Return: True if the current attendance + 1 is equal to expected amount, otherwise false.

# test_ordinal()

Test: Tests whether a number is converted to its ordinal string.<br/>
Return: True if the string of the ordinal matches the expected string, otherwise false.

# test_get_ordinal_number()

Test: Tests Whether the get_ordinalnumber function returns the correct string.<br/>
Return: True if the string response matches the expected string, otherwise false..
