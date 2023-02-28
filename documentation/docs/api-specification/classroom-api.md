---
title: API - Classroom Bot
description: API Specification from fastapi
sidebar_position: 1
---

ClassroomBotAPI (0.0.1) : http://35.237.162.33:2556/redoc
=======================

Download OpenAPI specification:[Download](http://127.0.0.1:8000/openapi.json)

[](#operation/get_classrooms_classrooms_get)Get Classrooms
----------------------------------------------------------

### Responses

**200**

Successful Response

get/classrooms

http://127.0.0.1:8000/classrooms

### Response samples

*   200

Content type

application/json

Copy

`{  *   "id": 0,      *   "serverId": "string",      *   "serverName": "string"       }`

[](#operation/get_classroom_id_classroomId_get)Get Classroom Id
---------------------------------------------------------------

##### query Parameters

serverId

integer (Serverid)

Default: 0

### Responses

**200**

Successful Response

**404**

Not Found

**422**

Validation Error

get/classroomId

http://127.0.0.1:8000/classroomId

### Response samples

*   200
*   404
*   422

Content type

application/json

Copy

`{  *   "id": 0       }`

[](#operation/get_educators_educators__get)Get Educators
--------------------------------------------------------

##### query Parameters

classroomId

integer (Classroomid)

Default: 0

### Responses

**200**

Successful Response

**404**

Not Found

**422**

Validation Error

get/educators/

http://127.0.0.1:8000/educators/

### Response samples

*   200
*   404
*   422

Content type

application/json

Copy

Expand all Collapse all

`[  *   {          *   "id": 0,              *   "name": "string",              *   "sectionId": 0                   }       ]`

[](#operation/get_students_students__get)Get Students
-----------------------------------------------------

##### query Parameters

classroomId

integer (Classroomid)

Default: 0

### Responses

**200**

Successful Response

**404**

Not Found

**422**

Validation Error

get/students/

http://127.0.0.1:8000/students/

### Response samples

*   200
*   404
*   422

Content type

application/json

Copy

Expand all Collapse all

`[  *   {          *   "id": 0,              *   "sectionId": 0,              *   "name": "string",              *   "attendance": 0                   }       ]`

[](#operation/get_sections_sections__get)Get Sections
-----------------------------------------------------

##### query Parameters

classroomId

integer (Classroomid)

Default: 0

### Responses

**200**

Successful Response

**404**

Not Found

**422**

Validation Error

get/sections/

http://127.0.0.1:8000/sections/

### Response samples

*   200
*   404
*   422

Content type

application/json

Copy

Expand all Collapse all

`[  *   {          *   "id": 0,              *   "name": "string",              *   "classroomId": 0,              *   "totalAttendance": 0,              *   "totalGrade": 0                   }       ]`

[](#operation/get_grades_grades__get)Get Grades
-----------------------------------------------

##### query Parameters

studentId

integer (Studentid)

Default: 0

### Responses

**200**

Successful Response

**404**

Not Found

**422**

Validation Error

get/grades/

http://127.0.0.1:8000/grades/

### Response samples

*   200
*   404
*   422

Content type

application/json

Copy

Expand all Collapse all

`[  *   {          *   "type": "string",              *   "name": "string",              *   "score": 0,              *   "maxScore": 0                   }       ]`