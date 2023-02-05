---
sidebar_position: 1
---

# System Overview
### Project Abstract<br/>	
The Discord Classroom is a Discord bot that is for people or companies that want to create a learning environment in Discord for teaching. Some learning environments are for school use and other video conferencing applications do not have features that can allow for teachers to create quizzes or assignments for the students in the same palace that the lectures are occurring. The goal is to make a streamlined experience that helps both students and teachers without being overly complicated. 

As a teacher user, they will have the ability to set quizzes and assignments pertaining to their teaching topics and will allow the teacher to see how the students are doing and manage their attendance and grades if needed. As a student user, they will have the ability to set their role to students and to take quizzes, submit assignments, and to leave feedback and share notes and questions with fellow students or the teacher in the same environment that they attend class. The Ta user will have the ability to oversee the quiz information and assist the teacher or observe the results of students and help both the teacher or student if need be.

The bot will be for any learning environment and not limited to just schooling, but the initial ideas came from a school environment. A company may also take advantage of the learning space for internal information such as training and familiarizing new employees with their systems or procedures. By making it simple and including various commands the idea is to have a ready to go classroom with just the addition of a bot to a server. Having everything localized to one location, the hope is that the learning environment feels open and since it is paired with the ease of access of discord. Students will be able to have a quick and easy way of communicating with the teacher or fellow students to help promote their learning and find answers to questions or problems they may have in short periods of time.


# Conceptual Design
The bot will be programmed in Python 3.7+ and will connect to a SparkedHost database which uses simple SQL commands to add/retrieve data from the database. To host the application, SparkedHost will be used at a fee of 2$ per month.

### Background<br/>
With the recent pandemic, online learning has become essential for students to continue their learning in a safe environment for both teachers and students. This product would be used to make teaching from home an easier, less stressful activity. The main way teachers are connecting with their students is through applications like canvas and blackboard. Although these sites do a great job with allowing educators to post assignments, quizzes, and grades, students rarely will use the site to connect with each other. Instead, students usually create discord channels to communicate with each other where the teachers and TAs are not involved in the discussion. Having the learning environment be on Discord itself will help both the students connect with each other and allow the teachers and TAs to be part of the conversation.
There is a similar Discord Bot as the one proposed called “StudyLion” (https://top.gg/bot/889078613817831495). This bot promotes the idea of study communities where students gather together in rooms and study with each other. There are cool features like timers, achievements, and personal profiles for users to feel more engaged. Since StudyLion is mainly just for students to connect with each other, my application will be different since it will allow teachers to be in control of the discord environment. Also, StudyLion does not support services such as hosting quizzes and submitting assignments.

### Required Resources<br>
For the entirety of this project, we will use Python3 to build the Discord bot and make use of the discord API. The discord bot will be hosted on SparkedHost for 2$ a month which comes with its own database (MySQL), DDoS protection, and Git support.
