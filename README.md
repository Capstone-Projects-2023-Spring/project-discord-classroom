[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-f4981d0f882b2a3f0472912d15f9806d57e124e0fc890972558857b51b24a6f9.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=9911448)
<div align="center">

# Discord Classroom Bot
[![Report Issue on Jira](https://img.shields.io/badge/Report%20Issues-Jira-0052CC?style=flat&logo=jira-software)](https://temple-cis-projects-in-cs.atlassian.net/jira/software/c/projects/DC/issues)
[![Deploy Docs](https://github.com/ApplebaumIan/tu-cis-4398-docs-template/actions/workflows/deploy.yml/badge.svg)](https://github.com/Capstone-Projects-2023-Spring/project-discord-classroom/actions/workflows/deploy.yml)
[![Documentation Website Link](https://img.shields.io/badge/-Documentation%20Website-brightgreen)](https://capstone-projects-2023-spring.github.io/project-discord-classroom/)
</div>

## Video Demonstration

[![Discord Classroom Demo](https://img.youtube.com/vi/spUYv7YRjcU/0.jpg)](https://youtu.be/spUYv7YRjcU?t=2444)


## Keywords 

Section 704, Discord Bot, Python 3.7+, Database, Teaching Environment 

## How to Run Discord Classroom Bot

1) You will need to first create the Discord Server that you would like to use as a Classroom ([for help](https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server-)).

2) Next you will need to invite the Bot with this [link](https://discord.com/api/oauth2/authorize?client_id=1069136471635800164&permissions=8&scope=bot) to join the classroom you have created.

3) Enter the server and you can now type ‘/’ and select help or type ‘/help’ to get more information on the Bot.

4) You can follow along with the Acceptance Test ([Here](https://docs.google.com/spreadsheets/d/1i7M14jydYnNDTcZuedH4e5BVZQyFxsuZoQAXXERoXSY/edit?usp=sharing)).

## Project Abstract 

This document proposes a Discord Application designed to facilitate a comprehensive learning environment for educators. With this bot, educators can schedule assignments, quizzes, discussions, manage grading, attendance, polling, and role assignments. The bot allows educators to add TAs and students to the Discord server and assign roles through the bot. Students can access their grades, submit assignments, and communicate with their classmates. Additional features to be implemented include a dedicated channel for sharing notes, AI tools for studying, a ticket system for asking questions, a section for creating and scheduling announcements, and lecture tools.

## High Level Requirement 

To begin using the Discord Classroom Bot, the user must first add the application to their Discord server. The bot will then fully customize the server by adding text and voice channels for general topics, such as assignments, discussions, syllabus, and more. In a private channel, the Discord bot will display available commands for the educator to customize the server and add content like assignments and quizzes. These commands are how the user (the teacher) interacts with the bot. TAs and students will also have access to specific commands that make grading and learning more manageable.

## Conceptual Design 

The bot will be programmed in Python 3.9+ utilizing multiple libraries like pycord, supabase, and fastapi. Our database will be stored on Supabase which is a cloud storage application. We will also use FastAPI to deploy the API to connect to our database. 

## Background 

The recent pandemic has made online learning essential for students to continue their education in a safe environment for both educators and students. This product aims to make teaching from home easier and less stressful. While applications like Canvas and Blackboard allow educators to post assignments, quizzes, and grades, students seldom use these sites to connect with one another. Instead, they often create Discord channels to communicate with each other, where teachers and TAs are not involved in the discussion. Moving the learning environment to Discord itself will enable students to connect with one another and teachers and TAs to be part of the conversation.

A similar Discord bot to the proposed one is [“StudyLion”](https://top.gg/bot/889078613817831495). StudyLion promotes study communities where students gather in rooms to study together, with features such as timers, achievements, and personal profiles to engage users. However, StudyLion is mainly for students to connect with one another, while the proposed application allows teachers to control the Discord environment. Additionally, StudyLion does not support features such as hosting quizzes and submitting assignments, which this application aims to provide.

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
