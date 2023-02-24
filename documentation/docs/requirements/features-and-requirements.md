---
sidebar_position: 4
---

# Features and Requirements
##  Functional Requirements 

- The Discord Classroom bot will transform the server into a learning environment. <br />
  - Classroom bot will create and manage text and voice channels such as private channels, quiz channels, assignment channels, and homework channels. <br />
  - Classroom bot can be utilized to assign and manage roles of members. <br />
  - Users can perform certain action associated with their roles, such as submitting assignments and viewing grades. <br />

- Both educators and students can use simple commands to perform various tasks. <br />
  - Students will be able to mark their attendance by issuing the command `!present`. The Discord Classroom bot will then record the attendance in its database. <br />
  - Educators will be able to create quizzes by issuing the command `!cquiz`. This will allow them to easily create quizzes without having to navigate through multiple menus or interfaces. <br />
  - Issuing the command `!help` will display a comprehensive manual page containing all the commands associated with the Discord Classroom bot. <br />

##  Nonfunctional Requirements

- The Discord Classroom bot will function within the context of a Discord environment  <br />
  - The bot will be added to a server using a unique invitation link. <br />
  - Login security for the bot will leverage built-in Discord authentication. <br />
  - The bot will execute commands issued by authorized users in the server. <br />

- The Discord Classroom bot will connect to a MySQL database for data storage and retrieval. <br />
  - The bot will securely interact to the database using REST API with secure methods.<br />
  - The database will store and update information such as student attendance records, quiz results, and assignment submissions in real-time. <br />
  - The bot will retrieve and display information upon request from authorized users. <br />
