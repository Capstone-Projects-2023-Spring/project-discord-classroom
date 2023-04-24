---
sidebar_position: 1
---

# Activities

## Requirements Gathering

In order to find out what features Discord Classroom should have we will look at other bots and virtual education enviornments to see what they offer. By looking at the most popular discord bot and other educational bots we can check the command layouts, what features are possible, and how bot messages are displayed for the user. For example most bot commands start with a '!' and then a verb for when a user wants to create something and a noun when they want to view something. Also these bots have useful features we did not original think of like reminders and timers. 

Another step to gathering resources is looking at popular virtual education enviornments like Canvas, BlackBoard, or Quizlet. These sources can help us pick more features to add to the Discord application that we did not original think of. Also they could provide a way to make creating quizzes or assignments by connecting directly to the site. Finally, we will have access to a college professor (Professor Ian) and can ask what features he would like to see added as a feature.
## Top-Level Design

1. Create a Discord bot used by educators to create a virtual educational enviornment within a Discord channel.
2. Allow the educator to set up assignments, discussion, quizzes and polls within the Discord channel through bot commands.
3. Allow the students to submit assignments, post dicussions, take quizzes, and react to polls all within Discord.
4. Allow the educator to host a class within a voice channel which will have automatic attendence and participation.
5. Allow students to get notified when class will start and let them join in the voice channel to attend class.
6. Allow the educator and TA to grade assigned work for each student.
7. Allow the students to check their grade for each school work they submitted.
8. Allow students to create tickets for TA/teacher to respond to.
9. Allow the teacher to make important announcements for the students.
10. Submitted assignments will be saved onto Google drive for easy access 
11. A database will be used to store information such as grades and attendence. 

## Detailed Design

1. Develop classroom setup functionality that automates initial setup of the Discord server
    1. Implement role configuration that classifies users as an educator, assistant, or student
    2. Create text and audio channels specified by user
    3. Create cloud storage folder associated with Discord server   
2. Develop attendance functionality that allows users to take and report attendance
    1. Implement educator command that starts attendance process
    2. Implement student command that records their attendance
    3. Integrate with database for storage and access of attendance records
    4. Implement educator command that retrieves attendance records
3. Develop poll functionality that allows users to create and respond to polls
    1. Implement educator command that creates a poll
    2. Implement student command that allows them to respond to polls
4. Develop assignment functionality that allows users to create and submit assignments
    1. Implement educator command that creates an assignments and allows them to upload associated documents
    2. Implement student command that allows them to submit files
    3. Integrate with cloud storage service to store and access assignment submissions
5. Develop quiz functionality that allows users to create and take quizzes
    1. Implement educator command that creates a quiz
    2. Implement functionality for adding questions to the quiz
    3. Implement functionality for students to take the quiz
    4. Integrate with database to store quiz grades
    5. Implement functionality for generating quiz score report with class statistics
6. Develop gradebook functionality that allows users to store and access course grades
    1. Integrate server with database to store grades
    2. Implement educator command to generate grade reports for the course
    3. Implement student command to retrieve their own grades
7. Develop functionality that allows users to manage the classroom server
    1. Implement command for publishing course syllabus on server
    2. Implement command to generate server participation activity report

## Testing
- Unit Test
  - The team will conduct unit tests for testing individual components during the software development cycle. The unit tests will cover aspects such as command parsing, the expected output of functions, error handling, etc.
  - The unit testing will be done using Pytest. 

- Functional Testing
  - The team will conduct tests to verify that the Discord bot and FastAPI behave as expected. Functional testing will cover aspects such as the behavior of the bot with various commands, API responses, etc.

- Acceptance Test
  - Our team will create a document containing our non-functional and functional requirements that will be used to verify and check that our bot is both easy to use and is functioning as expected.
