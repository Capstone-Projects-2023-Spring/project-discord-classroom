---
sidebar_position: 4
---

# Features and Requirements
##  Functional Requirements 

- The system shall require a Discord server.
  - Discord servers are free and require an account to make. 
- The system shall require permissions to change the server.
  - The admin (educator/owner) of the server must give permission to allow the bot to make changes to the server.
  - These changes include the creation of various text and voice channels that are used to manage the classroom and the assignment of various classroom roles to users.
- The system shall have commands for performing classroom related actions.
  - These commands will be slash commands that can be selected from Discord applications in the message UI or typed in the message UI.
  - Commands will be straightforward in what they do and have descriptions of what they require and how to function.
  - Educators will have the ability to use the assignment creation and classroom management commands.
  - Students will have the ability to use the assignment submission, help, and private question creation commands.
  - TAs will have the ability to use the grading commands.
  - All actions will be activated with bot commands.
- The system shall have a database.
  - Grades, users, assignments, quizzes, discussions, and classroom servers will be saved and referenced to allow the bot to make changes to the server and to keep track of the activities happening on the server.
- The system shall allow editing.
  - It will allow the assignments, discussions, and quizzes to be edited after creation.
  - Grades will be able to be updated by the users with the educator or TA roles.


##  Nonfunctional Requirements

- Commands should activate within 30 seconds.
- The commands should be straightforward.
- When using the tutor commands, the text limit is 150 characters.
- Bot commands will be dependent on the user's role.
- In the case that the document/assignment is too large, there will be a website for students to submit their assignments.
- The bot will allow educators to copy assignments, quizzes, and discussions to allow for ease of use in other servers.
  - Educators can get the JSON of their created assignments, quizzes, and discussions; they can then use them in another server to make it easier to manage multiple classrooms.
