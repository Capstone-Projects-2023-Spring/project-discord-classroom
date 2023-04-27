---
sidebar_position: 3
---

# Schedule

```mermaid
gantt
    title Discord Classroom Schedule
    dateFormat  YYYY-MM-DD
    
    section Elaboration Phase 
         Sprint 0: , 2023-02-08, 1w
         Software Development Plan Assignment: milestone, done, 2023-02-12, 1d

         Sprint 1: , 2023-02-15, 2w
         Design Document Part 1 (Architecture) Assignment: milestone, , 2023-02-19, 1d
         Design Document Part 2 (API) Assignment: milestone, , 2023-02-26, 1d
         Research Requirements needed For Project : , 2023-02-27, 1w
         Create Discord Bot : , 2023-02-19, 1d
         Import Bot to Discord Server: , 2023-02-19, 1d

        section Construction Phase 
         Sprint 2: , 2023-03-01, 1w
         Test Procedures Document Assignment: milestone, , 2023-03-05, 1d 
         Display All the Command list: , 2023-03-01, 12d
         Implement Logic For Bot to Customize Discord Server : , 2023-03-01, 4d
         Setup MySQL Database:  , 2023-03-01, 3d
         Create Database Tables :  , 2023-03-01, 3d 
         Host Bot with Sparkedhost :  , 2023-03-13, 1d
         Testing :  , 2023-03-13, 1w

         Milestone Demo 1 :crit, milestone,  , 2023-03-14, 1d
         Milestone Goal - Functional bot, hosted and accessible, with working database: milestone, 2023-03-14, 1d
         
         Sprint 3: , 2023-03-15, 2w
         Implement Logic To Determine Status of Command Issuer:  , 2023-03-15, 4d
         Verify Permission Level Before Executing an Action:  , 2023-03-15, 3d
         Structure a Comprehensive Database System:  , 2023-03-15, 6d 
         Implement Logic to Interact with Database with API:  , 2023-03-15, 5d
         Connect Database with Discord Bot :  , 2023-03-15, 1w 
         Store and Retrieve assignments:  , 2023-03-15, 4d
         Testing :  , 2023-03-15, 2w

         Milestone Demo 2 :crit, milestone,  , 2023-03-28, 1d
         Milestone Goal - The bot can facilitate appropriate interactions between educators and students: milestone, 2023-03-28, 1d

         Sprint 4: , 2023-03-29, 2w
         Educator Can Upload Quiz:  , 2023-03-29, 4d
         Student Presence Stored in Database:  , 2023-03-29, 4d
         Quiz Answers stored in Database and in Storage Service:  , 2023-03-29, 5d
         Educator Can Update Student's Grades:  , 2023-03-29, 4d
         Student Able to View Their Grade:  , 2023-03-29, 4d
         Testing :  , 2023-03-29, 2w

         Milestone Demo 3 :crit, milestone,  , 2023-04-11, 1d
         Milestone Goal - Educators and students are able to store, retrieve, and update school work: milestone, 2023-04-11, 1d
         
         Sprint 5: , 2023-04-12, 16d
         Student Can Open Ticket:  , 2023-04-12, 3d
         Educator views Number of Slots:  , 2023-04-14, 4d
         Educator create polls:  , 2023-04-15, 3d
         Poll Feedback Stored In Database:  , 2023-04-12, 4d
         Testing :  , 2023-04-12, 16d

         Final Presentation & Demo :crit, milestone,  , 2023-04-27, 1d
         Test Report Document Assignment: milestone, , 2023-05-06, 1d
```

# Milestones

## Milestone Demo 1

* Discord bot sets up the channel with preset Categories, Text Channels, Voice channels, and Roles

    * Assigns the owner of the Discord the educator role
    
    * Allows students to pick their sections within the "role" text channel
    
    * When the bot joins the discord server, it automatically sets up separate channels for the users
    
    * Educator can use `/ta` command to give users the Assistant role

* Educator uses the `/syllabus` command to upload the syllabus to the dsicord server

    * Bot reads the pdf file attachment with the `/syllabus` command
    
    * Bot parses through the PDF to print a text version of the syllabus to discord

* Help command for users to know how certain commands work

    * Discord command for `/help` with optional arguments
    
    * If an argument is given, it returns the syntax for that argument

* Poll command used by users to create polls for users to vote through reactions

    * The command itself implemented within the bot

    * Takes two required and more optional arguments for each option

    * The bot reacts to the poll it creates so the users can click on each reaction

## Milestone Demo 2

* Educator can create content for the classroom such as Assignments, Quizzes, and Discussions

    * `/assignment` command available to educators

    * `/quiz` command available to educators

    * `/discussion` command available to educators

* Educators can start lectures within the Discord voice channel

    * attendance command used to track which students attended the lecture

    * command to announce to the discord server that a lecture is about to start

## Milestone Demo 3

* Students can submit classroom work such as Assignments, Quizzes, and Discussions

    * `/submit` command for assignments

    * `/start` command for quizzes

* Teachers can look at the work students submitted and grade them

    * `/grade` command for educators

    * `/grades` command for students to check their grade

## Milestone Demo FINAL

* The bot can join multiple servers without conflicts between servers

    * Database is set up in a way to avoid conflicts

* Polished UI

    * All bot responses look professional with no spelling/grammar errors

* All testing commands removed
