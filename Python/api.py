from create_classes import Assignment, Discussion, Grade, Question, Quiz
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from storage3.utils import StorageException
from supabase import create_client
from typing import List

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
    channelId: int
    points: int
    startDate: datetime.date
    dueDate: datetime.date
    classroom_id: int
    title: str

class Classroom(BaseModel):
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
    name: str
    discordId: int

# Endpoints

# /assignment

@app.post("/assignment")
async def create_assignment(assignment: Assignment):
    response = supabase.table('Assignment').insert(dict(assignment)).execute()
    return response

@app.get("/assignment")
async def get_assignment(channel_id:int):
    response = supabase.table("Assignment").select('*').eq('channelId', channel_id).execute()
    return response

# /classroom

@app.post("/classroom")
async def create_classroom(classroom: Classroom):
    response = supabase.table('Classroom').insert(dict(classroom)).execute()
    return response    

@app.get("/classroom")
async def get_classroom():
    response = supabase.table('Classroom').select('*').execute()
    return response

@app.get("/classroom/{server_id})
async def get_classroom(server_id: int):
    response = supabase.table('Classroom').select('*').eq('serverId', server_id).execute()
    return response

@app.get("/classroom/{server_id}/attendance")
async def get_classroom_attendance(server_id: int):
    response = supabase.table('Classroom').select('attendance').eq('serverId', server_id).execute()
    return response

# /classroom_user

@app.post("/classroom_user")
async def create_classroom_user(classroom_user: Classroom_User):
    response = supabase.table('Classroom_User').insert(dict(classroom_user)).execute()
    return response

@app.get("/classroom_user/{user_id}/{classroom_id}/attendance")
async def get_user_attendance(user_id: int, classroom_id: int):
    response = supabase.table('Classroom_User').select('attendance').match({'classroomId': classroom_id, 'userId': user_id}).execute()
    return response

@app.get("/classroom_user/{classroom_id}/student")
    response = supabase.table('Classroom_User').select('*').match({'classroomId': classroom_id, 'role': "Student"}).execute()
    return response

@app.get("/classroom_user/{classroom_id}/educator")
    response = supabase.table('Classroom_User').select('*').match({'classroomId': classroom_id, 'role': "Educator"}).execute()
    return response

# /discussion

@app.post("/discussion")
async def create_discussion(discussion: Discussion):
    response = supabase.table('Discussion').insert(dict(discussion)).execute()
    return response

# /grade

@app.post("/grade")
async def create_grade(grade: Grade):
    response = supabase.table('Grade').insert(dict(grade)).execute()
    return response
    
@app.get("/grades/{student_id}")
async def get_grades(student_id):
    response = supabase.table('Grade').select('score', 'taskId').eq('studentId', student_id).execute()
    return response

# /quiz

@app.post("/quiz")
async def create_quiz(quiz: Quiz):
    response = supabase.table('Quiz').insert(dict(quiz)).execute()
    return response

async def get_assignment(channel_id: int):
    response = supabase.table("Quiz").select('*').eq('channelId', channel_id).execute()
    return response

@app.get("/quiz/{quiz_id}/questions/")
async def get_question(quiz_id: int):
    response = supabase.table("Quiz").select('questions').eq('id', quiz_id).execute()
    return response

# /user

@app.post("/user")
async def create_user(user: User):
    response = supabase.table('User').insert(dict(user)).execute()
    return response

@app.get("/user/{discord_id}")
async def get_user(discord_id:int):
    response = supabase.table('User').select('*').eq('discordId', discord_id).execute()
    return response

# TODO: Only return id
@app.get("/user/{discord_id}/id")
async def get_user_id(discord_id: int):
    response = supabase.table('User').select('id').eq('discordId', discord_id).execute()
    return response











# @app.put("/userAttendance")
# async def update_user_attendance(old_attendance: int, user_id: int, classroom_id: int):
#     response = supabase.table('Classroom_User').update({'attendance': old_attendance+1}).match({'classroomId': classroom_id, 'userId': user_id}).execute()

# @app.put("/Assignment_Update/")
# async def update_assignment(dictionary: dict, channel_id: int):
#     supabase.table("Assignment").update(dictionary).eq('channelId', channel_id).execute()

# @app.put("/Quiz_Update/")
# async def update_quiz(dictionary: dict, channel_id: int):
#     supabase.table("Quiz").update(dictionary).eq('channelId', channel_id).execute()

# # ---------------------------POST Methods-------------------------------


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

# @app.delete("/classroom/")
# async def remove_classroom(id: int):
#     supabase.table('Classroom').delete().eq('serverId', id).execute()
#     return {'message': 'Classroom deleted'}


# @app.post("/Grade/")
# async def update_grade(grade: Grade):
#     list = {'graderId': grade.graderId, 'taskId': grade.taskId, 'studentId': grade.studentId, 'score': grade.score}

#     res = supabase.table("Grade").insert(list).execute()

#     return {"message": "grade updated successfully"}

# # --------------------------- PUT Methods-------------------------------

# # /user

# @app.put("/user")
# async def create_user(nick: str, discord_id: int):
#     response = supabase.table('User').insert({'discordId': discord_id, 'name': nick }).execute()
#     return {'message': 'User created', 'id': response.data[0]['id']}

# @app.put("/user/nick")
# async def update_user_nick(nick: str, discord_id: int):
#     response = supabase.table('User').update({'name': nick}).eq('discordId', discord_id).execute()
#     return {'message': 'Nickname updated'}

# @app.put("/member")
# async def update_member_role(role: str, id: int, classroom_id: int):
#     if role == "Student":
#         response = supabase.table('Classroom_User').update({'role': role, 'attendance': 0}).match({'userId': id, 'classroomId': classroom_id}).execute()
#     else:
#         response = supabase.table('Classroom_User').update({'role': role, 'attendance': None}).match({'userId': id, 'classroomId': classroom_id}).execute()
# # /classroom_user
    
# @app.put("/classroom_user")
# async def update_classroom_user_role(role: str, user_id: int, classroom_id: int):
#     if role == 'Student':
#         attendance = 0
#     else:
#         attendance = None
#     response = supabase.table('Classroom_User').update({'role': role, 'attendance': attendance}).eq('userId', user_id).eq('classroomId', classroom_id).execute()
#     return {'message': 'Role updated'}
