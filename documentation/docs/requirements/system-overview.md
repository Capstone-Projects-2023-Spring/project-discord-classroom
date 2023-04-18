---
sidebar_position: 1
---

# System Overview
### Project Abstract<br/>	
The Classroom Bot is a Discord bot that is for educators or companies that want to create a learning environment in Discord for teaching. Some learning environments that are for school use and other video conferencing applications do not have features that can allow educators to create quizzes or assignments for the students in the same place that the lectures are occurring. Our goal is to create a streamlined experience that helps both students and educators without being overly complicated or requiring multiple web applications.

As an educator, they will have the ability to set quizzes, discussions, polls, and assignments pertaining to their teaching topics. This will allow the educator to see how the students are doing and manage their attendance and grades as needed. The owner of the server is the default educator for the classroom. As a student, they will have the ability to take quizzes, submit assignments, participate in discussions, and leave feedback. They can share notes and questions with fellow students or the educator and TA in the same environment that they attend class. The TA, which will have to be set by the educator, will have the ability to input grades and assist the educator with responding to student questions or other issues.

The bot will be for any learning environment and not limited to just schooling, but the initial ideas originated with a school environment in mind. A company may also take advantage of the learning space for internal information such as training and familiarizing new employees with their systems or procedures. By making it simple and including various commands, the idea is to have a ready-to-go classroom with just the addition of a bot to a server. By having the class be held in the same place as the discussions, assignments, and quizzes, the hope is that the learning environment feels open and easy to access. Students will have a quick and easy way of communicating with the educator or fellow students to help promote their learning and find answers to questions or problems they may have in short periods of time.

## Conceptual Design
The bot will be programmed with Python 3.7 and will connect to a Supabase database. The bot will use simple SQL commands to add/retrieve data from the database. The bot will be hosted through Google Computer Engine.

### Background<br/>
With the recent pandemic, online learning has become essential for students to continue their learning in 
a safe environment for both teachers and students. This product would be used to make teaching from 
home an easier, less stressful activity. The main way teachers are connecting with their students is 
through applications like canvas and blackboard. Although these sites do a great job with allowing 
educators to post assignments, quizzes, and grades, students rarely will use the site to connect with each 
other. Instead, students usually create discord channels to communicate with each other where the 
teachers and TAs are not involved in the discussion. Having the learning environment be on Discord itself 
will help both the students connect with each other and allow the teachers and TAs to be part of the 
conversation. 

There is a similar Discord Bot as the one proposed called [“StudyLion”](https://top.gg/bot/889078613817831495). 
This bot promotes the idea of study communities where students gather 
together in rooms and study with each other. There are cool features like timers, achievements, and 
personal profiles for users to feel more engaged. Since StudyLion is mainly just for students to connect 
with each other, my application will be different since it will allow teachers to be in control of the discord 
environment. Also, StudyLion does not support services such as hosting quizzes and submitting 
assignments. 

### Required Resources<br/>
For the entirety of this project, we use Python3 to build the Discord bot and creating our API to the database. The discord bot and API will be hosted on Google's Computer Engine costing about 6$ a month. Our database is hosted on Supabase for free. 
