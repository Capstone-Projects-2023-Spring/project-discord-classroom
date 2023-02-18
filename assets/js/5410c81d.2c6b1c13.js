"use strict";(self.webpackChunktu_cis_4398_docs_template=self.webpackChunktu_cis_4398_docs_template||[]).push([[6654],{3905:(e,t,a)=>{a.d(t,{Zo:()=>d,kt:()=>h});var n=a(7294);function o(e,t,a){return t in e?Object.defineProperty(e,t,{value:a,enumerable:!0,configurable:!0,writable:!0}):e[t]=a,e}function r(e,t){var a=Object.keys(e);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(e);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),a.push.apply(a,n)}return a}function i(e){for(var t=1;t<arguments.length;t++){var a=null!=arguments[t]?arguments[t]:{};t%2?r(Object(a),!0).forEach((function(t){o(e,t,a[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(a)):r(Object(a)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(a,t))}))}return e}function l(e,t){if(null==e)return{};var a,n,o=function(e,t){if(null==e)return{};var a,n,o={},r=Object.keys(e);for(n=0;n<r.length;n++)a=r[n],t.indexOf(a)>=0||(o[a]=e[a]);return o}(e,t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);for(n=0;n<r.length;n++)a=r[n],t.indexOf(a)>=0||Object.prototype.propertyIsEnumerable.call(e,a)&&(o[a]=e[a])}return o}var s=n.createContext({}),c=function(e){var t=n.useContext(s),a=t;return e&&(a="function"==typeof e?e(t):i(i({},t),e)),a},d=function(e){var t=c(e.components);return n.createElement(s.Provider,{value:t},e.children)},m="mdxType",p={inlineCode:"code",wrapper:function(e){var t=e.children;return n.createElement(n.Fragment,{},t)}},u=n.forwardRef((function(e,t){var a=e.components,o=e.mdxType,r=e.originalType,s=e.parentName,d=l(e,["components","mdxType","originalType","parentName"]),m=c(a),u=o,h=m["".concat(s,".").concat(u)]||m[u]||p[u]||r;return a?n.createElement(h,i(i({ref:t},d),{},{components:a})):n.createElement(h,i({ref:t},d))}));function h(e,t){var a=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var r=a.length,i=new Array(r);i[0]=u;var l={};for(var s in t)hasOwnProperty.call(t,s)&&(l[s]=t[s]);l.originalType=e,l[m]="string"==typeof e?e:o,i[1]=l;for(var c=2;c<r;c++)i[c]=a[c];return n.createElement.apply(null,i)}return n.createElement.apply(null,a)}u.displayName="MDXCreateElement"},3144:(e,t,a)=>{a.r(t),a.d(t,{assets:()=>s,contentTitle:()=>i,default:()=>m,frontMatter:()=>r,metadata:()=>l,toc:()=>c});var n=a(7462),o=(a(7294),a(3905));const r={sidebar_position:1},i="Activities",l={unversionedId:"development-plan/activities",id:"development-plan/activities",title:"Activities",description:"Requirements Gathering",source:"@site/docs/development-plan/activities.md",sourceDirName:"development-plan",slug:"/development-plan/activities",permalink:"/project-discord-classroom/docs/development-plan/activities",draft:!1,editUrl:"https://github.com/Capstone-Projects-2023-Spring/project-discord-classroom/edit/main/documentation/docs/development-plan/activities.md",tags:[],version:"current",lastUpdatedBy:"Salte8",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"docsSidebar",previous:{title:"Software Development Plan",permalink:"/project-discord-classroom/docs/category/software-development-plan"},next:{title:"Tasks",permalink:"/project-discord-classroom/docs/development-plan/tasks"}},s={},c=[{value:"Requirements Gathering",id:"requirements-gathering",level:2},{value:"Top-Level Design",id:"top-level-design",level:2},{value:"Detailed Design",id:"detailed-design",level:2},{value:"Testing",id:"testing",level:2}],d={toc:c};function m(e){let{components:t,...a}=e;return(0,o.kt)("wrapper",(0,n.Z)({},d,a,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"activities"},"Activities"),(0,o.kt)("h2",{id:"requirements-gathering"},"Requirements Gathering"),(0,o.kt)("p",null,"In order to find out what features Discord Classroom should have we will look at other bots and virtual education enviornments to see what they offer. By looking at the most popular discord bot and other educational bots we can check the command layouts, what features are possible, and how bot messages are displayed for the user. For example most bot commands start with a '!' and then a verb for when a user wants to create something and a noun when they want to view something. Also these bots have useful features we did not original think of like reminders and timers. "),(0,o.kt)("p",null,"Another step to gathering resources is looking at popular virtual education enviornments like Canvas, BlackBoard, or Quizlet. These sources can help us pick more features to add to the Discord application that we did not original think of. Also they could provide a way to make creating quizzes or assignments by connecting directly to the site. Finally, we will have access to a college professor (Professor Ian) and can ask what features he would like to see added as a feature."),(0,o.kt)("h2",{id:"top-level-design"},"Top-Level Design"),(0,o.kt)("ol",null,(0,o.kt)("li",{parentName:"ol"},"Create a Discord bot used by educators to create a virtual educational enviornment within a Discord channel."),(0,o.kt)("li",{parentName:"ol"},"Allow the educator to set up assignments, discussion, quizzes and polls within the Discord channel through bot commands."),(0,o.kt)("li",{parentName:"ol"},"Allow the students to submit assignments, post dicussions, take quizzes, and react to polls all within Discord."),(0,o.kt)("li",{parentName:"ol"},"Allow the educator to host a class within a voice channel which will have automatic attendence and participation."),(0,o.kt)("li",{parentName:"ol"},"Allow students to get notified when class will start and let them join in the voice channel to attend class."),(0,o.kt)("li",{parentName:"ol"},"Allow the educator and TA to grade assigned work for each student."),(0,o.kt)("li",{parentName:"ol"},"Allow the students to check their grade for each school work they submitted."),(0,o.kt)("li",{parentName:"ol"},"Allow students to create tickets for TA/teacher to respond to."),(0,o.kt)("li",{parentName:"ol"},"Allow the teacher to make important announcements for the students."),(0,o.kt)("li",{parentName:"ol"},"Submitted assignments will be saved onto Google drive for easy access "),(0,o.kt)("li",{parentName:"ol"},"A database will be used to store information such as grades and attendence. ")),(0,o.kt)("h2",{id:"detailed-design"},"Detailed Design"),(0,o.kt)("ol",null,(0,o.kt)("li",{parentName:"ol"},"Develop classroom setup functionality that automates initial setup of the Discord server",(0,o.kt)("ol",{parentName:"li"},(0,o.kt)("li",{parentName:"ol"},"Implement role configuration that classifies users as an educator, assistant, or student"),(0,o.kt)("li",{parentName:"ol"},"Create text and audio channels specified by user"),(0,o.kt)("li",{parentName:"ol"},"Create cloud storage folder associated with Discord server   "))),(0,o.kt)("li",{parentName:"ol"},"Develop attendance functionality that allows users to take and report attendance",(0,o.kt)("ol",{parentName:"li"},(0,o.kt)("li",{parentName:"ol"},"Implement educator command that starts attendance process"),(0,o.kt)("li",{parentName:"ol"},"Implement student command that records their attendance"),(0,o.kt)("li",{parentName:"ol"},"Integrate with database for storage and access of attendance records"),(0,o.kt)("li",{parentName:"ol"},"Implement educator command that retrieves attendance records"))),(0,o.kt)("li",{parentName:"ol"},"Develop poll functionality that allows users to create and respond to polls",(0,o.kt)("ol",{parentName:"li"},(0,o.kt)("li",{parentName:"ol"},"Implement educator command that creates a poll"),(0,o.kt)("li",{parentName:"ol"},"Implement student command that allows them to respond to polls"))),(0,o.kt)("li",{parentName:"ol"},"Develop assignment functionality that allows users to create and submit assignments",(0,o.kt)("ol",{parentName:"li"},(0,o.kt)("li",{parentName:"ol"},"Implement educator command that creates an assignments and allows them to upload associated documents"),(0,o.kt)("li",{parentName:"ol"},"Implement student command that allows them to submit files"),(0,o.kt)("li",{parentName:"ol"},"Integrate with cloud storage service to store and access assignment submissions"))),(0,o.kt)("li",{parentName:"ol"},"Develop quiz functionality that allows users to create and take quizzes",(0,o.kt)("ol",{parentName:"li"},(0,o.kt)("li",{parentName:"ol"},"Implement educator command that creates a quiz"),(0,o.kt)("li",{parentName:"ol"},"Implement functionality for adding questions to the quiz"),(0,o.kt)("li",{parentName:"ol"},"Implement functionality for students to take the quiz"),(0,o.kt)("li",{parentName:"ol"},"Integrate with database to store quiz grades"),(0,o.kt)("li",{parentName:"ol"},"Implement functionality for generating quiz score report with class statistics"))),(0,o.kt)("li",{parentName:"ol"},"Develop gradebook functionality that allows users to store and access course grades",(0,o.kt)("ol",{parentName:"li"},(0,o.kt)("li",{parentName:"ol"},"Integrate server with database to store grades"),(0,o.kt)("li",{parentName:"ol"},"Implement educator command to generate grade reports for the course"),(0,o.kt)("li",{parentName:"ol"},"Implement student command to retrieve their own grades"))),(0,o.kt)("li",{parentName:"ol"},"Develop functionality that allows users to manage the classroom server",(0,o.kt)("ol",{parentName:"li"},(0,o.kt)("li",{parentName:"ol"},"Implement command for publishing course syllabus on server"),(0,o.kt)("li",{parentName:"ol"},"Implement command to generate server participation activity report")))),(0,o.kt)("h2",{id:"testing"},"Testing"),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},"Unit Test",(0,o.kt)("ul",{parentName:"li"},(0,o.kt)("li",{parentName:"ul"},"The team will conduct unit tests for testing individual components during the software development cycle. The unit tests will cover aspects such as command parsing, the expected output of functions, error handling, etc.")))),(0,o.kt)("ul",null,(0,o.kt)("li",{parentName:"ul"},"Functional Testing",(0,o.kt)("ul",{parentName:"li"},(0,o.kt)("li",{parentName:"ul"},"The team will conduct tests to verify that the Discord bot and FastAPI behave as expected. Functional testing will cover aspects such as the behavior of the bot with various commands, API responses, etc.")))))}m.isMDXComponent=!0}}]);