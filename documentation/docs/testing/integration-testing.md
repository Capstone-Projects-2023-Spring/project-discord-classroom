---
sidebar_position: 2
---
# Integration tests


** Use Case #1 &harr; test_attendance_recording: **

    Test: Tests whether the bot can successfully record attendance for a teacher in a Discord channel, 
    then send the attendance metrics to a database, along with posting a summary of the attendance to the teacher

    Returns: Returns True if all the steps were met whereby teacher recieves a summary of the attendance, otherwise False, if encountered any error

    Uses:
    Discord bot component, database component, and discord component
    

** Use Case #2 &harr; test_check_grades: **

    Test: Tests whether the bot can successfully pull the user's grade from the database and send it as a private message to the user upon request

    Returns: Returns True if a user is able to recieve their correct grade, otherwise False

    Uses:
    Discord bot component, API component, database component, and discord component
    

** Use Case #3 &harr; test_practice_quiz: **

    Test: Tests whether the bot can successfully list the available practice quizzes, send quiz questions to the user, check the answers, and return the user's results

    Returns: Returns True if user is able to retrieve, post, and recieve a grade for the practice quiz, otherwise False, if encountered any error

    Uses:
    Discord bot component, API component, database component, and discord component
    

** Use Case #4 &harr; test_ask_questions: **

    Test: Tests whether the bot can create a private chat between a student and a teacher, and allow the student to ask a question and the teacher to respond

    Returns: Returns True if the private chat is successfully created, the student is able to ask a question, and the teacher is able to respond, otherwise False

    Uses:
    Discord bot component, and discord component
    

** Use Case #5 &harr; test_create_poll: **

    Test: Tests whether the teacher is able to create a poll for their class

    Returns: Returns True if the poll creation is successfull, otherwise False

    Uses:
    Discord bot component, database component, and discord component

    
** Use Case #6 &harr; test_taking_attendance: **

    Test: Tests whether the teacher can successfully initiate attendance tracking whereby students input will be saved to the database afterward the discord bot will send teacher the summary of the absentees. 

    Returns: Returns True if the students attendence capture was successfull, otherwise False

    Uses:
    Discord bot component, API component, database component, and discord component

