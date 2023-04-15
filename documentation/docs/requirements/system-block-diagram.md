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
    D[Discord]
    E[Classroom Bot]
    F[Google Compute Engine]
    G[Supabase]
    H[GitHub]
    I[main.py]
    J[FastAPI]
    A<-->D
    B<-->|User enters commands through Discord UI and receive response|D
    C<-->D
    D<-->|Classroom Bot receive commands through Discord and responds|E
    E<-->F
    subgraph ide1 [Application]
    H-->|Compute Engine pulls from Main branch|F
    H-->I
    J<-->G
    I<-->J
    end
```

The System Block Diagram involves two sections, the application side and the UI side. First, Discord is used as the user interface in order to interact with the application. Each user has a role which decides what commands they have access to, the roles being Educator, Assistant, and Student. When a command is typed the message is read by the bot and anaylzed by the bot. The bot then sends an appropriate response. The application is hosted on Google Computer Engine which pulls the code directly from GitHub repo's main branch. Within GitHub is the main.py file which is ran on the server. main.py also connects to FastAPI which uses Supabase's API to connect to the database.
