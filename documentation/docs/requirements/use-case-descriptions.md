---
sidebar_position: 5
---

# Use-case descriptions
Use Case 1<br />
As an educator, I want to be able to create a poll so I can get feedback from my students. This will help me understand the students better, allow me address the issues accordingly. 
1. The user types the command `/poll` in a text channel.
2. The user can add arguments `[topic]` and then add the options `[option1]``[option2]`...`[option8]`
3. Students can now see that there is a new poll and are prompted to select their answers. 
4. The poll updates as people select the options<br/>

Use Case 2<br />
As a student, I want to check my grades or attendance in the class. 
1. In the bot commands channel type the command `/grades or /attendance`
2. The bot sends a SQL request to the class database and pulls the user’s grade/attendance data
3. The bot sends current grade/attendance values into the user as a private message<br/>

Use Case 3<br />
As an educator, I want to create a new assignment, so everyone can access it.
1. In the private channel type the command `/create assignment`
2. The bot responds with a prompt to enter the title, points, details, start date, and due date
3. A new channel is created for the assignment.
4. The bot notifies everyone that a new assignment has been created<br/>

Use Case 4<br />
As a student, I want to practice for my upcoming test, so that I can make sure that I am understanding the current concepts of class.
1. The user types `/tutor quiz [number of questions] [topic] [grade level]` in the general channel
2. The bot processes the request with AI language model 
3. Next, the bot sends the generated questions to the user via DM
4. The user is presented with a list of questions. They can type their answer the questions.
5. Once the user types their answers the bot will respond with the correct answers

Use Case 5<br />
As an educator, I want to take the attendance of students in my class.
1. The educator types the `/attendance` command in the bot commands channel.
2. The bot sends a poll to the attendance channel for students to respond to.
3. The bot writes the attendance data to the SQL database: marking a student as present if they reacted to the poll, or absent if it did not.

Use Case 6<br />
As a student, I want open a private ticket/question that can be answered by the TA/Teacher.
1. The user types the `/private [question]` command in the questions channel.
2. The bot opens a private chat with the Student, TAs, and the Teacher and provides them with the questions.
3. The student can now ask any additional questions privately in the newly opened chat
4. When the teacher/TA replies they can answer publicly and announce it to the rest of the class, or privately in the chat created.<br/>
