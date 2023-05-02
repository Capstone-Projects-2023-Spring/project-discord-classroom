"use strict";(self.webpackChunktu_cis_4398_docs_template=self.webpackChunktu_cis_4398_docs_template||[]).push([[195],{8140:(e,t,s)=>{s.r(t),s.d(t,{default:()=>A});var a=s(7294),n=s(6010),o=s(9960),r=s(2263),i=s(782),l=s(7462),c=s(3905);const u={toc:[{value:"Video Demonstration",id:"video-demonstration",level:2},{value:"Keywords",id:"keywords",level:2},{value:"How to Run Discord Classroom Bot",id:"how-to-run-discord-classroom-bot",level:2},{value:"Project Abstract",id:"project-abstract",level:2},{value:"High Level Requirement",id:"high-level-requirement",level:2},{value:"Conceptual Design",id:"conceptual-design",level:2},{value:"Background",id:"background",level:2},{value:"Required Resources",id:"required-resources",level:2},{value:"Collaborators",id:"collaborators",level:2}]};function d(e){let{components:t,...s}=e;return(0,c.kt)("wrapper",(0,l.Z)({},u,s,{components:t,mdxType:"MDXLayout"}),(0,c.kt)("p",null,(0,c.kt)("a",{parentName:"p",href:"https://classroom.github.com/open-in-codespaces?assignment_repo_id=9911448"},(0,c.kt)("img",{parentName:"a",src:"https://classroom.github.com/assets/launch-codespace-f4981d0f882b2a3f0472912d15f9806d57e124e0fc890972558857b51b24a6f9.svg",alt:"Open in Codespaces"}))),(0,c.kt)("div",{align:"center"},(0,c.kt)("h1",{id:"discord-classroom-bot"},"Discord Classroom Bot"),(0,c.kt)("p",null,(0,c.kt)("a",{parentName:"p",href:"https://temple-cis-projects-in-cs.atlassian.net/jira/software/c/projects/DC/issues"},(0,c.kt)("img",{parentName:"a",src:"https://img.shields.io/badge/Report%20Issues-Jira-0052CC?style=flat&logo=jira-software",alt:"Report Issue on Jira"})),"\n",(0,c.kt)("a",{parentName:"p",href:"https://github.com/Capstone-Projects-2023-Spring/project-discord-classroom/actions/workflows/deploy.yml"},(0,c.kt)("img",{parentName:"a",src:"https://github.com/ApplebaumIan/tu-cis-4398-docs-template/actions/workflows/deploy.yml/badge.svg",alt:"Deploy Docs"})),"\n",(0,c.kt)("a",{parentName:"p",href:"https://capstone-projects-2023-spring.github.io/project-discord-classroom/"},(0,c.kt)("img",{parentName:"a",src:"https://img.shields.io/badge/-Documentation%20Website-brightgreen",alt:"Documentation Website Link"})))),(0,c.kt)("h2",{id:"video-demonstration"},"Video Demonstration"),(0,c.kt)("p",null,(0,c.kt)("a",{parentName:"p",href:"https://youtu.be/spUYv7YRjcU?t=2444"},(0,c.kt)("img",{parentName:"a",src:"https://img.youtube.com/vi/spUYv7YRjcU/0.jpg",alt:"Discord Classroom Demo"}))),(0,c.kt)("h2",{id:"keywords"},"Keywords"),(0,c.kt)("p",null,"Section 704, Discord Bot, Python 3.7+, Database, Teaching Environment "),(0,c.kt)("h2",{id:"how-to-run-discord-classroom-bot"},"How to Run Discord Classroom Bot"),(0,c.kt)("p",null,"1) You will need to first create the Discord Server that you would like to use as a Classroom (",(0,c.kt)("a",{parentName:"p",href:"https://support.discord.com/hc/en-us/articles/204849977-How-do-I-create-a-server-"},"for help"),")."),(0,c.kt)("p",null,"2) Next you will need to invite the Bot with this ",(0,c.kt)("a",{parentName:"p",href:"https://discord.com/api/oauth2/authorize?client_id=1069136471635800164&permissions=8&scope=bot"},"link")," to join the classroom you have created."),(0,c.kt)("p",null,"3) Enter the server and you can now type \u2018/\u2019 and select help or type \u2018/help\u2019 to get more information on the Bot."),(0,c.kt)("p",null,"4) You can follow along with the Acceptance Test (",(0,c.kt)("a",{parentName:"p",href:"https://docs.google.com/spreadsheets/d/1i7M14jydYnNDTcZuedH4e5BVZQyFxsuZoQAXXERoXSY/edit?usp=sharing"},"Here"),")."),(0,c.kt)("h2",{id:"project-abstract"},"Project Abstract"),(0,c.kt)("p",null,"This document proposes a Discord Application designed to facilitate a comprehensive learning environment for educators. With this bot, educators can schedule assignments, quizzes, discussions, manage grading, attendance, polling, and role assignments. The bot allows educators to add TAs and students to the Discord server and assign roles through the bot. Students can access their grades, submit assignments, and communicate with their classmates. Additional features to be implemented include a dedicated channel for sharing notes, AI tools for studying, a ticket system for asking questions, a section for creating and scheduling announcements, and lecture tools."),(0,c.kt)("h2",{id:"high-level-requirement"},"High Level Requirement"),(0,c.kt)("p",null,"To begin using the Discord Classroom Bot, the user must first add the application to their Discord server. The bot will then fully customize the server by adding text and voice channels for general topics, such as assignments, discussions, syllabus, and more. In a private channel, the Discord bot will display available commands for the educator to customize the server and add content like assignments and quizzes. These commands are how the user (the teacher) interacts with the bot. TAs and students will also have access to specific commands that make grading and learning more manageable."),(0,c.kt)("h2",{id:"conceptual-design"},"Conceptual Design"),(0,c.kt)("p",null,"The bot will be programmed in Python 3.9+ utilizing multiple libraries like pycord, supabase, and fastapi. Our database will be stored on Supabase which is a cloud storage application. We will also use FastAPI to deploy the API to connect to our database. "),(0,c.kt)("h2",{id:"background"},"Background"),(0,c.kt)("p",null,"The recent pandemic has made online learning essential for students to continue their education in a safe environment for both educators and students. This product aims to make teaching from home easier and less stressful. While applications like Canvas and Blackboard allow educators to post assignments, quizzes, and grades, students seldom use these sites to connect with one another. Instead, they often create Discord channels to communicate with each other, where teachers and TAs are not involved in the discussion. Moving the learning environment to Discord itself will enable students to connect with one another and teachers and TAs to be part of the conversation."),(0,c.kt)("p",null,"A similar Discord bot to the proposed one is ",(0,c.kt)("a",{parentName:"p",href:"https://top.gg/bot/889078613817831495"},"\u201cStudyLion\u201d"),". StudyLion promotes study communities where students gather in rooms to study together, with features such as timers, achievements, and personal profiles to engage users. However, StudyLion is mainly for students to connect with one another, while the proposed application allows teachers to control the Discord environment. Additionally, StudyLion does not support features such as hosting quizzes and submitting assignments, which this application aims to provide."),(0,c.kt)("h2",{id:"required-resources"},"Required Resources"),(0,c.kt)("p",null,"For the entirety of this project, we use Python3 to build the Discord bot and creating our API to the database. The discord bot and API will be hosted on Google's Computer Engine costing about 6$ a month. Our database is hosted on Supabase for free. "),(0,c.kt)("h2",{id:"collaborators"},"Collaborators"),(0,c.kt)("table",null,(0,c.kt)("tr",null,(0,c.kt)("td",{align:"center"},(0,c.kt)("a",{href:"https://github.com/timlopes17"},(0,c.kt)("img",{src:"https://avatars.githubusercontent.com/u/15525152?v=4",width:"100;",alt:"timlopes17"}),(0,c.kt)("br",null),(0,c.kt)("sub",null,(0,c.kt)("b",null,"Tim Lopes")))),(0,c.kt)("td",{align:"center"},(0,c.kt)("a",{href:"https://github.com/tuj83407"},(0,c.kt)("img",{src:"https://avatars.githubusercontent.com/u/70284955?v=4",width:"100;",alt:"tuj83407"}),(0,c.kt)("br",null),(0,c.kt)("sub",null,(0,c.kt)("b",null,"Kiran Nixon")))),(0,c.kt)("td",{align:"center"},(0,c.kt)("a",{href:"https://github.com/tun31876"},(0,c.kt)("img",{src:"https://avatars.githubusercontent.com/u/97766696?v=4",width:"100;",alt:"tun31876"}),(0,c.kt)("br",null),(0,c.kt)("sub",null,(0,c.kt)("b",null,"Tanvir Alam")))),(0,c.kt)("td",{align:"center"},(0,c.kt)("a",{href:"https://github.com/BenBaldino"},(0,c.kt)("img",{src:"https://avatars.githubusercontent.com/u/112522605?v=4",width:"100;",alt:"BenBaldino"}),(0,c.kt)("br",null),(0,c.kt)("sub",null,(0,c.kt)("b",null,"Ben Baldino")))),(0,c.kt)("td",{align:"center"},(0,c.kt)("a",{href:"https://github.com/Salte8"},(0,c.kt)("img",{src:"https://avatars.githubusercontent.com/u/63520132?v=4",width:"100;",alt:"Salte8"}),(0,c.kt)("br",null),(0,c.kt)("sub",null,(0,c.kt)("b",null,"Steven Altemose")))),(0,c.kt)("td",{align:"center"},(0,c.kt)("a",{href:"https://github.com/rk2357"},(0,c.kt)("img",{src:"https://avatars.githubusercontent.com/u/91990873?v=4",width:"100;",alt:"rk2357"}),(0,c.kt)("br",null),(0,c.kt)("sub",null,(0,c.kt)("b",null,"Ryan Klein")))),(0,c.kt)("td",{align:"center"},(0,c.kt)("a",{href:"https://github.com/ApplebaumIan"},(0,c.kt)("img",{src:"https://avatars.githubusercontent.com/u/9451941?v=4",width:"100;",alt:"ApplebaumIan"}),(0,c.kt)("br",null),(0,c.kt)("sub",null,(0,c.kt)("b",null,"Ian Tyler Applebaum")))))))}function h(){return a.createElement("div",{className:"container",style:{marginTop:"50px",marginBottom:"100px"}},a.createElement(d,null))}d.isMDXComponent=!0;const m="heroBanner_qdFl",p="buttons_AeoN";var g=s(6706);function b(){const{siteConfig:e}=(0,r.Z)();return a.createElement("header",{className:(0,n.Z)("hero hero--primary",m)},a.createElement("div",{className:"container"},a.createElement("h1",{className:"hero__title"},e.title),a.createElement("p",{className:"hero__subtitle"},e.tagline),a.createElement("div",{className:p},a.createElement(o.Z,{className:"button button--secondary button--lg",to:"/tutorial/intro"},"Classroom Installation Tutorial"))))}function A(){const{siteConfig:e}=(0,r.Z)();return a.createElement(i.Z,{title:`Hello from ${e.title}`,description:"Description will go into a meta tag in <head />"},a.createElement(b,null),a.createElement("main",null,a.createElement(g.Z,null,a.createElement(h,null))))}},6706:(e,t,s)=>{s.d(t,{Z:()=>o});var a=s(7294),n=s(4912);function o(e){return a.createElement(a.Fragment,null,a.createElement(n.Z,e))}},2414:(e,t,s)=>{s.d(t,{Z:()=>n});var a=s(7294);const n={React:a,...a,Figure:function(e){function t(){return t=e.id?e.id:(t=(t=(t=e.caption).replaceAll("."," ")).replaceAll(" ","-")).toLowerCase()}return a.createElement("figure",{id:t(),align:e.align?e.align:"center",style:e.style?e.style:{}},e.children,e.src?a.createElement("img",{src:e.src,alt:e.alt}):a.createElement(a.Fragment,null),a.createElement("figcaption",{align:e.align?e.align:"center",style:{fontWeight:"bold"}},e.caption),a.createElement("figcaption",{align:e.align?e.align:"center",style:{}},e.subcaption))},dinosaur:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eAAAT3UlEQVR42u1dCVQVV5pWXNt2N0czykl33KImZ7IgKgqIghq3KCDK+qowCek2c2K0Mx3idBxakzYxJnZiq3Gf6Bg7UdN2R51MxnTSia3gew9Rwccm7oqiiIK4sPxTt1hEHo9XvPVW1fed852Dr+67UNb/1f3/+9/731atAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO8i2CxGjDUJXzMGmcSZnmoHAF7B6GMJvYPNwq5gk1AmMS/YJMbaahtkNsRLbeghmoU4d7cDAO+NCEbhQCMjrZbe5q81bhdyVOwuXbtqZdDSZ+yau9oBgNcgGeIvmzDQJkUy1ix8ZKMtsWvuagcAXsNYs/iyLSNlIgk2GebLQjKJQ6R/32+mbcWYI8KTrm6HJwR4170yCV80Y6T1I4kklH122lFNG9e2wxMC3Ao/U1KnQLPgF2SK/xeri5TiIxlikX1DBXVANpoXSy/DzGCjYfdYs2FRiFkcxWxEu/GF0RAm3fT1Bv8JJyV+LLlV08ccnNuFCQeGAdrheWkkXxaSGueruZFDurlrzfn4QSbDGRgAqJD3JK4NMcU8oo3RIz1hOB4q6AZeCzKK0aoXCIs58DBBt9Esfip5Ke3UPkN1Eg8TdB8N+5grr+JRxPAJHiLoTgaZhf97MiuqvVqTgNPxEEEPcK0qBTIyNa6rnWw1CLooJjHMUZc6KMWnNs9xDg8Q9ACLQtMMvbhfeFi7tuoLZMhBz1NczaUw2H4OFizhAYFe5l0uM+61m53wgMAWM+C7aBr425Ey2c8umPpdxmO+oxQPWz8cvnOmTGf7Gf1DDHXs25lYxMrIfmafOdnvOe4WONZsk4XhaD7nkJpAPQN96w2a/cw+c7S/QYsC6vuq46D/CHD+7zQaRvDmYsXVbG6CEWmZQ5YGWRk0+8zR/phb1bg/9pkLgvVk/twso+EViETbfPw1PyuDHrDQ36n4o6GL1eHRn7skDhlrEnZyuvbKMN/TIglKM9AzmyfLbzL2sBjZz89sniJfg2G7Nvbwad+m3qB9OrQh/z0RTschzK1yXZAu8zi/CxQ9NJL4fT6d+kwdQG27drB6q9WxXbcO1GfaAPL78wswcBfx6Y2T6ZHxv5DJfuY1acj5Kl55JHHPtOCBaOozZQC18mltUxhWlNoyobjwDQVyng/hVhyBaYbBrEKhW0aNL2Y85LO2lB37daHhX86AAemAPC4z6R5sEt9j6nWXONr8vJ3D4qhj287tIRIIxMP7PmrKd151p1vV3MjRtmt7eiT0F+QbN4z6xQ6T/eO2XdrbbP8z3y5wtyAQT+VAxAh336wcczQVhPfsKM+ANJWsYp+xRFS7Hh2b/C6LSWBIEIgnsuh73T1b1VRA3ql/dxq5d5bd74/4OlJu21TgjtktCMT9uwbdFJDXjx5TBzQ5cigRR71I/hZJ7bpbTwf3mT4QxgSBuHtbrSHcnUlAlstwxXqdgcmjmsyTIJkIgag2SGcZ8qYCckcWyAUdTpBnsBr398yWKTAoCESd07xD3rFeHMdmqxztj81uNe5v6B+CYVAQiAeD9qPiIOkP/NIVN9l//nArg/ZNeNLh/nzjn7Tqr//rw2FQEIg6M+lN7RcY/LvR3PQHupdh6S9R+LH5ZMh8i17NfoeS81bSO6fX0cfn/ps2X/wL7bzyv/TNtYP0z5KjdLw0hwrKL1DR/Rt0r+q+Plys0d/HyMtDGib4nNlx5ur+QPcZuLPQTSa9bjk0oyuM2dX9adm4Zx57jeIzk+lXliX0Ru4KSjm1hlac/S/69MKXtP3yXvrr1b/Td8WplHbzOGWV5dPZO5fo+v0Slxi4ZgTiiUw66BoD/32BPQO/zI2Ba0cgbs6kg9aMPfFbWn5mM/258H80a+CaEYi7M+ngA7JR4ERpHgFqEogbM+lgDSelv0LfFx+B1SNIBxtzWsarlH27ABavZoF4YsOUHhliEuX4AlCOwsJC2rVrF7+JwjHGuU8Em4X9MHDn+afzOzRtzGVlZbR69WqKjY2lqKgoev/996m4uNihvqqrqyklJYU6dKhf3Kq/Pel6izuKK246bYQXLlygvXv30ldffUWZmZlO9cX6CAwMpI4dO1Lbtm3pueeeo61btzrUV1ZWFj3++ONWKxseffRRMpvNLe7vzTffrClF5ONDEydOhIuldb53ZqNTxpyfn08RERFWBsiM2mQytbi/+fPn29zCnJSU1KK+ioqKyNe3poTpU089RRs3bqTt27dTQEBAvUiuXr2quL8ff/xRFgYT7e7duxGk64E/FBsdFsfhw4epR48eNTsvO3WioKAgmjRpEvXu3Vv+rHPnzvTTTz8p7u/dd9+tqXwouS/Lly+nS5cuUUlJCa1fv17ui11j7pFSTJs2Tf4O+7tu3bpV//ndu3fr3v40Y8YMRX1VVFTQkCFD5O8sW7YMmXS98MLdQofEYbFYqFu3brLBsBGEBa11KC0tpcTERPkaa8NGGXs4ePCg/HZu06YN7du3z+r6/v3769/e6enpdvvbs2dPTeHrnj1l968xLl68SN2712yR/vbbb+3299lnn8ltn3jiCbp37x4y6XphedWdFouDBbiDBw+WDWb27NlUWVlp1aaqqooiIyPlNsOHD3/IqBrj9u3bNGjQILnt4sWLbbZbuHCh3Mbf37/J31kH9rvq+mPBuS2w0Yi18fPzk4NvW2C/iwmDtd22bRsy6RAINWvM48aNq48z2L9tgblH/fv3l9suWLDAZrt58+bJbZ5++ulmhcRGpscee8yu4a9YsUJuM2zYMNk1soXy8nLq16+f3Hbnzp0227EJAtZm4MCBVv0hkw4XS8aNGzdkV4S9bZmxMMM6f/683e+lpaVR+/Y1W5A//PBDq+vr1q2Tr7E2GRkZil2nrl27Um5ubpOTBuwaa/PNN9/Y7a/u97MRgsUmjcE+Y8JgbbZs2YJMut6oZGnJ6NGjHz5bQzKYggLlWXf2BmbxA/suC+LZbNKOHTsoLi6OWrduLXPz5s2K+2P5DNYXC5rz8h6sGbt8+bI8qrFrrI3S4JuNNOw7ycnJVtfffvvtZkcjTPNqnMtOb7BrRGPGjJFnlpiRfPDBB826VbbABNGrVy/rii/t2tGqVata7OY9++yz8ve7dOkiC41NAdfNng0dOlR2x5TCaDTKfwf77tKlS2UhsJiEuXFs0oCJ+9ChQ+pYauKOPel65sT0JJckCpXmJVhgzLLZM2fOpEWLFj00ArR0oqCp/AuLj9hI0lIwkbKRrG7mqy42YVyyZIl61mJhqYnruercdtUuI2HTzZs2baK1a9fSkSPOrURm8U1droOxb9++tGHDBixWxGJFkVJLjmEFYoMcCYuxmpsBQ5Cuu+Xu8+hk2SmoQ63L3ZFJ90w8cuD6YVi9KgWCTLrHuDB3uVwep5qqoQC1CASZdM8z+sQb9P6ZTbSjcD+KNnAvEGTSUfYHAkGQDoGhcBymeUGUHkUmHdS6wG5VlmFPOgjq/gAdEMQRbCCoZYEgkw5CIMikgxAIMukgBIJMOgiBIEgHIRBM84KgegSCTDoIgSCTzvcWXbNAv7bE0/oL0fSPG1F0+k4k3aoMp4rqmUSkL8LFAus563gCbb88h4ruR+hOCKoQCIJ07/CFDAP9rWg23a+GILgVCDLp3uGSghi6WREOMXAvEGTSPcrxUpzxtTRqQAQqEQgCck9WNzFQasksCEBVAkEm3WMjB8SBIB20QbhVmOYFbXBpQazLDYjlR25XhetGIJOyXuw5JntuF2TSNVd61EAlLpytqpa4sjCWJmSLMtdcidG2QKhV67CcxHVh2WJVLVcik65zjmVZ9QyRxmcKFHpSJMkoaGqOSHGnDPTGuXj53w1pLIvSnECk+yoPzRZPh2Un/r3x/YZZEifBxdLrcpOMB6JQyt3Fc7QokOb4OoJ0vdEs0LgTLRNGHQ/cnE07JZEcLo2SXTCtC2RCdmJ8aI64MNSSOI25YMik64COiqMxPy6M0cMI0oDCGmTSdeBWuUIcYbWBe6kGZrdacM/VIafF7sikazggb2nMYU8gJZURehJIVUhO0iPIpGt29HCdOBj/qDMXS3ohfIogXctLUDJd516xaeCvb8yhMv24WGekQP2VsFNJ3TDNq1G60r2qY4IkFLWLpIX3fMojIkEm3QsV0LMFlwuEcfS/P0N+ft29ypdf/qWnBEJhFiEJmXQIRDH7RQ2uP5fcW+zbt6PHBDIhJ/EluFhwsRRxzsl4OmgeTyZTiFdZXDzVUwLJd6uLhSBdO0H63huzdRWkM9fKreJAJl07SULGjy7H6iuTbhHXI5Ou8URhGBKFHCcKEZB7fxQ5iqUm/C41QSadk8WKrhHJJ4X6crFCLeKfkEnXiavl7HL31LJZutgPUrfcPSxXmIoNU3rcMGURsGGKpw1TyKTzKZTxmWJtnkT6OSOBxhyYRX6fPW9lML0C+3k9KdgUR47s4dSWW4kF3Gy5RSbdtXTUMEaM6NG84bVuRUNSAiThSCNNlkCDk/25FAfjqFE9XVO0IVtcW1uwoTLMInyEsj86FohSllaGU7mOyv5MPR7bIyRrXmcUjoNAQFR3h0BAVHeHQEBUdwchEFR3ByEQVHdHkA6BQCCY5oVAIBBk0tUrEH//Htwm/jyZSedWIMikc55JVxFdkkmHiwWBgAjSIRAQmXQQAkEmHYRAkEkHeRDIP0ujaOG5eJqWK8j8jfQzOyQHAkEmXfcC2XA12uaOuk1F0RAIgnRtC4Qd4XyifBZZ7kRaHefMRg5722wbjySsD9YX61MLx0OH5cwNnJwX1xXTvDoTyF3JeD8pjKHncx4Y+xTp51VXYuRrrM3CJk6ybUx22u2D/mLlPuquTc4RavqrVv2e9LthOcKqgPNRP0MmXQcCqZAMdsFZ28b/unTNf1QvGpceZ1cg48xx5NPOh4Z/PsVmG79tz1Prtj5q3ZPekD/4mZLaIZOu9dpXx+1XKBl3XFlFk9BMAw1+a4Tddo8Zhqkyk95EQbz5cLG0Xsk9S3TLUQfN8ddnErRS9seMIF3rZ4FYPC+QF3IFrQjkFjLpOAvE5UwsMGhFIBZk0rV+FsgJweMC+Vilp95a34uwBpl0rdffNXtWIKzS+9Hbs2hlYSwZThnkqWA2onx+LZr7KeDGFdxDsw3jwnIS18mnSWWLd9iIEmpJfMvtU8DIpHtwBMny/Ahii/8mBe88JxRb8BJIc3tCEUG6Nt0re/zgcozqBVLrfm3GNK+aC1Ef408cjBM5Po2qhfdS6dZTppBJd2/cEWoRuRQIY8/RfdWQSbfP3LlhSoPuxSGpcb7IpMO1UsIe/n1UkUm3OxrmCsF2jTs09aU+0kO5zQwcLhYHTBe5Fgdb1HirMlwLLtbdSVkv9lSS01ha93CCzMpP4UGQzve5g+7iHzk+z7CF97JWadIvr8EDqmJZcmTSvUSzd5aWKOX8swn1y+tVLpCD001JnezHHkdE/yYe1B17IkEm3U3BeTq/o8faK9Hy0nvVn3JrET5SvAxeeii/sfGwqqSY5DVk0j3sXh3jd/Rgm7V43+Ou8F7uSyyT+P1EizjdnkC+sDPk7x+TPrcvMukemr3K5DtA532PuyP3EZojvtvc9G6mggd3LcgoLAg49PD6FQTp7li5K6hGIE3tcVejQGSRWBKn2RpBLrXgAbK2vws0zu2PaV7t7P1whnV73NUuEHZstC2B3HFwtuVIkEn8cKxRiJFGkn8NyZgbGGw07IaROzmCZKtLIGyPu6oz6fY2VkkP5R4MEwJxlCGmOG4y6ferw525l5u2BHIdhsmRQOBiOUy2gNLhGCRb/M6ZIB3U8PZaZ5haNosbgRTcjXT8XnKFqbZGkK9gmDxtjlKPOLZwNs37j1uzHbwXYWlzOwMXwTCRKFSaKJyeK8huFU8jh5K6xNaJQqGUuVU2R476aVqzOAqGiaUmSnjmXiTXy0xePZOgLN7ISxymfL06pfhID+YcjJMTgXAah7xymu9CclfuR8jFJhTcy1EHSvgYlsE41VVq1NPccX0O1wJhFVcU3UuOmNzyfeWpcb7Ih/C1YYqnfAirsnijkt8l7iz/EZ1vUJQMnJif0NvRQnBrYZw8bZriRyDbrvE9euwpnqOs1E+OsNjhogsBh17sKT2YIhgnLxunRC7WZc3OF6ic4w1SN6WRLTJP0ehxOSRrXmfn6lwZxWgYJ8r+NKywmMbhdG5DLrkYp+ReqsbnGCa7qij1pzBOVDdh3HqN7zMN/3pjttLA/D9dVt8q6suoNmNNwl9gnPreRPV76c1czbE4WKJyUo6il8euFErxcWkROD9TUqdgk2EfjJOf3IgnRfLepViqrOY37mCbtKbmKhLH1pDvU9q6pVIi29SOmS19zWxNqC3MUM25W6Vg5KhmhRlaUavWHjgoxzAHs1scBe4ZclUOl4sjJt9AxrIoboVRUhmuNCA/F2ZJnOTRs0BC0wy9gk3iamyr5ad2lquCd1alZM2VGG6PNGBJQJbnCM+ze7+sSslKr56RPj7D0K92WQrWbnEiFLYsxZG1W2zEYMszeC0herUiQv77FGTIz7EDcRSVEPUYKMUnyGgYIY0qyVIAuVN6WMdrdyZiuYqXgvixRwX5KOjxmTWLHdnORLZchfnrEdLb9+XTCZKLEiv78GfvRXA0QsykmxXhlF8eST8UR9G6i9H0q7x4Cm10H2HZQoUkhmsSj0/IFnZOyBFeDctNGNoKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsI3/BxVeQNnL1kBuAAAAAElFTkSuQmCC"}}}]);