---
sidebar_position: 1
---

# Activities

## Requirements Gathering

In order to find out what features Discord Classroom should have we will look at other bots and virtual education enviornments to see what they offer. By looking at the most popular discord bot and other educational bots we can check the command layouts, what features are possible, and how bot messages are displayed for the user. For example most bot commands start with a '!' and then a verb for when a user wants to create something and a noun when they want to view something. Also these bots have useful features we did not original think of like reminders and timers. 

Another step to gathering resources is looking at popular virtual education enviornments like Canvas, BlackBoard, or Quizlet. These sources can help us pick more features to add to the Discord application that we did not original think of. Also they could provide a way to make creating quizzes or assignments by connecting directly to the site. Finally, we will have access to a college prossor (Professor Ian) and can ask what features he would like to see added as a feature.
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

## Testing
- Unit Test
  - The team will conduct unit tests for testing individual components during the software development cycle. The unit tests will cover aspects such as command parsing, the expected output of functions, error handling, etc.


- Functional Testing
  - The team will conduct tests to verify that the Discord bot and FastAPI behave as expected. Functional testing will cover aspects such as the behavior of the bot with various commands, API responses, etc.

 
