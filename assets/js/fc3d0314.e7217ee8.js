"use strict";(self.webpackChunktu_cis_4398_docs_template=self.webpackChunktu_cis_4398_docs_template||[]).push([[1650],{3905:(e,t,n)=>{n.d(t,{Zo:()=>d,kt:()=>m});var s=n(7294);function a(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function o(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);t&&(s=s.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,s)}return n}function r(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?o(Object(n),!0).forEach((function(t){a(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):o(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function i(e,t){if(null==e)return{};var n,s,a=function(e,t){if(null==e)return{};var n,s,a={},o=Object.keys(e);for(s=0;s<o.length;s++)n=o[s],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(s=0;s<o.length;s++)n=o[s],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}var l=s.createContext({}),c=function(e){var t=s.useContext(l),n=t;return e&&(n="function"==typeof e?e(t):r(r({},t),e)),n},d=function(e){var t=c(e.components);return s.createElement(l.Provider,{value:t},e.children)},u="mdxType",p={inlineCode:"code",wrapper:function(e){var t=e.children;return s.createElement(s.Fragment,{},t)}},h=s.forwardRef((function(e,t){var n=e.components,a=e.mdxType,o=e.originalType,l=e.parentName,d=i(e,["components","mdxType","originalType","parentName"]),u=c(n),h=a,m=u["".concat(l,".").concat(h)]||u[h]||p[h]||o;return n?s.createElement(m,r(r({ref:t},d),{},{components:n})):s.createElement(m,r({ref:t},d))}));function m(e,t){var n=arguments,a=t&&t.mdxType;if("string"==typeof e||a){var o=n.length,r=new Array(o);r[0]=h;var i={};for(var l in t)hasOwnProperty.call(t,l)&&(i[l]=t[l]);i.originalType=e,i[u]="string"==typeof e?e:a,r[1]=i;for(var c=2;c<o;c++)r[c]=n[c];return s.createElement.apply(null,r)}return s.createElement.apply(null,n)}h.displayName="MDXCreateElement"},2233:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>l,contentTitle:()=>r,default:()=>u,frontMatter:()=>o,metadata:()=>i,toc:()=>c});var s=n(7462),a=(n(7294),n(3905));const o={sidebar_position:3},r="Acceptance test",i={unversionedId:"testing/acceptence-testing",id:"testing/acceptence-testing",title:"Acceptance test",description:"Use Case Acceptance Test will be performed to ensure that certain features are functional and work for the user's needs.",source:"@site/docs/testing/acceptence-testing.md",sourceDirName:"testing",slug:"/testing/acceptence-testing",permalink:"/project-discord-classroom/docs/testing/acceptence-testing",draft:!1,editUrl:"https://github.com/Capstone-Projects-2023-Spring/project-discord-classroom/edit/main/documentation/docs/testing/acceptence-testing.md",tags:[],version:"current",lastUpdatedBy:"Ben Baldino",sidebarPosition:3,frontMatter:{sidebar_position:3},sidebar:"docsSidebar",previous:{title:"Integration tests",permalink:"/project-discord-classroom/docs/testing/integration-testing"}},l={},c=[{value:"Add bot to the server",id:"add-bot-to-the-server",level:3},{value:"Help",id:"help",level:3},{value:"Create Roles",id:"create-roles",level:3},{value:"Attendance",id:"attendance",level:3},{value:"Poll",id:"poll",level:3},{value:"Private Question",id:"private-question",level:3},{value:"Class Ping",id:"class-ping",level:3},{value:"Assignments",id:"assignments",level:3},{value:"Quizzes",id:"quizzes",level:3},{value:"Discussions",id:"discussions",level:3},{value:"Testing Sheet",id:"testing-sheet",level:3}],d={toc:c};function u(e){let{components:t,...n}=e;return(0,a.kt)("wrapper",(0,s.Z)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,a.kt)("h1",{id:"acceptance-test"},"Acceptance test"),(0,a.kt)("p",null,"Use Case Acceptance Test will be performed to ensure that certain features are functional and work for the user's needs."),(0,a.kt)("h3",{id:"add-bot-to-the-server"},"Add bot to the server"),(0,a.kt)("p",null,"Actions: Open Discord and make a new Classroom server, then navigate to the bot\u2019s github page and add the bot to the server. "),(0,a.kt)("p",null,"Expected Result: The bot is added to the new classroom server and will populate the server with the various channels and helpful functions and features."),(0,a.kt)("h3",{id:"help"},"Help"),(0,a.kt)("p",null,"Actions: Type \u2018/\u2019 and select the help option."),(0,a.kt)("p",null,"Expected Results: The Bot will list all commands and what they do if the Educator needs assistance with any commands."),(0,a.kt)("h3",{id:"create-roles"},"Create Roles"),(0,a.kt)("p",null,"Actions: Type \u2018/\u2019 and select the roles option. Then enter the number(s) for the section(s) needed. Next click on a role to see that it adds that to their discord profile which can be checked by clicking on the users profile."),(0,a.kt)("p",null,"Expected Results: The Bot adds the roles into the roles channel and the user is able to select a role and see that it changes their profile in the server."),(0,a.kt)("h3",{id:"attendance"},"Attendance"),(0,a.kt)("p",null,"Actions: Type \u2018/\u2019 and select attendance and add a message to create a poll to be able to prompt students to check in for the class."),(0,a.kt)("p",null,"Expected Results: The Bot will start the check-in for attendance and will state the poll the user chose to show and record who marks that they have attended class for the day."),(0,a.kt)("h3",{id:"poll"},"Poll"),(0,a.kt)("p",null,"Actions: Type \u2018/\u2019 and select poll and add the options desired for the poll if the educator wants to ask if students are following or just to prompt a multiple choice question to make sure everyone is following the lesson."),(0,a.kt)("p",null,"Expected Results: The Bot will launch the poll, students will respond and the educator will get a better understanding of where to go with the lesson."),(0,a.kt)("h3",{id:"private-question"},"Private Question"),(0,a.kt)("p",null,"Actions: In the Public Questions Channel type \u2018/\u2019 and select private. Then add the question that is to be asked to the Educator/TA."),(0,a.kt)("p",null,"Expected Results: The Bot will delete what the user has typed and will star a private channel for just the user and Educator/TA for them to discuss the question privately."),(0,a.kt)("h3",{id:"class-ping"},"Class Ping"),(0,a.kt)("p",null,"Actions: Type \u2018/\u2019 and select announcement and add the message you would like to share with everyone, such as an answer to a problem brought up in a private chat that the Educator would like everyone to know about."),(0,a.kt)("p",null,"Expected Results: The Bot publishes the message in the Announcement channel and pings everyone so that they get a notification."),(0,a.kt)("h3",{id:"assignments"},"Assignments"),(0,a.kt)("p",null,"Actions: Type \u2019/\u2019 and select assignment and fill out the relevant information as prompted to create an assignment."),(0,a.kt)("p",null,"Expected Results: Creates an assignment and adds a new channel under the Assignment category with the name of the new Assignment."),(0,a.kt)("h3",{id:"quizzes"},"Quizzes"),(0,a.kt)("p",null,"Actions: Type \u2018/\u2019 and select quiz and fill out the relevant information as prompted. Next the questions and answers will be typed in to save the quiz file in the database."),(0,a.kt)("p",null,"Expected Results: The Bot will create a new channel under Quiz category with the name of the newly created quiz."),(0,a.kt)("h3",{id:"discussions"},"Discussions"),(0,a.kt)("p",null,"Actions: Type \u2018/\u2019 and select discussions and fill out the prompts with the relevant information."),(0,a.kt)("p",null,"Expected Results: The Bot will create a new channel with the name entered under the Submissions channel for the students to submit their responses."),(0,a.kt)("h3",{id:"testing-sheet"},"Testing Sheet"),(0,a.kt)("p",null,(0,a.kt)("img",{parentName:"p",src:"https://user-images.githubusercontent.com/112522605/222987986-ee07ea8a-08ca-40bf-99eb-87f148658325.png",alt:"image"}),"\n",(0,a.kt)("img",{parentName:"p",src:"https://user-images.githubusercontent.com/112522605/222987997-2e310a3f-f42b-424e-9b1d-cda3e5bd61a9.png",alt:"image"})))}u.isMDXComponent=!0}}]);