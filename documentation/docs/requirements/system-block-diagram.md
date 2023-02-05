---
sidebar_position: 2
---

# System Block Diagram
```mermaid
 %%{init: { 'theme':'dark', "themeCSS": ".label foreignObject { overflow: visible; }" } }%%
---
title: System Block Diagram
---
flowchart TB
    A[<img src='https://cdn-icons-png.flaticon.com/512/1995/1995574.png'>Educator]
    B[<img src='https://cdn-icons-png.flaticon.com/512/5850/5850276.png'>Student]
    C[<img src='https://cdn-icons-png.flaticon.com/512/6032/6032273.png'>Assistant]
    D[<img src='https://www.svgrepo.com/show/353655/discord-icon.svg'>Discord]
    E[<img src='https://cdn.discordapp.com/attachments/494945996892012544/1071574051623030834/Discord_Classroom.jpg'>Classroom Bot]
    F[<img src='https://s3-eu-west-1.amazonaws.com/tpd/logos/5dc1fb0c303176000104b2d4/0x0.png'>SparkedHost]
    G[<img src='https://static-00.iconduck.com/assets.00/office-database-icon-491x512-nll0enk8.png'>SH Database]
    H[<img src='https://pbs.twimg.com/profile_images/1414990564408262661/r6YemvF9_400x400.jpg'>GitHub]
    A<--->D
    B<--->|User enters commands through Discord UI and receive response|D
    C<--->D
    D<-->|Classroom Bot receive commands through Discord and responds|E
    E<-->|Discord.py library used to host bot on SparkedHost|F
    F<-->|Server POST/GET data from its DB|G
    H-- SparkedHost pulls code from GitHub -->F
```
