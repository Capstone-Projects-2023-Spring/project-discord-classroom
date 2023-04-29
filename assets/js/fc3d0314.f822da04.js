"use strict";(self.webpackChunktu_cis_4398_docs_template=self.webpackChunktu_cis_4398_docs_template||[]).push([[650],{3905:(e,t,n)=>{n.d(t,{Zo:()=>r,kt:()=>m});var l=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function s(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var l=Object.getOwnPropertySymbols(e);t&&(l=l.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,l)}return n}function o(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?s(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):s(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function i(e,t){if(null==e)return{};var n,l,a=function(e,t){if(null==e)return{};var n,l,a={},s=Object.keys(e);for(l=0;l<s.length;l++)n=s[l],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);for(l=0;l<s.length;l++)n=s[l],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var u=l.createContext({}),d=function(e){var t=l.useContext(u),n=t;return e&&(n="function"==typeof e?e(t):o(o({},t),e)),n},r=function(e){var t=d(e.components);return l.createElement(u.Provider,{value:t},e.children)},c="mdxType",h={inlineCode:"code",wrapper:function(e){var t=e.children;return l.createElement(l.Fragment,{},t)}},p=l.forwardRef((function(e,t){var n=e.components,a=e.mdxType,s=e.originalType,u=e.parentName,r=i(e,["components","mdxType","originalType","parentName"]),c=d(n),p=a,m=c["".concat(u,".").concat(p)]||c[p]||h[p]||s;return n?l.createElement(m,o(o({ref:t},r),{},{components:n})):l.createElement(m,o({ref:t},r))}));function m(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var s=n.length,o=new Array(s);o[0]=p;var i={};for(var u in t)hasOwnProperty.call(t,u)&&(i[u]=t[u]);i.originalType=e,i[c]="string"==typeof e?e:a,o[1]=i;for(var d=2;d<s;d++)o[d]=n[d];return l.createElement.apply(null,o)}return l.createElement.apply(null,n)}p.displayName="MDXCreateElement"},2233:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>u,contentTitle:()=>o,default:()=>c,frontMatter:()=>s,metadata:()=>i,toc:()=>d});var l=n(7462),a=(n(7294),n(3905));const s={sidebar_position:3},o="Acceptance test",i={unversionedId:"testing/acceptence-testing",id:"testing/acceptence-testing",title:"Acceptance test",description:"Use Case Acceptance Test will be performed to ensure that certain features are functional and work for the user's needs.",source:"@site/docs/testing/acceptence-testing.md",sourceDirName:"testing",slug:"/testing/acceptence-testing",permalink:"/project-discord-classroom/docs/testing/acceptence-testing",draft:!1,editUrl:"https://github.com/Capstone-Projects-2023-Spring/project-discord-classroom/edit/main/documentation/docs/testing/acceptence-testing.md",tags:[],version:"current",lastUpdatedBy:"KiranNixon",sidebarPosition:3,frontMatter:{sidebar_position:3},sidebar:"docsSidebar",previous:{title:"Integration tests",permalink:"/project-discord-classroom/docs/testing/integration-testing"}},u={},d=[{value:"Add bot to the server",id:"add-bot-to-the-server",level:3},{value:"Help",id:"help",level:3},{value:"Lecture Attendance",id:"lecture-attendance",level:3},{value:"Poll",id:"poll",level:3},{value:"Anonymous Poll",id:"anonymous-poll",level:3},{value:"Lecture Mute",id:"lecture-mute",level:3},{value:"Lecture unmute",id:"lecture-unmute",level:3},{value:"Lecture Breakout",id:"lecture-breakout",level:3},{value:"Create Assignment",id:"create-assignment",level:3},{value:"Create Quiz",id:"create-quiz",level:3},{value:"Create Discussion",id:"create-discussion",level:3},{value:"Create Upload",id:"create-upload",level:3},{value:"Edit",id:"edit",level:3},{value:"Upcoming",id:"upcoming",level:3},{value:"Delete",id:"delete",level:3},{value:"Syllabus",id:"syllabus",level:3},{value:"Grade Quiz",id:"grade-quiz",level:3},{value:"Grade Assignment",id:"grade-assignment",level:3},{value:"Tutor Quiz",id:"tutor-quiz",level:3},{value:"Tutor Study",id:"tutor-study",level:3},{value:"Tutor Flashcards",id:"tutor-flashcards",level:3},{value:"Commands that need a Student/2nd Account on the Server",id:"commands-that-need-a-student2nd-account-on-the-server",level:2},{value:"Private Question",id:"private-question",level:3},{value:"Close",id:"close",level:3},{value:"Attendance",id:"attendance",level:3},{value:"Upload File",id:"upload-file",level:3},{value:"Grade Edit",id:"grade-edit",level:3},{value:"TA",id:"ta",level:3},{value:"EDU",id:"edu",level:3},{value:"Testing Sheet",id:"testing-sheet",level:3}],r={toc:d};function c(e){let{components:t,...n}=e;return(0,a.kt)("wrapper",(0,l.Z)({},r,n,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"acceptance-test"},"Acceptance test"),(0,a.kt)("p",null,"Use Case Acceptance Test will be performed to ensure that certain features are functional and work for the user's needs."),(0,a.kt)("h3",{id:"add-bot-to-the-server"},"Add bot to the server"),(0,a.kt)("p",null,"Actions: Open Discord and make a new Classroom server, then navigate to the bot\u2019s github page and add the bot to the server. User will then accept to let the bot make changes by clicking the checkmark."),(0,a.kt)("p",null,"Expected Result: The bot is added to the new classroom server and will populate the server with the various channels and helpful functions and features."),(0,a.kt)("h3",{id:"help"},"Help"),(0,a.kt)("p",null,"Actions: Type \u2018/help\u2019 and select the help option."),(0,a.kt)("p",null,"Expected Results: The Bot will send a list of all commands and what they do as a DM if the Educator needs assistance with any commands."),(0,a.kt)("h3",{id:"lecture-attendance"},"Lecture Attendance"),(0,a.kt)("p",null,"Actions: Type \u2018/lecture\u2019 and select lecture attendance and add a number to indicate the amount of time you would like check-in."),(0,a.kt)("p",null,"Expected Results: The Bot will start the check-in for attendance and will stay open while there is still time for check-in."),(0,a.kt)("h3",{id:"poll"},"Poll"),(0,a.kt)("p",null,"Actions: Type \u2018/poll\u2019 and select poll and add the options desired for the poll if the educator wants to ask if students are following or just to prompt a multiple choice question to make sure everyone is following the lesson."),(0,a.kt)("p",null,"Expected Results: The Bot will launch the poll, students will respond and the educator will get a better understanding of where to go with the lesson."),(0,a.kt)("h3",{id:"anonymous-poll"},"Anonymous Poll"),(0,a.kt)("p",null,"Actions: Type \u2018/anon\u2019 and select anon poll and add the options desired for the poll if the educator wants to ask if students are following or just to prompt a multiple choice question to make sure everyone is following the lesson."),(0,a.kt)("p",null,"Expected Results: The Bot will launch an anonymous poll, students will respond anonymously and the educator will get a better understanding of where to go with the lesson."),(0,a.kt)("h3",{id:"lecture-mute"},"Lecture Mute"),(0,a.kt)("p",null,"Actions: Type \u2018/lecture\u2019 and select lecture mute."),(0,a.kt)("p",null,"Expected Results: Everyone in the voice channel besides the Educator will be muted."),(0,a.kt)("h3",{id:"lecture-unmute"},"Lecture unmute"),(0,a.kt)("p",null,"Actions: Type \u2018/lecture\u2019 and select lecture unmute."),(0,a.kt)("p",null,"Expected Results: Everyone in the voice channel will be unmuted."),(0,a.kt)("h3",{id:"lecture-breakout"},"Lecture Breakout"),(0,a.kt)("p",null,"Actions: Type \u2018/lecture\u2019 and select lecture breakout and then the number of rooms you would like."),(0,a.kt)("p",null,"Expected Results: Should make voice channels based on the number of rooms indicated."),(0,a.kt)("h3",{id:"create-assignment"},"Create Assignment"),(0,a.kt)("p",null,"Actions: Type \u2019/create\u2019 and select create assignment and fill out the form with what you want the assignment to be or attach a file with the assignment that you would like to publish.."),(0,a.kt)("p",null,"Expected Results: Creates an assignment and adds a new channel under the Assignment category with the name of the new Assignment."),(0,a.kt)("h3",{id:"create-quiz"},"Create Quiz"),(0,a.kt)("p",null,"Actions: Type \u2018/create\u2019 and select create quiz and fill out the relevant information as prompted. Next the questions and answers will be typed in to save the quiz file in the database."),(0,a.kt)("p",null,"Expected Results: The Bot will prompt the educator to enter the name, and questions for the quiz. It will then create a new channel under the Quiz category with the name of the newly created quiz."),(0,a.kt)("h3",{id:"create-discussion"},"Create Discussion"),(0,a.kt)("p",null,"Actions: Type \u2018/create\u2019 and select create discussion and fill out the prompts with the relevant information."),(0,a.kt)("p",null,"Expected Results: The Bot will create a new channel with the name entered under the Submissions channel for the students to submit their responses."),(0,a.kt)("h3",{id:"create-upload"},"Create Upload"),(0,a.kt)("p",null,"Actions: Type \u2018/create\u2019 and select create upload. This will allow the Educator to upload the JSON that they have gotten before and use that quiz, assignment, or discussion. "),(0,a.kt)("p",null,"Expected Results: Bot should create the proper assignment, quiz or discussion based on the JSON uploaded.."),(0,a.kt)("h3",{id:"edit"},"Edit"),(0,a.kt)("p",null,"Actions: In the assignment, quiz, or discussion type \u2018/edit\u2019 and select edit and then fill out the information you would like to change."),(0,a.kt)("p",null,"Expected Results: The Educator will be able to edit and change the assignment, quiz, or discussion. "),(0,a.kt)("h3",{id:"upcoming"},"Upcoming"),(0,a.kt)("p",null,"Actions: Type \u2018/upcoming\u2019 and select upcoming and then select the date you would like to be the end date."),(0,a.kt)("p",null,"Expected Results: The bot should grab all assignments, quizzes and discussions due up to the end date entered and add them to the Upcoming Category with an emoji to indicate what it is."),(0,a.kt)("h3",{id:"delete"},"Delete"),(0,a.kt)("p",null,"Actions: Type \u2018/delete\u2019 and select delete while in the channel for the channel you wish to remove."),(0,a.kt)("p",null,"Expected Results: This will delete the current quiz, assignment, or discussion. "),(0,a.kt)("h3",{id:"syllabus"},"Syllabus"),(0,a.kt)("p",null,"Actions: Type \u2018/syllabus\u2019 and select syllabus and upload the pdf of your syllabus."),(0,a.kt)("p",null,"Expected Results: The bot will add the syllabus to the syllabus category and will also add the file itself."),(0,a.kt)("h3",{id:"grade-quiz"},"Grade Quiz"),(0,a.kt)("p",null,"Actions: In the Submissions select the quiz you want to grade and type \u2018/grade quiz\u2019 and select grade quiz and enter the score and the comments."),(0,a.kt)("p",null,"Expected Results: The grade in the students grade section should update with their grade and the comments left."),(0,a.kt)("h3",{id:"grade-assignment"},"Grade Assignment"),(0,a.kt)("p",null,"Actions: In the Submissions select the assignment you want to grade and type \u2018/grade assignment\u2019 and select grade assignment and enter the score and the comments."),(0,a.kt)("p",null,"Expected Results: The grade in the students grade section should update with their grade and the comments left."),(0,a.kt)("h3",{id:"tutor-quiz"},"Tutor Quiz"),(0,a.kt)("p",null,"Actions: Type \u2018tutor/\u2019 and select tutor quiz, then fill out the number of questions, the subject and the grade level."),(0,a.kt)("p",null,"Expected Results: The bot will DM you with a number of questions that you input."),(0,a.kt)("h3",{id:"tutor-study"},"Tutor Study"),(0,a.kt)("p",null,"Actions: Type \u2018/tutor\u2019 and select tutor study, you can then upload a file with notes from class or powerpoint and make a study guide based on that information."),(0,a.kt)("p",null,"Expected Results: The bot will give you a breakdown of the file submitted."),(0,a.kt)("h3",{id:"tutor-flashcards"},"Tutor Flashcards"),(0,a.kt)("p",null,"Actions: Type \u2018/tutor\u2019 and select tutor flashcards, you can then submit your own topic or can copy and paste of the tutor study and submit that."),(0,a.kt)("p",null,"Expected Results: The bot will give you a DM with the questions and the answers, but the answers will be hidden until clicked."),(0,a.kt)("h2",{id:"commands-that-need-a-student2nd-account-on-the-server"},"Commands that need a Student/2nd Account on the Server"),(0,a.kt)("h3",{id:"private-question"},"Private Question"),(0,a.kt)("p",null,"Actions: In the Public Questions Channel type \u2018/private\u2019 and select private. Then add the question that is to be asked to the Educator/TA."),(0,a.kt)("p",null,"Expected Results: The Bot will delete what the user has typed and will start a private channel for just the user and Educator/TA for them to discuss the question privately."),(0,a.kt)("h3",{id:"close"},"Close"),(0,a.kt)("p",null,"Actions: Type \u2018/close\u2019 and select close in the private message when your question has been answered and then select the confirmation to close."),(0,a.kt)("p",null,"Expected Results: The private message should close."),(0,a.kt)("h3",{id:"attendance"},"Attendance"),(0,a.kt)("p",null,"Actions: Type \u2018/attendance\u2019 and select attendance. The student will then be informed on their attendance status."),(0,a.kt)("p",null,"Expected Results: Bot will tell student what their current attendance record is."),(0,a.kt)("h3",{id:"upload-file"},"Upload File"),(0,a.kt)("p",null,"Actions: Type \u2018/upload file\u2019 and select upload file. The student can then attach the file they would like to use as their submission."),(0,a.kt)("p",null,"Expected Results: The assignment should be uploaded to the relevant assignment and should receive a message confirming their submission."),(0,a.kt)("h3",{id:"grade-edit"},"Grade Edit"),(0,a.kt)("p",null,"Actions: In the Student\u2019s grade channel type \u2018/grade edit\u2019 and select the grade edit, you will then need to add the link to the grade you would like to change (can right click the message and select copy link to message) then add the new score and comments."),(0,a.kt)("p",null,"Expected Results: The grade tab should have a new message with the updated grade and message."),(0,a.kt)("h3",{id:"ta"},"TA"),(0,a.kt)("p",null,"Actions: Type \u2018/ta\u2019 and select ta, you will then need to input the user you would like to make a TA."),(0,a.kt)("p",null,"Expected Results: The user typed should gain the TA role."),(0,a.kt)("h3",{id:"edu"},"EDU"),(0,a.kt)("p",null,"Actions: Type \u2018/edu\u2019 and select edu, you will then need to input the user you would like to make an educator."),(0,a.kt)("p",null,"Expected Results: The user toyed should now have the Educator role."),(0,a.kt)("h3",{id:"testing-sheet"},"Testing Sheet"),(0,a.kt)("p",null,(0,a.kt)("img",{parentName:"p",src:"https://user-images.githubusercontent.com/112522605/235012450-6787de8a-af8a-46d1-ab0c-dc791a1fe84a.png",alt:"image"}),"\n",(0,a.kt)("img",{parentName:"p",src:"https://user-images.githubusercontent.com/112522605/235012734-35dcfd40-bf8e-4b78-a25f-44d6c7a81a3e.png",alt:"image"}),"\n",(0,a.kt)("img",{parentName:"p",src:"https://user-images.githubusercontent.com/112522605/235012811-870d51af-2a77-4699-b1ba-c869b421b870.png",alt:"image"}),"\n",(0,a.kt)("img",{parentName:"p",src:"https://user-images.githubusercontent.com/112522605/235012832-f62ff003-33ed-4fdb-9ef3-2d9848613612.png",alt:"image"})))}c.isMDXComponent=!0}}]);