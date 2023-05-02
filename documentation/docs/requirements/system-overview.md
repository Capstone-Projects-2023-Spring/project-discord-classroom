---
sidebar_position: 1
---

# System Overview
### Project Abstract
The Classroom Bot is a Discord bot designed for educators or companies that want to create a learning environment using Discord servers. Many learning environments for schools and other video conferencing applications lack features that enable educators to create quizzes or assignments in the same place as the lectures. Our goal is to create a simple, streamlined experience that benefits both students and educators without the need for multiple web applications or a complicated setup.

Educators can use the bot to create quizzes, discussions, polls, and assignments related to their instructional topics. This feature allows educators to assess student performance and classroom attendance. The server owner is the default educator for the classroom. Students can take quizzes, submit assignments, participate in discussions, and provide feedback. They can share notes and questions with their peers, educators, or TAs in the same environment where they attend class. The TA, who must be assigned by the educator, can enter grades and assist with responding to student questions or other issues.

While the initial idea originated with a school environment in mind, the bot is useful for any learning environment. A company can also utilize the learning space to train and familiarize new employees with their systems or procedures. By making it simple and including various commands, the bot is ready to use, and adding it to a server creates a classroom instantly. By having class held in the same space as discussions, assignments, and quizzes, the learning environment feels open and easy to access. Students can communicate easily with educators or their peers, promoting their learning and enabling them to find answers to questions or problems quickly.

## Conceptual Design
The bot will be programmed with Python 3.7 and will connect to a Supabase database. The bot will use simple SQL commands to add/retrieve data from the database. The bot will be hosted through Google Computer Engine.

### Background
The recent pandemic has made online learning essential for students to continue their education in a safe environment for both educators and students. This product aims to make teaching from home easier and less stressful. While applications like Canvas and Blackboard allow educators to post assignments, quizzes, and grades, students seldom use these sites to connect with one another. Instead, they often create Discord channels to communicate with each other, where teachers and TAs are not involved in the discussion. Moving the learning environment to Discord itself will enable students to connect with one another and teachers and TAs to be part of the conversation.

A similar Discord bot to the proposed one is [“StudyLion”](https://top.gg/bot/889078613817831495). StudyLion promotes study communities where students gather in rooms to study together, with features such as timers, achievements, and personal profiles to engage users. However, StudyLion is mainly for students to connect with one another, while the proposed application allows teachers to control the Discord environment. Additionally, StudyLion does not support features such as hosting quizzes and submitting assignments, which this application aims to provide.

### Required Resources
For the entirety of this project, we have use Python3 to build the Discord bot and the API to connect to the database. The discord bot and API will be hosted on Google's Computer Engine, costing approximately $6 per month. Our database is hosted for free on Supabase.
