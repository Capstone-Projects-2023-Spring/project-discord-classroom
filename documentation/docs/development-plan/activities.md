---
sidebar_position: 1
---

# Activities

## Top-Level Design

1. Develop classroom setup functionality that automates initial setup of the Discord server
2. Develop attendance functionality that allows users to take and report attendance
3. Develop poll functionality that allows users to create and respond to polls
4. Develop assignment functionality that allows users to create and submit assignments
5. Develop quiz functionality that allows users to create and take quizzes
7. Develop gradebook functionality that allows users to store and access course grades
8. Develop functionality that allows users to manage the classroom server

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
