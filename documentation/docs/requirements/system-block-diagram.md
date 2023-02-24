---
sidebar_position: 2
---

# System Block Diagram
```mermaid
---
title: System Block Diagram
---
flowchart TB
    A[User: Educator]
    B[User: Student]
    C[User: Assistant]
    D[<img src='https://www.svgrepo.com/show/353655/discord-icon.svg'>Discord]
    E[<img src='https://cdn.discordapp.com/attachments/494945996892012544/1071574051623030834/Discord_Classroom.jpg'>Classroom Bot]
    F[<img src='https://s3-eu-west-1.amazonaws.com/tpd/logos/5dc1fb0c303176000104b2d4/0x0.png'>SparkedHost]
    G[<img src='https://seeklogo.com/images/S/supabase-logo-DCC676FFE2-seeklogo.com.png'>Supabase DB]
    H[<img src='https://pbs.twimg.com/profile_images/1414990564408262661/r6YemvF9_400x400.jpg'>GitHub]
    I[<img src='https://cdn3.iconfinder.com/data/icons/logos-and-brands-adobe/512/267_Python-512.png' > main.py]
    A<--->D
    B<--->|User enters commands through Discord UI and receive response|D
    C<--->D
    D<-->|Classroom Bot receive commands through Discord and responds|E
    E<-->F
    subgraph ide1 [Application]
    I<-->G
    H-- SparkedHost pulls code from GitHub -->F
    H---I
    end
```

The System Block Diagram involves two sections, the application side and the UI side. First, Discord is used as the user interface in order to interact with the application. Each user has a role which decides what commands they have access to, the roles being Educator, Assistant, and Student. When a command is typed the message is read by the bot and anaylzed by the bot. The bot then sends an appropriate response. The application is hosted on SparkedHost which pulls the code directly from GitHub repo's main branch. Within GitHub is the main.py file which is ran on the server. main.py also connects to a Supabase Database through a library.
