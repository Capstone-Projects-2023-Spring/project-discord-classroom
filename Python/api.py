from create_classes import Assignment, Discussion, Grade, Question, Quiz
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from storage3.utils import StorageException
from supabase import create_client
from typing import List, Optional

import asyncio
import datetime
import hashlib
import json
import os
import pickle
import requests

app = FastAPI(
    title="ClassroomBotAPI",
    version="0.0.1"
)

if os.path.exists(os.getcwd() + "/config.json"):
    with open("config.json") as f:
        configData = json.load(f)
else:
    print("ERROR: config.json does not exist")
    exit

# Create a Supabase client instance
supabase = create_client(
    configData["SupaUrl"],
    configData["SupaKey"]
)

# Base Models

class Assignment(BaseModel):
    id: Optional[int] = None
    channelId: int
    points: int
    startDate: datetime.date
    dueDate: datetime.date
    classroomId: int
    title: str

class Classroom(BaseModel):
    id: Optional[int] = None
    attendance: int
    serverId: int
    serverName: str

class Classroom_User(BaseModel):
    classroomId: int
    role: str
    userId: int
    attendance: int # TODO: 0 for student, None for educator

class Discussion(BaseModel):
    classroomId: int
    channelId: int
    title: str # TODO: Why varchar as opposed to text?
    points: int
    startDate: datetime.date
    dueDate: datetime.date

class Grade(BaseModel):
    taskType: str
    graderId: int
    taskId: int
    studentId: int
    score: int

class Quiz(BaseModel):
    questions: str
    channelId: int
    title: str
    points: float # TODO: should this be float or int?
    startDate: datetime.date
    dueDate: datetime.date
    timeLimit: int
    classroomId: int

class User(BaseModel):
    id: Optional[int] = None
    name: str
    discordId: int

# TODO: verify db response, error message if can't connect to db or data not found

# ===========
# /assignment
# ===========

@app.post("/assignment")
async def create_assignment(assignment: Assignment):
    response = supabase.table('Assignment').insert(dict(assignment)).execute()
    return JSONResponse(content={'message': 'assignment created'}) 

@app.get("/assignment", response_model=Assignment)
async def get_assignment(channel_id:int):
    sb_response = supabase.table("Assignment").select('*').eq('channelId', channel_id).execute()
    assignment = Assignment.parse_obj(sb_response.data[0])
    return assignment

# ==========
# /classroom
# ==========

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
async def get_classroom_attendance(server_id: int):
    classroom = await get_classroom(server_id)
    return JSONResponse(content={'attendance': classroom.attendance})

# ===============
# /classroom_user
# ===============

@app.post("/classroom_user")
async def create_classroom_user(classroom_user: Classroom_User):
    sb_response = supabase.table('Classroom_User').insert(dict(classroom_user)).execute()
    return JSONResponse(content={'message': 'classroom user created'}) 

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

@app.put("/classroom_user/{user_id}/{classroom_id}/role")
async def update_classroom_user_role(user_id: int, classroom_id: int, role: str):
    if role == 'Student':
        attendance = 0
    else:
        attendance = None
    sb_response = supabase.table('Classroom_User').update({'role': role, 'attendance': attendance}).eq('userId', user_id).eq('classroomId', classroom_id).execute()
    return {'message': 'role updated'}


# ===========
# /discussion
# ===========

@app.post("/discussion")
async def create_discussion(discussion: Discussion):
    sb_response = supabase.table('Discussion').insert(dict(discussion)).execute()
    return JSONResponse(content={'message': 'discussion created'}) 

# ======
# /grade
# ======

@app.post("/grade")
async def create_grade(grade: Grade):
    sb_response = supabase.table('Grade').insert(dict(grade)).execute()
    return JSONResponse(content={'message': 'grade created'}) 

@app.get("/grade/{student_id}", response_model=List[Grade])
async def get_grades(student_id):
    sb_response = supabase.table('Grade').select('score', 'taskId').eq('studentId', student_id).execute()
    grades = sb_response.data
    return grades

# TODO: Update score? 
@app.put("grade/")
async def update_grade(grade: Grade):
    list = {'graderId': grade.graderId, 'taskId': grade.taskId, 'studentId': grade.studentId, 'score': grade.score}

    res = supabase.table("Grade").insert(list).execute()

    return JSONResponse({"message": "grade updated"})

# =====
# /quiz
# ===== 

@app.post("/quiz")
async def create_quiz(quiz: Quiz):
    response = supabase.table('Quiz').insert(dict(quiz)).execute()
    return JSONResponse(content={'message': 'quiz created'})    

# TODO: response models
# TODO: response
@app.get("/quiz/{quiz_id}/questions/")
async def get_question(quiz_id: int):
    response = supabase.table("Quiz").select('questions').eq('id', quiz_id).execute()
    return response

# =====
# /user
# =====

@app.post("/user")
async def create_user(user: User):
    sb_response = supabase.table('User').insert(dict(user)).execute()
    return JSONResponse(content={'message': 'user created'})

@app.get("/user/{discord_id}", response_model=User)
async def get_user(discord_id: int):
    sb_response = supabase.table('User').select('*').eq('discordId', discord_id).execute()
    user = User.parse_obj(sb_response.data[0])
    return user

@app.get("/user/{discord_id}/id")
async def get_user_id(discord_id: int, response_model=User, response_model_include={'id'}):
    user = await get_user(discord_id)
    return JSONResponse(content={'id': user.id})

@app.put("/user/{discord_id}/nick")
async def update_user_name(discord_id: int, name: str):
    sb_response = supabase.table('User').update({'name': name}).eq('discordId', discord_id).execute()
    return JSONResponse(content={'message': 'nickname updated'})

# ===================================================================================================

# TODO

# @app.put("/Assignment_Update/")
# async def update_assignment(dictionary: dict, channel_id: int):
#     supabase.table("Assignment").update(dictionary).eq('channelId', channel_id).execute()

# @app.put("/Quiz_Update/")
# async def update_quiz(dictionary: dict, channel_id: int):
#     supabase.table("Quiz").update(dictionary).eq('channelId', channel_id).execute()

# @app.post("/questions/")
# async def create_questions(questions: List[Question]):

#     ques_list = []
#     for question in questions:
#         temp = {'question': question.question, 'answer': question.answer, 'wrong': question.wrong,
#                 'points': question.points}
#         ques_list.append(temp)

#     bytes_obj = pickle.dumps(ques_list)
#     hash_object = hashlib.sha256(bytes_obj)
#     hex_dig = hash_object.hexdigest()

#     with open(f"{hex_dig}.json", "w") as outfile:
#         json.dump(ques_list, outfile)

#     outfile.close()

#     with open(f'{hex_dig}.json', 'r') as f:
#         data = json.load(f)

#     f.close()

#     json_string: str = json.dumps(data)

#     public_url = supabase.storage().from_('questions').get_public_url(f"{hex_dig}.json")

#     response = requests.get(public_url)

#     if response.status_code == 400:
#         res = supabase.storage().from_('questions').upload(f"{hex_dig}.json", json_string.encode())
#         public_url = supabase.storage().from_('questions').get_public_url(f"{hex_dig}.json")
#         os.remove(f'{hex_dig}.json')

#     return public_url




