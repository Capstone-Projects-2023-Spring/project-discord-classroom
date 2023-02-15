---
sidebar_position: 1
---

**Purpose**

The Design Document - Part I Architecture describes the software architecture and how the requirements are mapped into the design. This document will be a combination of diagrams and text that describes what the diagrams are showing.

**Requirements**

In addition to the general requirements the Design Document - Part I Architecture will contain:

A description the different components and their interfaces. For example: client, server, database.

For each component provide class diagrams showing the classes to be developed (or used) and their relationship.

Sequence diagrams showing the data flow for _all_ use cases. One sequence diagram corresponds to one use case and different use cases should have different corresponding sequence diagrams.

Describe algorithms employed in your project, e.g. neural network paradigm, training and training data set, etc.

If there is a database:

Entity-relation diagram.

Table design.

A check list for architecture design is attached here [architecture\_design\_checklist.pdf](https://templeu.instructure.com/courses/106563/files/16928870/download?wrap=1 "architecture_design_checklist.pdf")  and should be used as a guidance.

## Database Design

```mermaid
---
title: Database Design
---
erDiagram
    CLASSROOM {
        int id
        string name
        int totalAttendance
        int totalGrade
    }
    EDUCATOR {
        int id
        string name
        int classroom_id
    }
    STUDENT {
        int id
        string name
        int classroom_id
        int grade
        int attendance
    }
    ASSIGNMENT {
        int id
        int classroom_id
        string name
        int maxScore
        dateFormat startDate
        dateFormat dueDate
        string instructions
    }
    QUIZ {
        int id
        int classroom_id
        string name
        int maxScore
        dateFormat startDate
        dateFormat dueDate
        int timeLimit
    }
    QUESTION {
        int id
        int quiz_id
        string prompt
        string answer
        string wrong1
        string wrong2
        string wrong3
    }
    DISCUSSION {
       int id
       int name
       int maxScore
       dateFormat startDate
       dateFormat dueDate 
    }
    GRADED-ASSIGNMENT {
        int id
        int assignment_id
        int student_id
        int maxScore
        int score
    }
    GRADED-QUIZ {
        int id
        int quiz_id
        int student_id
        int maxScore
        int score
    }
    GRADED-DISCUSSION {
        int id
        int discussion_id
        int student_id
        int maxScore
        int score
    }
    CLASSROOM }|--|{ EDUCATOR : contains
    CLASSROOM }|--|{ STUDENT : contains
    CLASSROOM ||--o{ ASSIGNMENT : has
    CLASSROOM ||--o{ QUIZ : has
    CLASSROOM ||--o{ DISCUSSION : has
    QUIZ ||--|{ QUESTION : contains
    STUDENT }|--o{ GRADED-ASSIGNMENT : has
    STUDENT }|--o{ GRADED-QUIZ : has
    STUDENT }|--o{ GRADED-DISCUSSION : has   
```
