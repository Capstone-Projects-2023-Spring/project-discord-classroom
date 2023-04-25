"use strict";(self.webpackChunktu_cis_4398_docs_template=self.webpackChunktu_cis_4398_docs_template||[]).push([[3196],{3905:(e,t,n)=>{n.d(t,{Zo:()=>d,kt:()=>p});var r=n(7294);function o(e,t,n){return t in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n,e}function s(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function a(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?s(Object(n),!0).forEach((function(t){o(e,t,n[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):s(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function i(e,t){if(null==e)return{};var n,r,o=function(e,t){if(null==e)return{};var n,r,o={},s=Object.keys(e);for(r=0;r<s.length;r++)n=s[r],t.indexOf(n)>=0||(o[n]=e[n]);return o}(e,t);if(Object.getOwnPropertySymbols){var s=Object.getOwnPropertySymbols(e);for(r=0;r<s.length;r++)n=s[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(o[n]=e[n])}return o}var c=r.createContext({}),l=function(e){var t=r.useContext(c),n=t;return e&&(n="function"==typeof e?e(t):a(a({},t),e)),n},d=function(e){var t=l(e.components);return r.createElement(c.Provider,{value:t},e.children)},u="mdxType",h={inlineCode:"code",wrapper:function(e){var t=e.children;return r.createElement(r.Fragment,{},t)}},m=r.forwardRef((function(e,t){var n=e.components,o=e.mdxType,s=e.originalType,c=e.parentName,d=i(e,["components","mdxType","originalType","parentName"]),u=l(n),m=o,p=u["".concat(c,".").concat(m)]||u[m]||h[m]||s;return n?r.createElement(p,a(a({ref:t},d),{},{components:n})):r.createElement(p,a({ref:t},d))}));function p(e,t){var n=arguments,o=t&&t.mdxType;if("string"==typeof e||o){var s=n.length,a=new Array(s);a[0]=m;var i={};for(var c in t)hasOwnProperty.call(t,c)&&(i[c]=t[c]);i.originalType=e,i[u]="string"==typeof e?e:o,a[1]=i;for(var l=2;l<s;l++)a[l]=n[l];return r.createElement.apply(null,a)}return r.createElement.apply(null,n)}m.displayName="MDXCreateElement"},7781:(e,t,n)=>{n.r(t),n.d(t,{assets:()=>c,contentTitle:()=>a,default:()=>u,frontMatter:()=>s,metadata:()=>i,toc:()=>l});var r=n(7462),o=(n(7294),n(3905));const s={sidebar_position:1},a="System Overview",i={unversionedId:"requirements/system-overview",id:"requirements/system-overview",title:"System Overview",description:"Project Abstract",source:"@site/docs/requirements/system-overview.md",sourceDirName:"requirements",slug:"/requirements/system-overview",permalink:"/project-discord-classroom/docs/requirements/system-overview",draft:!1,editUrl:"https://github.com/Capstone-Projects-2023-Spring/project-discord-classroom/edit/main/documentation/docs/requirements/system-overview.md",tags:[],version:"current",lastUpdatedBy:"Tanvir",sidebarPosition:1,frontMatter:{sidebar_position:1},sidebar:"docsSidebar",previous:{title:"Requirements Specification",permalink:"/project-discord-classroom/docs/category/requirements-specification"},next:{title:"System Block Diagram",permalink:"/project-discord-classroom/docs/requirements/system-block-diagram"}},c={},l=[{value:"Project Abstract<br/>",id:"project-abstract",level:3},{value:"Conceptual Design",id:"conceptual-design",level:2},{value:"Background<br/>",id:"background",level:3},{value:"Required Resources<br/>",id:"required-resources",level:3}],d={toc:l};function u(e){let{components:t,...n}=e;return(0,o.kt)("wrapper",(0,r.Z)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,o.kt)("h1",{id:"system-overview"},"System Overview"),(0,o.kt)("h3",{id:"project-abstract"},"Project Abstract",(0,o.kt)("br",null)),(0,o.kt)("p",null,"The Classroom Bot is a Discord bot that is for educators or companies that want to create a learning environment in Discord for teaching. Some learning environments that are for school use and other video conferencing applications do not have features that can allow educators to create quizzes or assignments for the students in the same place that the lectures are occurring. Our goal is to create a streamlined experience that helps both students and educators without being overly complicated or requiring multiple web applications."),(0,o.kt)("p",null,"As an educator, they will have the ability to set quizzes, discussions, polls, and assignments pertaining to their teaching topics. This will allow the educator to see how the students are doing and manage their attendance and grades as needed. The owner of the server is the default educator for the classroom. As a student, they will have the ability to take quizzes, submit assignments, participate in discussions, and leave feedback. They can share notes and questions with fellow students or the educator and TA in the same environment that they attend class. The TA, which will have to be set by the educator, will have the ability to input grades and assist the educator with responding to student questions or other issues."),(0,o.kt)("p",null,"The bot will be for any learning environment and not limited to just schooling, but the initial ideas originated with a school environment in mind. A company may also take advantage of the learning space for internal information such as training and familiarizing new employees with their systems or procedures. By making it simple and including various commands, the idea is to have a ready-to-go classroom with just the addition of a bot to a server. By having the class be held in the same place as the discussions, assignments, and quizzes, the hope is that the learning environment feels open and easy to access. Students will have a quick and easy way of communicating with the educator or fellow students to help promote their learning and find answers to questions or problems they may have in short periods of time."),(0,o.kt)("h2",{id:"conceptual-design"},"Conceptual Design"),(0,o.kt)("p",null,"The bot will be programmed with Python 3.7 and will connect to a Supabase database. The bot will use simple SQL commands to add/retrieve data from the database. The bot will be hosted through Google Computer Engine."),(0,o.kt)("h3",{id:"background"},"Background",(0,o.kt)("br",null)),(0,o.kt)("p",null,"With the recent pandemic, online learning has become essential for students to continue their learning in\na safe environment for both teachers and students. This product would be used to make teaching from\nhome an easier, less stressful activity. The main way teachers are connecting with their students is\nthrough applications like canvas and blackboard. Although these sites do a great job with allowing\neducators to post assignments, quizzes, and grades, students rarely will use the site to connect with each\nother. Instead, students usually create discord channels to communicate with each other where the\nteachers and TAs are not involved in the discussion. Having the learning environment be on Discord itself\nwill help both the students connect with each other and allow the teachers and TAs to be part of the\nconversation. "),(0,o.kt)("p",null,"There is a similar Discord Bot as the one proposed called ",(0,o.kt)("a",{parentName:"p",href:"https://top.gg/bot/889078613817831495"},"\u201cStudyLion\u201d"),".\nThis bot promotes the idea of study communities where students gather\ntogether in rooms and study with each other. There are cool features like timers, achievements, and\npersonal profiles for users to feel more engaged. Since StudyLion is mainly just for students to connect\nwith each other, my application will be different since it will allow teachers to be in control of the discord\nenvironment. Also, StudyLion does not support services such as hosting quizzes and submitting\nassignments. "),(0,o.kt)("h3",{id:"required-resources"},"Required Resources",(0,o.kt)("br",null)),(0,o.kt)("p",null,"For the entirety of this project, we use Python3 to build the Discord bot and creating our API to the database. The discord bot and API will be hosted on Google's Computer Engine costing about 6$ a month. Our database is hosted on Supabase for free."))}u.isMDXComponent=!0}}]);