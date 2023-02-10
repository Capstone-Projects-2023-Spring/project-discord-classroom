---
sidebar_position: 5
---

# Use-case descriptions
Use Case 1<br />
As a user, I want to be able to create a poll to get feedback from my students.
1. The user types the command `!pollcreate` in the bot commands channel.
2. The user is prompted to enter question(s) and possible answers.
3. Every student is then notified from the bot that there is a new poll and are prompted to enter their answers. 
4. The user can type the command `!pollend` to end the poll
5. The user can type the command `!pollresults` to get the results of the poll<br/>

Use Case 2<br />
As a user I want to check my grades or attendance in the class. 
1. In the bot commands channel type the command `!grades/!attendance`
2. The bot sends a SQL request to the class database and pulls the user’s grade/attendance data
3. The bot sends current grade/attendance values in to the user as a private message<br/>

Use Case 3<br />
As a user, I want to create a new assignment, so everyone can access it.
1. In the private channel type the command `!assignmentcreate`
2. The bot responds with a prompt to enter the title, date, and instructions
3. The bot confirms with the user that all the detail are correct 
4. The bot notifies everyone that a new assignment has been created<br/>

Use Case 4<br />
As a user, I want to take a practice quiz, so that I can make sure that I am understanding the current concepts of class.
1. The user types `!pquiz` in the quiz section
2. The bot lists the currently available practice quizes
4. The user types `!pquiz 2` to take the second quiz from the list
5. The bot begins to send the questions to the user via DM
6. The user answers the questions
7. The bot checks the questions (if applicable) 
8. Returns the user results
9. User has the understanding of where they stand on the current topic<br/>

Use Case 5<br />
As a user, I want to track the attendance of students in my class.
1. The user types the `!attendance` command in the bot commands channel.
2. The bot send a message to all students and awaits their reply for a specified period of time.
3. The bot writes the attendance data to the SQL database: marking a student as present if it revived a response, or absent if it did not.
4. The bot notifies the user of any absences after the attendance taking period closes.<br/>

Use Case 6<br />
As a user, I want open a ticket/question that can be answered by the TA/Teacher.
1. The user types the `!ticketcreate` command in the bot commands channel.
2. The bot opens a private chat with the Student, TAs, and the Teacher.
3. The student can now ask a question privately in the newly opened chat
4. When the teacher/TA replies they can answer publicly and announce to the rest of the class, or privately in the chat created.<br/>
