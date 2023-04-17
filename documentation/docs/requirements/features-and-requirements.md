---
sidebar_position: 4
---

# Features and Requirements
##  Functional Requirements 

- The system shall require a Discord server.
  - Discord servers are free and require an account to make. 
- The system shall require permissions to change the server.
  - These changes are various text and voice channels that are used to manage the classroom aspect of the server, and the bot allows for the assignment of roles to users.
  - The admin (educator/owner) of the server will have to give permission to allow the bot to make changes to the server.
- The system shall have commands for performing actions.
  - These commands will be slash commands that can be selected from Discord applications in the message UI or typed in the message UI.
  - Commands will be straightforward in what they do and have descriptions of what they require and how to function.
  - Educators will have the ability to use the creation commands and other management commands.
  - Students will have the ability to use submit commands, help commands, and the creation of a private question.
  - TAs will have the ability to adjust grades.
  - All actions will be activated with bot commands.
  - Bot commands will be dependent on the user's role.
- The system shall have a database.
  - Grades, users, assignments, quizzes, discussions, and classrooms will be saved and referenced to allow the bot to make changes to the server and to keep track of the activities happening on the server.
- The system shall have a way for submitting assignments.
  - In the case that the document/assignment is too large, there will be a website for students to submit their assignments.
- The system shall allow educators to copy assignments, quizzes, and discussions to allow for ease of use in other servers.
  - Educators can get the JSON of their created assignments, quizzes, and discussions; they can then use them in another server to make it easier to manage multiple classrooms.
- The system shall allow editing.
  - It will allow the assignments, discussions, and quizzes to be edited after creation.
  - Grades will be able to be updated by the Educator or the TA roles.


##  Nonfunctional Requirements

- Commands should activate within 30 seconds.
- The commands will not be confusing.
- When using the tutor commands, the text limit is 150 characters.

