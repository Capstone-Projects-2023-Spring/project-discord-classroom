[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-f4981d0f882b2a3f0472912d15f9806d57e124e0fc890972558857b51b24a6f9.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=9911448)
<div align="center">

# Discord Classroom Bot
[![Report Issue on Jira](https://img.shields.io/badge/Report%20Issues-Jira-0052CC?style=flat&logo=jira-software)](https://temple-cis-projects-in-cs.atlassian.net/jira/software/c/projects/DC/issues)
[![Deploy Docs](https://github.com/ApplebaumIan/tu-cis-4398-docs-template/actions/workflows/deploy.yml/badge.svg)](https://github.com/Capstone-Projects-2023-Spring/project-discord-classroom/actions/workflows/deploy.yml)
[![Documentation Website Link](https://img.shields.io/badge/-Documentation%20Website-brightgreen)](https://capstone-projects-2023-spring.github.io/project-discord-classroom/)
</div>

[![Discord Classroom Demo](https://img.youtube.com/vi/spUYv7YRjcU/0.jpg)](https://www.youtube.com/watch?v=spUYv7YRjcU&t=2650s)



## Keywords 

Section 704, Discord Bot, Python 3.7+, Database, Teaching Environment 

## How to Run Discord Classroom Bot

1) You will need to first create the Discord Server that you would like to use as a Classroom ([for help](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server-)).

2) Next you will need to invite the Bot with this [link](https://discord.com/api/oauth2/authorize?client_id=1069136471635800164&permissions=8&scope=bot) to join the classroom you have created.

3) Enter the server and you can now type ‘/’ and select help or type ‘/help’ to get more information on the Bot.

4) You can follow along with the Acceptance Test ([Here](https://docs.google.com/spreadsheets/d/1i7M14jydYnNDTcZuedH4e5BVZQyFxsuZoQAXXERoXSY/edit?usp=sharing)).

## Project Abstract 

This document proposes a Discord Application that allows users to create a learning environment. An 
educator can use the bot to set up features scheduling, setting up assignments, quizzes, and discussions, 
grading, attendance, polling, and role management. Educators can add TAs and students to the discord to 
and give them roles through the bot. Students will be able to access their grades, submit assignments, 
and connect with their fellow classmates. Additional Features to implement include: a channel dedicated 
for students to share notes with each other, a trivia session for students to test their knowledge against 
each other, a ticket system to ask the TA or professor questions, a section for educators to 
create/schedule announcements, allow students to “raise hand” when they have a question, and a 
command for personal reminders.

## High Level Requirement 

First the user will add the application to their Discord channel. Then the bot will fully customize the 
channel adding text and voice channels for general topics like assignments, discussions, syllabus, and so 
on. Then in a private channel the discord bot will display commands available to the educator that they can 
use to customize the channel and add content like assignments and quizzes. Through these commands 
is how the user (the teacher) interacts with the bot. Also, TAs and students will have 
commands they can use to make grading and learning easier.

## Conceptual Design 

The bot will be programmed in Python 3.9+ utilizing multiple libraries like pycord, supabase, and fastapi. Our database will be stored on Supabase which is a cloud storage application. We will also use FastAPI to deploy the API to connect to our database. 

## Background 

With the recent pandemic, online learning has become essential for students to continue their learning in 
a safe environment for both educators and students. This product would be used to make teaching from 
home an easier, less stressful activity. The main way educators are connecting with their students is 
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

## Required Resources 

For the entirety of this project, we use Python3 to build the Discord bot and creating our API to the database. The discord bot and API will be hosted on Google's Computer Engine costing about 6$ a month. Our database is hosted on Supabase for free. 

## Collaborators

<table>
<tr>
    <td align="center">
        <a href="https://github.com/timlopes17">
            <img src="https://avatars.githubusercontent.com/u/15525152?v=4" width="100;" alt="timlopes17"/>
            <br />
            <sub><b>Tim Lopes</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/tuj83407">
            <img src="https://avatars.githubusercontent.com/u/70284955?v=4" width="100;" alt="tuj83407"/>
            <br />
            <sub><b>Kiran Nixon</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/tun31876">
            <img src="https://avatars.githubusercontent.com/u/97766696?v=4" width="100;" alt="tun31876"/>
            <br />
            <sub><b>Tanvir Alam</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/BenBaldino">
            <img src="https://avatars.githubusercontent.com/u/112522605?v=4" width="100;" alt="BenBaldino"/>
            <br />
            <sub><b>Ben Baldino</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/Salte8">
            <img src="https://avatars.githubusercontent.com/u/63520132?v=4" width="100;" alt="Salte8"/>
            <br />
            <sub><b>Steven Altemose</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/rk2357">
            <img src="https://avatars.githubusercontent.com/u/91990873?v=4" width="100;" alt="rk2357"/>
            <br />
            <sub><b>Ryan Klein</b></sub>
        </a>
    </td>
    <td align="center">
        <a href="https://github.com/ApplebaumIan">
            <img src="https://avatars.githubusercontent.com/u/9451941?v=4" width="100;" alt="ApplebaumIan"/>
            <br />
            <sub><b>Ian Tyler Applebaum</b></sub>
        </a>
    </td>
    
</tr>
</table>
