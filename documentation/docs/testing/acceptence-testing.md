---
sidebar_position: 3
---
# Acceptance test

Use Case Acceptance Test will be performed to ensure that certain features are functional and work for the user's needs.



### Add bot to the server

Actions: Open Discord and make a new Classroom server, then navigate to the bot’s github page and add the bot to the server. User will then accept to let the bot make changes by clicking the checkmark.

Expected Result: The bot is added to the new classroom server and will populate the server with the various channels and helpful functions and features.



### Help

Actions: Type ‘/help’ and select the help option.

Expected Results: The Bot will send a list of all commands and what they do as a DM if the Educator needs assistance with any commands.



### Lecture Attendance

Actions: Type ‘/lecture’ and select lecture attendance and add a number to indicate the amount of time you would like check-in.

Expected Results: The Bot will start the check-in for attendance and will stay open while there is still time for check-in.



### Poll

Actions: Type ‘/poll’ and select poll and add the options desired for the poll if the educator wants to ask if students are following or just to prompt a multiple choice question to make sure everyone is following the lesson.

Expected Results: The Bot will launch the poll, students will respond and the educator will get a better understanding of where to go with the lesson.



### Anonymous Poll

Actions: Type ‘/anon’ and select anon poll and add the options desired for the poll if the educator wants to ask if students are following or just to prompt a multiple choice question to make sure everyone is following the lesson.

Expected Results: The Bot will launch an anonymous poll, students will respond anonymously and the educator will get a better understanding of where to go with the lesson.



### Lecture Mute

Actions: Type ‘/lecture’ and select lecture mute.

Expected Results: Everyone in the voice channel besides the Educator will be muted.



### Lecture unmute

Actions: Type ‘/lecture’ and select lecture unmute.

Expected Results: Everyone in the voice channel will be unmuted.



### Lecture Breakout

Actions: Type ‘/lecture’ and select lecture breakout and then the number of rooms you would like.

Expected Results: Should make voice channels based on the number of rooms indicated.



### Create Assignment

Actions: Type ’/create’ and select create assignment and fill out the form with what you want the assignment to be or attach a file with the assignment that you would like to publish..

Expected Results: Creates an assignment and adds a new channel under the Assignment category with the name of the new Assignment.



### Create Quiz

Actions: Type ‘/create’ and select create quiz and fill out the relevant information as prompted. Next the questions and answers will be typed in to save the quiz file in the database.

Expected Results: The Bot will prompt the educator to enter the name, and questions for the quiz. It will then create a new channel under the Quiz category with the name of the newly created quiz.



### Create Discussion

Actions: Type ‘/create’ and select create discussion and fill out the prompts with the relevant information.

Expected Results: The Bot will create a new channel with the name entered under the Submissions channel for the students to submit their responses.



### Create Upload

Actions: Type ‘/create’ and select create upload. This will allow the Educator to upload the JSON that they have gotten before and use that quiz, assignment, or discussion. 

Expected Results: Bot should create the proper assignment, quiz or discussion based on the JSON uploaded..



### Edit

Actions: In the assignment, quiz, or discussion type ‘/edit’ and select edit and then fill out the information you would like to change.

Expected Results: The Educator will be able to edit and change the assignment, quiz, or discussion. 



### Upcoming

Actions: Type ‘/upcoming’ and select upcoming and then select the date you would like to be the end date.

Expected Results: The bot should grab all assignments, quizzes and discussions due up to the end date entered and add them to the Upcoming Category with an emoji to indicate what it is.



### Delete

Actions: Type ‘/delete’ and select delete while in the channel for the channel you wish to remove.

Expected Results: This will delete the current quiz, assignment, or discussion. 



### Syllabus

Actions: Type ‘/syllabus’ and select syllabus and upload the pdf of your syllabus.

Expected Results: The bot will add the syllabus to the syllabus category and will also add the file itself.



### Grade Quiz

Actions: In the Submissions select the quiz you want to grade and type ‘/grade quiz’ and select grade quiz and enter the score and the comments.

Expected Results: The grade in the students grade section should update with their grade and the comments left.



### Grade Assignment

Actions: In the Submissions select the assignment you want to grade and type ‘/grade assignment’ and select grade assignment and enter the score and the comments.


Expected Results: The grade in the students grade section should update with their grade and the comments left.



### Tutor Quiz

Actions: Type ‘tutor/’ and select tutor quiz, then fill out the number of questions, the subject and the grade level.

Expected Results: The bot will DM you with a number of questions that you input.



### Tutor Study

Actions: Type ‘/tutor’ and select tutor study, you can then upload a file with notes from class or powerpoint and make a study guide based on that information.

Expected Results: The bot will give you a breakdown of the file submitted.



###  Tutor Flashcards

Actions: Type ‘/tutor’ and select tutor flashcards, you can then submit your own topic or can copy and paste of the tutor study and submit that.

Expected Results: The bot will give you a DM with the questions and the answers, but the answers will be hidden until clicked.








## Commands that need a Student/2nd Account on the Server



### Private Question

Actions: In the Public Questions Channel type ‘/private’ and select private. Then add the question that is to be asked to the Educator/TA.

Expected Results: The Bot will delete what the user has typed and will start a private channel for just the user and Educator/TA for them to discuss the question privately.



### Close

Actions: Type ‘/close’ and select close in the private message when your question has been answered and then select the confirmation to close.

Expected Results: The private message should close.


### Attendance

Actions: Type ‘/attendance’ and select attendance. The student will then be informed on their attendance status.

Expected Results: Bot will tell student what their current attendance record is.



### Upload File

Actions: Type ‘/upload file’ and select upload file. The student can then attach the file they would like to use as their submission.

Expected Results: The assignment should be uploaded to the relevant assignment and should receive a message confirming their submission.



### Grade Edit 

Actions: In the Student’s grade channel type ‘/grade edit’ and select the grade edit, you will then need to add the link to the grade you would like to change (can right click the message and select copy link to message) then add the new score and comments.

Expected Results: The grade tab should have a new message with the updated grade and message.




### TA 

Actions: Type ‘/ta’ and select ta, you will then need to input the user you would like to make a TA.

Expected Results: The user typed should gain the TA role.



### EDU

Actions: Type ‘/edu’ and select edu, you will then need to input the user you would like to make an educator.

Expected Results: The user toyed should now have the Educator role.


### Testing Sheet

![image](https://user-images.githubusercontent.com/112522605/235012450-6787de8a-af8a-46d1-ab0c-dc791a1fe84a.png)
![image](https://user-images.githubusercontent.com/112522605/235012734-35dcfd40-bf8e-4b78-a25f-44d6c7a81a3e.png)
![image](https://user-images.githubusercontent.com/112522605/235012811-870d51af-2a77-4699-b1ba-c869b421b870.png)
![image](https://user-images.githubusercontent.com/112522605/235012832-f62ff003-33ed-4fdb-9ef3-2d9848613612.png)


