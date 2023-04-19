import create_classes
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pathlib import Path
from pydantic import BaseModel
from storage3.utils import StorageException
from supabase import create_client
from sqlite3 import Timestamp
from typing import List, Optional

import asyncio
import datetime
import hashlib
import json
import os
import pickle
import requests
import supabase as sb



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

#
# API Endpoints
#

# 
# /assignment
# 

@app.post("/assignment")
async def create_assignment(assignment: create_classes.Assignment):
    dictionary = assignment.dict()
    del dictionary['id']
    response = supabase.table('Assignment').insert(dictionary).execute()
    return {'message': 'assignment created'}
    # return JSONResponse(content={'message': 'assignment created'})

@app.get("/assignment", response_model=create_classes.Assignment)
async def get_assignment(channel_id:int):
    sb_response = supabase.table("Assignment").select('*').eq('channelId', channel_id).execute()
    assignment = create_classes.Assignment.parse_obj(sb_response.data[0])
    return {'Assignment': assignment}

@app.put("/assignment/")
async def update_assignment(dictionary: dict, channel_id: int):
    supabase.table("Assignment").update(dictionary).eq('channelId', channel_id).execute()
    return {'message': 'assignment updated'}
    # return JSONResponse(content={'message': 'assignment updated'})

# 
# /classroom
# 

@app.post("/classroom")
async def create_classroom(classroom: create_classes.Classroom):
    try:
        classroom_dict = classroom.dict()
        del classroom_dict['id']
        sb_response = supabase.table('Classroom').insert(classroom_dict).execute()
    except sb.PostgrestAPIError as e:
        return {'message': 'Classroom already exists'}
    return {'message': 'Classroom created'}
    # return JSONResponse(content={'message': 'quiz created'})
    
@app.get("/classroom", response_model=List[create_classes.Classroom])
async def get_all_classrooms():
    sb_response = supabase.table('Classroom').select('*').execute()
    classrooms = sb_response.data
    return {'classrooms': classrooms}

@app.delete("/classroom/")
async def delete_classroom(server_id: int):
    sb_resposne = supabase.table('Classroom').delete().eq('serverId', server_id).execute()
    return {'message': 'classroom deleted'}
    # return JSONResponse({'message': 'classroom deleted'})

@app.get("/classroom/{server_id}", response_model=create_classes.Classroom)
async def get_classroom(server_id: int):
    sb_response = supabase.table('Classroom').select('*').eq('serverId', server_id).execute()
    classroom = create_classes.Classroom.parse_obj(sb_response.data[0])
    return {'classroom': classroom}

@app.get("/classroom/{server_id}/attendance")
async def get_classroom_attendance(server_id: int):
    classroom = await get_classroom(server_id)
    return {'attendance': classroom['classroom'].attendance}
    # return JSONResponse(content={'attendance': classroom.attendance})

@app.get("/classroom/{server_id}/attendance")
async def get_classroom_id(server_id: int):
    classroom = await get_classroom(server_id)
    return {'id': classroom['classroom'].id}
    # return JSONResponse(content={'id': classroom.id})

# 
# /classroom_user
# 

@app.post("/classroom_user")
async def create_classroom_user(classroom_user: create_classes.Classroom_User):
    sb_response = supabase.table('Classroom_User').insert(classroom_user.dict()).execute()
    return {'message': 'classroom user create'}
    # return JSONResponse(content={'message': 'classroom user created'})

@app.get("/classroom_user/{classroom_id}/student", response_model=List[create_classes.Classroom_User])
async def get_students(classroom_id: int):
    sb_response = supabase.table('Classroom_User').select('*').match({'classroomId': classroom_id, 'role': "Student"}).execute()
    students = sb_response.data
    return {'students': students}
    # return student

@app.get("/classroom_user/{classroom_id}/educator", response_model=List[create_classes.Classroom_User])
async def get_educators(classroom_id: int):
    sb_response = supabase.table('Classroom_User').select('*').match({'classroomId': classroom_id, 'role': "Educator"}).execute()
    educators = sb_response.data
    return {'educators': educators}

@app.get("/classroom_user/{user_id}/{classroom_id}/attendance")
async def get_classroom_user_attendance(user_id: int, classroom_id: int):
    sb_response = supabase.table('Classroom_User').select('attendance').match({'classroomId': classroom_id, 'userId': user_id}).execute()
    classroom_user = sb_response.data
    return {'attendance': classroom_user[0]['attendance']}
    # return JSONResponse(content={'attendance': classroom_user.attendance})

@app.put("/classroom_user/{user_id}/{classroom_id}/attendance")
async def update_user_attendance(user_id: int, classroom_id: int):
    response = await get_classroom_user_attendance(user_id, classroom_id)
    attendance = response['attendance']
    sb_response = supabase.table('Classroom_User').update({'attendance': attendance+1}).match({'classroomId': classroom_id, 'userId': user_id}).execute()
    return {'message': 'attendance updated'}
    # return JSONResponse(content={'message': 'attendance updated'})

@app.put("/classroom_user/{user_id}/{classroom_id}/role")
async def update_classroom_user_role(user_id: int, classroom_id: int, role: str):
    if role == 'Student':
        attendance = 0
    else:
        attendance = None
    sb_response = supabase.table('Classroom_User').update({'role': role, 'attendance': attendance}).eq('userId', user_id).eq('classroomId', classroom_id).execute()
    return {'message': 'role updated'}

@app.put("/classroom_user/{user_id}/{classroom_id}/role")
async def update_classroom_user_name(new_name: str, discord_id: int):
    response = supabase.table('User').update({'name': new_name}).eq('discordId', discord_id).execute()
    return {'message': 'name updated'}




# 
# /discussion
# 

@app.post("/discussion")
async def create_discussion(discussion: create_classes.Discussion):
    dictionary = discussion.dict()
    del dictionary['id']
    sb_response = supabase.table('Discussion').insert(dictionary).execute()
    return {'message': 'discussion created'}
    # return JSONResponse(content={'message': 'discussion created'})

# 
# /grade
# 

@app.post("/grade")
async def create_grade(grade: create_classes.Grade):
    sb_response = supabase.table('Grade').insert(grade.dict()).execute()
    return {'message': 'grade created'}
    # return JSONResponse(content={'message': 'grade created'})

@app.get("/grade/{student_id}", response_model=List[create_classes.Grade])
async def get_grades(student_id):
    sb_response = supabase.table('Grade').select('score', 'taskId').eq('studentId', student_id).execute()
    grades = sb_response.data
    return {'grades': grades}

@app.put("grade/")
async def update_grade(grade: create_classes.Grade):
    # This makes no sense we are inserting instead of updating
    sb_response = supabase.table("Grade").insert(grade.dict()).execute()
    return {'message': "grade updated"}
    # return JSONResponse({"message": "grade updated"})

# 
# /quiz
#

@app.get("/quiz/")
async def get_quiz(channel_id: int):
    response = supabase.table("Quiz").select('*').eq('channelId', channel_id).execute()
    return {'quiz': response.data[0]}

@app.post("/quiz")
async def create_quiz(quiz: create_classes.Quiz):
    dictionary = quiz.dict()
    del dictionary['id']
    response = supabase.table('Quiz').insert(dictionary).execute()
    return {'message': 'quiz created'}
    # return JSONResponse(content={'message': 'quiz created'})

@app.put("/quiz/")
async def update_quiz(dictionary: dict, channel_id: int):
    supabase.table("Quiz").update(dictionary).eq('channelId', channel_id).execute()
    return {'message': 'quiz updated'}
    # return JSONResponse(content={'message': 'quiz updated'})

@app.get("/quiz/{quiz_id}/questions/")
async def get_questions(quiz_id: int):
    response = supabase.table("Quiz").select('questions').eq('id', quiz_id).execute()
    url = response.data[0]['questions']
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {'questions': data}
    else:
        return {'message': 'Error retrieving questions'}
    # return JSONResponse(content=response.data[0])

@app.post("/quiz/questions/")
async def create_questions(questions: List[create_classes.Question]):
    ques_list = []
    for question in questions:
        ques_list.append(question.dict())

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

    return {'url': public_url}

#
# /tokens
#
@app.post("/token/")
async def update_token(token: create_classes.Token):
    list = {'created_at': 'now()', 'userId': token.userId, 'unique_id': token.unique_id}
    res = supabase.table("Tokens").insert(list).execute()

    return {'message': 'token updated'}

# 
# /user
# 

@app.post("/user")
async def create_user(user: create_classes.User):
    user_dict = user.dict()
    del user_dict['id']
    sb_response = supabase.table('User').insert(user_dict).execute()
    return {'message': 'user created'}

@app.get("/user/{discord_id}", response_model=create_classes.User)
async def get_user(discord_id: int):
    sb_response = supabase.table('User').select('*').eq('discordId', discord_id).execute()
    if not sb_response.data:
        return {'message': 'user not found'}
    else:
        user = create_classes.User.parse_obj(sb_response.data[0])
        return {'user': user}

@app.get("/user/{discord_id}/id")
async def get_user_id(discord_id: int):
    sb_response = supabase.table('User').select('*').eq('discordId', discord_id).execute()
    if not sb_response.data:
        return {'message': 'user not found'}
    return {'id': sb_response.data[0]['id']}

@app.put("/user/{discord_id}/nick")
async def update_user_name(discord_id: int, name: str):
    sb_response = supabase.table('User').update({'name': name}).eq('discordId', discord_id).execute()
    return {'message': 'nickname updated'}