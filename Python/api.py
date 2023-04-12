<<<<<<< HEAD
from create_classes import Assignment, Discussion, Grade, Question, Quiz
=======
from sqlite3 import Timestamp
>>>>>>> main
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from storage3.utils import StorageException
import supabase as sb
from supabase import create_client
from typing import List, Optional

import asyncio
import datetime
import hashlib
import json
import os
import pickle
import requests
from pathlib import Path



#
# Setup
#

app = FastAPI(
    title="ClassroomBotAPI",
    version="0.0.1"
)


def get_config_path():
    module_path = Path(__file__).resolve().parent
    config_path = module_path / "config.json"
    return str(config_path)


def check_config_exists():
    config_path = get_config_path()
    return os.path.exists(config_path)


path = get_config_path()

if check_config_exists():
    with open(path, 'r') as f:
        configData = json.load(f)
else:
    raise FileNotFoundError(f"Configuration file '{path}' not found. Please ensure it exists.")

# Create a Supabase client instance
supabase = create_client(
    configData["SupaUrl"],
    configData["SupaKey"]
)


<<<<<<< HEAD

#
# Models
#

class Assignment(BaseModel):
    id: Optional[int] = None
    channelId: int
    points: int
    startDate: datetime.date
    dueDate: datetime.date
    classroomId: int
    title: str

=======
# classes
>>>>>>> main
class Classroom(BaseModel):
    id: Optional[int] = None
    attendance: int
    serverId: int
    serverName: str

<<<<<<< HEAD
class Classroom_User(BaseModel):
=======

class ClassroomId(BaseModel):
    id: int


class Educator(BaseModel):
    id: int
    name: str
    sectionId: int


class Student(BaseModel):
    id: int
    sectionId: int
    name: str
    attendance: int


class Section(BaseModel):
    id: int
    name: str
>>>>>>> main
    classroomId: int
    role: str
    userId: int
    attendance: Optional[int] = None

class Discussion(BaseModel):
    classroomId: int
    channelId: int
    title: str
    points: int
    startDate: datetime.date
    dueDate: datetime.date

class Grade(BaseModel):
    taskType: str
    graderId: int
    taskId: int
    studentId: int
    score: int

class Question(BaseModel):
    question: str
    answer: str
    wrong: List[str]
    points: float

class Quiz(BaseModel):
    questions: str
    channelId: int
    title: str
    points: float
    startDate: datetime.date
    dueDate: datetime.date
    timeLimit: int
    classroomId: int

class User(BaseModel):
    id: Optional[int] = None
    name: str
    discordId: int


<<<<<<< HEAD

#
# API Endpoints
#

# 
# /assignment
# 

@app.post("/assignment")
async def create_assignment(assignment: Assignment):
    response = supabase.table('Assignment').insert(dict(assignment)).execute()
    return JSONResponse(content={'message': 'assignment created'}) 
=======
class Message(BaseModel):
    message: str

class Tokens(BaseModel):
    userId: int
    unique_id: str
>>>>>>> main

@app.get("/assignment", response_model=Assignment)
async def get_assignment(channel_id:int):
    sb_response = supabase.table("Assignment").select('*').eq('channelId', channel_id).execute()
    assignment = Assignment.parse_obj(sb_response.data[0])
    return assignment

@app.put("/assignment/")
async def update_assignment(assignment: Assignment, channel_id: int):
    supabase.table("Assignment").update(dict(assignment)).eq('channelId', channel_id).execute()
    return JSONResponse(content={'message': 'assignment updated'}) 

# 
# /classroom
# 

<<<<<<< HEAD
@app.post("/classroom")
async def create_classroom(classroom: Classroom):
    sb_response = supabase.table('Classroom').insert(dict(classroom)).execute()
    return JSONResponse(content={'message': 'quiz created'}) 
    
@app.get("/classroom", response_model=List[Classroom])
async def get_all_classrooms():
    sb_response = supabase.table('Classroom').select('*').execute()
    classroom = sb_response.data
    return classroom

@app.delete("/classroom/")
async def delete_classroom(server_id: int):
    sb_resposne = supabase.table('Classroom').delete().eq('serverId', server_id).execute()
    return JSONResponse({'message': 'classroom deleted'})

@app.get("/classroom/{server_id}", response_model=Classroom)
async def get_classroom(server_id: int):
    sb_response = supabase.table('Classroom').select('*').eq('serverId', server_id).execute()
    classroom = Classroom.parse_obj(sb_response.data[0])
    return classroom

@app.get("/classroom/{server_id}/attendance")
=======

@app.get("/classroomAttendance")
>>>>>>> main
async def get_classroom_attendance(server_id: int):
    classroom = await get_classroom(server_id)
    return JSONResponse(content={'attendance': classroom.attendance})

# 
# /classroom_user
# 

@app.post("/classroom_user")
async def create_classroom_user(classroom_user: Classroom_User):
    sb_response = supabase.table('Classroom_User').insert(dict(classroom_user)).execute()
    return JSONResponse(content={'message': 'classroom user created'}) 

<<<<<<< HEAD
@app.get("/classroom_user/{classroom_id}/student", response_model=List[Classroom_User])
async def get_students(classroom_id: int):
    sb_response = supabase.table('Classroom_User').select('*').match({'classroomId': classroom_id, 'role': "Student"}).execute()
    student = sb_response.data
    return student

@app.get("/classroom_user/{classroom_id}/educator", response_model=List[Classroom_User])
async def get_educators(classroom_id: int):
    sb_response = supabase.table('Classroom_User').select('*').match({'classroomId': classroom_id, 'role': "Educator"}).execute()
    educator = sb_response.data
    return educator
=======

@app.get("/userAttendance")
async def get_user_attendance(user_id: int, classroom_id: int):
    response = supabase.table('Classroom_User').select('attendance').match(
        {'classroomId': classroom_id, 'userId': user_id}).execute()
    if response.data:
        return {'attendance': response.data[0]['attendance']}
    return JSONResponse(status_code=404, content={"message": "User not found"})


@app.put("/userAttendance")
async def update_user_attendance(old_attendance: int, user_id: int, classroom_id: int):
    response = supabase.table('Classroom_User').update({'attendance': old_attendance + 1}).match(
        {'classroomId': classroom_id, 'userId': user_id}).execute()
>>>>>>> main

@app.get("/classroom_user/{user_id}/{classroom_id}/attendance")
async def get_classroom_user_attendance(user_id: int, classroom_id: int):
    sb_response = supabase.table('Classroom_User').match({'classroomId': classroom_id, 'userId': user_id}).execute()
    classroom_user = sb_response.data
    return JSONResponse(content={'attendance': classroom_user.attendance})

@app.put("/classroom_user/{user_id}/{classroom_id}/attendance")
async def update_user_attendance(user_id: int, classroom_id: int):
    response = await get_classroom_user_attendance
    attendance = response['attendance']
    sb_response = supabase.table('Classroom_User').update({'attendance': attendance+1}).match({'classroomId': classroom_id, 'userId': user_id}).execute()
    return JSONResponse(content={'message': 'attendance updated'})

<<<<<<< HEAD
@app.put("/classroom_user/{user_id}/{classroom_id}/role")
async def update_classroom_user_role(user_id: int, classroom_id: int, role: str):
    if role == 'Student':
        attendance = 0
=======

@app.get("/students/", response_model=List[Student], responses={404: {"model": Message}})
async def get_students(classroom_id: int = 0):
    if classroom_id == 0:
        return JSONResponse(status_code=404, content={"message": "ClassroomId not given"})
    response = supabase.table('Classroom_User').select('*').match(
        {'role': "Student", 'classroomId': classroom_id}).execute()
    student_ids = []
    data = response.data
    for d in data:
        student_ids.append(d['userId'])
    students = []
    for id in student_ids:
        stu = supabase.table('User').select('*').eq('id', id).execute()
        if stu.data:
            students.append(stu.data[0])
    if students:
        return students
    return JSONResponse(status_code=404, content={"message": "Classroom not found"})


@app.get("/grades/", response_model=List[Grade], responses={404: {"model": Message}})
async def get_grades(student_id: int = 0):
    r = supabase.table('Grade').select('score', 'taskId').eq('studentId', student_id).execute()
    data = r.data
    all = []
    for info in data:
        taskId = info['taskId']
        r1 = supabase.table('Classroom_Task').select('id', 'taskType', 'taskTypeId').eq('id', taskId).execute()
        r2 = supabase.table(r1.data[0]['taskType']).select('*').eq('id', r1.data[0]['taskTypeId']).execute()

        combined = {'type': r1.data[0]['taskType'], 'title': r2.data[0]['title'], 'score': info['score'],
                    'points': r2.data[0]['points']}
        all.append(combined)

    return all


@app.get("/quiz/")
async def get_quiz(channel_id: int = 0):
    if channel_id == 0:
        return JSONResponse(status_code=404, content={"message": "Channel ID not given"})
    response = supabase.table("Quiz").select('*').eq('channelId', channel_id).execute()
    return {'quiz': response.data[0]}


@app.get("/questions/")
async def get_question(quiz_id: int = 0):
    if quiz_id == 0:
        return JSONResponse(status_code=404, content={"message": "Quiz ID not given"})
    response = supabase.table("Quiz").select('questions').eq('id', quiz_id).execute()
    url = response.data[0]['questions']
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
>>>>>>> main
    else:
        attendance = None
    sb_response = supabase.table('Classroom_User').update({'role': role, 'attendance': attendance}).eq('userId', user_id).eq('classroomId', classroom_id).execute()
    return {'message': 'role updated'}

<<<<<<< HEAD

# 
# /discussion
# 

@app.post("/discussion")
async def create_discussion(discussion: Discussion):
    sb_response = supabase.table('Discussion').insert(dict(discussion)).execute()
    return JSONResponse(content={'message': 'discussion created'}) 

# 
# /grade
# 
=======

@app.get("/Assignment/")
async def get_assignment(channel_id: int = 0):
    if channel_id == 0:
        return JSONResponse(status_code=404, content={"message": "Channel ID not given"})
    response = supabase.table("Assignment").select('*').eq('channelId', channel_id).execute()
    return {'Assignment': response.data[0]}


@app.put("/Assignment_Update/")
async def update_assignment(dictionary: dict, channel_id: int):
    supabase.table("Assignment").update(dictionary).eq('channelId', channel_id).execute()


@app.put("/Quiz_Update/")
async def update_quiz(dictionary: dict, channel_id: int):
    supabase.table("Quiz").update(dictionary).eq('channelId', channel_id).execute()


# ---------------------------POST Methods-------------------------------
>>>>>>> main

@app.post("/grade")
async def create_grade(grade: Grade):
    sb_response = supabase.table('Grade').insert(dict(grade)).execute()
    return JSONResponse(content={'message': 'grade created'}) 

@app.get("/grade/{student_id}", response_model=List[Grade])
async def get_grades(student_id):
    sb_response = supabase.table('Grade').select('score', 'taskId').eq('studentId', student_id).execute()
    grades = sb_response.data
    return grades

@app.put("grade/")
async def update_grade(grade: Grade):
    sb_response = supabase.table("Grade").insert(dict(grade)).execute()
    return JSONResponse({"message": "grade updated"})

# 
# /quiz
#  

@app.post("/quiz")
async def create_quiz(quiz: Quiz):
<<<<<<< HEAD
    response = supabase.table('Quiz').insert(dict(quiz)).execute()
    return JSONResponse(content={'message': 'quiz created'})    
=======
    list = {'title': quiz.title, 'points': quiz.points, 'startDate': quiz.start, 'dueDate': quiz.due,
            'timeLimit': quiz.time,
            'channelId': quiz.channelId, 'classroomId': quiz.classroomId, 'questions': quiz.questions}
    res = supabase.table("Quiz").insert(list).execute()
>>>>>>> main

@app.put("/quiz/")
async def update_quiz(quiz: Quiz, channel_id: int):
    supabase.table("Quiz").update(dict(quiz)).eq('channelId', channel_id).execute()
    return JSONResponse(content={'message': 'quiz updated'})    

<<<<<<< HEAD
@app.get("/quiz/{quiz_id}/questions/")
async def get_questions(quiz_id: int):
    response = supabase.table("Quiz").select('questions').eq('id', quiz_id).execute()
    return JSONResponse(content=response.data[0])

@app.post("/quiz/questions/")
=======

@app.post("/questions/")
>>>>>>> main
async def create_questions(questions: List[Question]):
    ques_list = []
    for question in questions:
        ques_list.append(dict(question))

    bytes_obj = pickle.dumps(ques_list)
    hash_object = hashlib.sha256(bytes_obj)
    hex_dig = hash_object.hexdigest()

    with open(f"{hex_dig}.json", "w") as outfile:
        json.dump(ques_list, outfile)

    outfile.close()

    with open(f'{hex_dig}.json', 'r') as f:
        data = json.load(f)

    f.close()

    json_string: str = json.dumps(data)

    public_url = supabase.storage().from_('questions').get_public_url(f"{hex_dig}.json")

    # Verify URL created
    response = requests.get(public_url)
    if response.status_code == 400:
        res = supabase.storage().from_('questions').upload(f"{hex_dig}.json", json_string.encode())
        public_url = supabase.storage().from_('questions').get_public_url(f"{hex_dig}.json")
        os.remove(f'{hex_dig}.json')

<<<<<<< HEAD
    return JSONResponse(content={'url': public_url})
=======
    return public_url


@app.delete("/classroom/")
async def remove_classroom(id: int):
    supabase.table('Classroom').delete().eq('serverId', id).execute()
    return {'message': 'Classroom deleted'}


@app.post("/classroom/")
async def create_classroom(id: int, name: str):
    list = {'serverId': id, 'serverName': name}
    try:
        supabase.table('Classroom').insert(list).execute()

    except sb.PostgrestAPIError as e:
        return {'message': 'Classroom already exists'}

    return {'message': 'Classroom created'}


@app.post("/educator/")
async def create_educator(id: str, name: str, server: str):
    response = supabase.table("Classroom").select('id').eq("serverId", server).execute()
    classroom_id = response.data[0]['id']
    list = {'discordId': id, 'name': name}
    response = supabase.table('User').insert(list).execute()
    user_id = response.data[0]['id']
    list = {'classroomId': classroom_id, 'userId': user_id, 'role': "Educator"}
    supabase.table('Classroom_User').insert(list).execute()
    return {'message': 'Educator created'}


@app.post("/student/")
async def create_student(id: str, name: str, server: str):
    response = supabase.table("Classroom").select('id').eq("serverId", server).execute()
    classroom_id = response.data[0]['id']
    list = {'discordId': id, 'name': name, 'attendance': 0}
    response = supabase.table('User').insert(list).execute()
    user_id = response.data[0]['id']
    list = {'classroomId': classroom_id, 'userId': user_id, 'role': "Student"}
    supabase.table('Classroom_User').insert(list).execute()
    return {'message': 'Educator created'}


@app.post("/Assignments/")
async def create_assignment(assignment: Assignment):
    list = {'title': assignment.title, 'points': assignment.points, 'startDate': assignment.start,
            'dueDate': assignment.due,
            'channelId': assignment.channelId, 'classroomId': assignment.classroomId}

    res = supabase.table("Assignment").insert(list).execute()

    return {"message": "assignment created successfully"}


@app.post("/Discussions/")
async def create_discussion(discussion: Discussion):
    list = {'title': discussion.title, 'points': discussion.points, 'startDate': discussion.start,
            'dueDate': discussion.due,
            'channelId': discussion.channelId, 'classroomId': discussion.classroomId}

    res = supabase.table("Discussion").insert(list).execute()

    return {"message": "assignment created successfully"}


@app.post("/Grade/")
async def update_grade(grade: Grade):
    list = {'graderId': grade.graderId, 'taskId': grade.taskId, 'studentId': grade.studentId, 'score': grade.score}

    res = supabase.table("Grade").insert(list).execute()

    return {"message": "grade updated successfully"}

@app.post("/Tokens/")
async def update_token(tokens: Tokens):

    list = {'created_at': 'now()', 'userId': tokens.userId, 'unique_id': tokens.unique_id}
    res = supabase.table("Tokens").insert(list).execute()

    return {"message": "upload is avaiable for 10 minutes"}


# --------------------------- PUT Methods-------------------------------
>>>>>>> main

# 
# /user
# 

<<<<<<< HEAD
@app.post("/user")
async def create_user(user: User):
    sb_response = supabase.table('User').insert(dict(user)).execute()
    return JSONResponse(content={'message': 'user created'})

@app.get("/user/{discord_id}", response_model=User)
async def get_user(discord_id: int):
    sb_response = supabase.table('User').select('*').eq('discordId', discord_id).execute()
    if sb_response.data == []:
        return JSONResponse(content={'message': 'user not found'})
=======
@app.put("/user")
async def create_user(nick: str, discord_id: int):
    response = supabase.table('User').insert({'discordId': discord_id, 'name': nick}).execute()
    return {'message': 'User created', 'id': response.data[0]['id']}


@app.get("/user/id")
async def get_user_id(discord_id: int):
    response = supabase.table('User').select('id').eq('discordId', discord_id).execute()
    if response.data:
        return response.data[0]
>>>>>>> main
    else:
        user = User.parse_obj(sb_response.data[0])
        return user

@app.get("/user/{discord_id}/id")
async def get_user_id(discord_id: int, response_model=User, response_model_include={'id'}):
    sb_response = supabase.table('User').select('*').eq('discordId', discord_id).execute()
    if sb_response.data == []:
        return JSONResponse(content={'message': 'user not found'})
    return JSONResponse(content={'id': user.id})

@app.put("/user/{discord_id}/nick")
async def update_user_name(discord_id: int, name: str):
    sb_response = supabase.table('User').update({'name': name}).eq('discordId', discord_id).execute()
    return JSONResponse(content={'message': 'nickname updated'})


<<<<<<< HEAD


=======

@app.put("/user/nick")
async def update_user_nick(nick: str, discord_id: int):
    response = supabase.table('User').update({'name': nick}).eq('discordId', discord_id).execute()
    return {'message': 'Nickname updated'}


@app.put("/member")
async def update_member_role(role: str, id: int, classroom_id: int):
    if role == "Student":
        response = supabase.table('Classroom_User').update({'role': role, 'attendance': 0}).match(
            {'userId': id, 'classroomId': classroom_id}).execute()
    else:
        response = supabase.table('Classroom_User').update({'role': role, 'attendance': None}).match(
            {'userId': id, 'classroomId': classroom_id}).execute()


# /classroom_user

@app.post('/classroom_user')
async def create_classroom_user(classroom_id: int, user_id: int, name: str, role: str):
    if role == 'Student':
        attendance = 0
    else:
        attendance = None
    supabase.table("Classroom_User").insert(
        {"classroomId": classroom_id, 'userId': user_id, 'role': role, 'attendance': attendance}).execute()
    return {'message': 'Classroom user created'}


@app.put("/classroom_user")
async def update_classroom_user_role(role: str, user_id: int, classroom_id: int):
    if role == 'Student':
        attendance = 0
    else:
        attendance = None
    response = supabase.table('Classroom_User').update({'role': role, 'attendance': attendance}).eq('userId',
                                                                                                    user_id).eq(
        'classroomId', classroom_id).execute()
    return {'message': 'Role updated'}
>>>>>>> main
