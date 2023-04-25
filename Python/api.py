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
# API Tags
#

tags_metadata = [
    {
        "name": "assignment",
        "description": "Manage assignments.",
    },
    {
        "name": "classroom",
        "description": "Manage classrooms, and retrieve classroom attendance.",
    },
    {
        "name": "classroom_user",
        "description": "Manange user classroom information including their roles and attendance".",
    },
    {
        "name": "discussion",
        "description": "Manage discussion board.",
    },
    {
        "name": "grade",
        "description": "Manage grades.",
    },
    {
        "name": "quiz",
        "description": "Manage quizzes and their questions.",
    },
    {
        "name": "token",
        "description": "Manage tokens for file submission.",
    },
    {
        "name": "user",
        "description": "Manage user's Discord information.",
    },
]

#
# API Endpoints
#

# 
# /assignment
# 

@app.post(
    "/assignment"
    summary="Create a new assignment in the database"
)
async def create_assignment(assignment: create_classes.Assignment):
    """
    Creates a new assignment in the database from an Assignment object

    - **assignment**: an Assignment object
    """
    dictionary = assignment.dict()
    del dictionary['id']
    response = supabase.table('Assignment').insert(dictionary).execute()
    return {'message': 'assignment created'}
    # return JSONResponse(content={'message': 'assignment created'})

@app.get("/assignment", 
        response_model=create_classes.Assignment,
        summary="Gets an assignment from the database"
)
async def get_assignment(channel_id:int):
    """
    Gets the assignment associated with 'channel_id' from the database

    - **channel_id**: the assignment's Discord channel ID
    """
    sb_response = supabase.table("Assignment").select('*').eq('channelId', channel_id).execute()
    assignment = create_classes.Assignment.parse_obj(sb_response.data[0])
    return {'Assignment': assignment}

@app.put(
    "/assignment/",
    summary="Updates assignment in the database",
)
async def update_assignment(dictionary: dict, channel_id: int):
    """
    Updates the assignment associated with 'channel_id' in the database using information in 'dictionary'

    - **dictionary**: the assignment information to be updated in dictionary format
    - **channel_id**: the assignment's Discord channel ID
    """
    supabase.table("Assignment").update(dictionary).eq('channelId', channel_id).execute()
    return {'message': 'assignment updated'}
    # return JSONResponse(content={'message': 'assignment updated'})

# 
# /classroom
# 

@app.post(
    "/classroom",
    summary="Creates a new classroom in the database"
)
async def create_classroom(classroom: create_classes.Classroom):
    """
    Creates a new classroom in the database from a Classroom object

    - **classroom**: a Classroom object
    """
    try:
        classroom_dict = classroom.dict()
        del classroom_dict['id']
        sb_response = supabase.table('Classroom').insert(classroom_dict).execute()
    except sb.PostgrestAPIError as e:
        return {'message': 'Classroom already exists'}
    return {'message': 'Classroom created'}
    # return JSONResponse(content={'message': 'quiz created'})
    
@app.get(
    "/classroom", 
    response_model=List[create_classes.Classroom]
    summary="Gets a list of all classrooms in the database"
)
async def get_all_classrooms():
    """
    Gets a list of all classrooms in the database
    """
    sb_response = supabase.table('Classroom').select('*').execute()
    classrooms = sb_response.data
    return {'classrooms': classrooms}

@app.delete(
    "/classroom/",
    summary="Deletes a specific classroom from the database"
)
async def delete_classroom(server_id: int):
    """
    Deletes the classroom associated with 'server_id' from the database

    - **server_id**: the classroom's Discord server ID
    """
    sb_resposne = supabase.table('Classroom').delete().eq('serverId', server_id).execute()
    return {'message': 'classroom deleted'}
    # return JSONResponse({'message': 'classroom deleted'})

@app.get(
    "/classroom/{server_id}", 
    response_model=create_classes.Classroom
    summary="Gets a specific classroom from the database"
)
async def get_classroom(server_id: int):
    """
    Gets the classroom associated with 'server_id' from the database

    - **server_id**: the classroom's Discord server ID
    """
    sb_response = supabase.table('Classroom').select('*').eq('serverId', server_id).execute()
    classroom = create_classes.Classroom.parse_obj(sb_response.data[0])
    return {'classroom': classroom}

@app.get(
    "/classroom/{server_id}/attendance",
    summary="Gets the attendance information of a specific classroom from the database"
)
async def get_classroom_attendance(server_id: int):
    """
    Gets the attendance information of the classroom associated with 'server_id' from the database

    - **server_id**: the classroom's Discord server ID
    """
    classroom = await get_classroom(server_id)
    return {'attendance': classroom['classroom'].attendance}
    # return JSONResponse(content={'attendance': classroom.attendance})

@app.get(
    "/classroom/{server_id}/id",
    summary="Gets the ID of a specific classroom from the database"
    )
async def get_classroom_id(server_id: int):
    """
    Gets the database ID of the classroom associated with 'server_id' from the database

    - **server_id**: the classroom's Discord server ID
    """
    classroom = await get_classroom(server_id)
    return {'id': classroom['classroom'].id}
    # return JSONResponse(content={'id': classroom.id})

# 
# /classroom_user
# 

@app.post(
    "/classroom_user",
    summary="Creates a new classroom user in the database"
)
async def create_classroom_user(classroom_user: create_classes.Classroom_User):
    """
    Creates a new classroom user from a Classroom_User object in the database

    - **classroom_user**: a Classroom_User object
    """
    sb_response = supabase.table('Classroom_User').insert(classroom_user.dict()).execute()
    return {'message': 'classroom user create'}
    # return JSONResponse(content={'message': 'classroom user created'})

@app.get(
    "/classroom_user/{classroom_id}/student", 
    response_model=List[create_classes.Classroom_User],
    summary="Gets a list of students of a specific classroom from the database"
)
async def get_students(classroom_id: int):
    """
    Gets a list of students in the classroom associated with 'classroom_id' from the database

    - **classroom_id**: the classroom's database ID
    """
    sb_response = supabase.table('Classroom_User').select('*').match({'classroomId': classroom_id, 'role': "Student"}).execute()
    students = sb_response.data
    return {'students': students}
    # return student

@app.get(
    "/classroom_user/{classroom_id}/educator",
    response_model=List[create_classes.Classroom_User],
    summary="Gets a list of educators of a specific classroom from the database"
)
async def get_educators(classroom_id: int):
    """
    Gets a list of educators in the classroom associated with 'classroom_id' from the database

    - **classroom_id**: the classroom's database ID
    """
    sb_response = supabase.table('Classroom_User').select('*').match({'classroomId': classroom_id, 'role': "Educator"}).execute()
    educators = sb_response.data
    return {'educators': educators}

@app.get(
    "/classroom_user/{user_id}/{classroom_id}/attendance",
    summary="Gets the attendance information of a specific student from the database"
)
async def get_classroom_user_attendance(user_id: int, classroom_id: int):
    """
    Gets the attendance information of the user associated with 'user_id' in the classroom associated with 'classroom_id' from the database

    - **user_id**: the user's database ID
    - **classroom_id**: the classroom's database ID
    """
    sb_response = supabase.table('Classroom_User').select('attendance').match({'classroomId': classroom_id, 'userId': user_id}).execute()
    classroom_user = sb_response.data
    return {'attendance': classroom_user[0]['attendance']}
    # return JSONResponse(content={'attendance': classroom_user.attendance})

@app.put(
    "/classroom_user/{user_id}/{classroom_id}/attendance",
    summary="Updates the attendance information of a specifc student in the database"
)
async def update_user_attendance(user_id: int, classroom_id: int):
    """
    Updates the attendance of the user associated with 'user_id' in the classroom associated with 'classroom_id' in the database

    - **user_id**: the user's database ID
    - **classroom_id**: the classroom's database ID
    """
    response = await get_classroom_user_attendance(user_id, classroom_id)
    attendance = response['attendance']
    sb_response = supabase.table('Classroom_User').update({'attendance': attendance+1}).match({'classroomId': classroom_id, 'userId': user_id}).execute()
    return {'message': 'attendance updated'}
    # return JSONResponse(content={'message': 'attendance updated'})

@app.put(
    "/classroom_user/{user_id}/{classroom_id}/role",
    summary="Updates the role of a specific user in the database"
)
async def update_classroom_user_role(user_id: int, classroom_id: int, role: str):
    """
    Updates the role of the user associated with 'user_id' in the classroom associated with 'classroom_id' to 'role' in the database

    - **user_id**: the user's database ID
    - **classroom_id**: the classroom's database ID
    - **role**: the user's new role
    """
    if role == 'Student':
        attendance = 0
    else:
        attendance = None
    sb_response = supabase.table('Classroom_User').update({'role': role, 'attendance': attendance}).eq('userId', user_id).eq('classroomId', classroom_id).execute()
    return {'message': 'role updated'}

@app.put(
    "/classroom_user/{user_id}/{classroom_id}/role",
    summary="Updates the username of a specific user in the database"
)
async def update_classroom_user_name(new_name: str, discord_id: int):
    """
    Updates the username of the user associated with 'discord_id' to 'new_name' in the database

    - **new_name**: the user's new username
    - **discord_id**: the user's discord ID
    """
    response = supabase.table('User').update({'name': new_name}).eq('discordId', discord_id).execute()
    return {'message': 'name updated'}




# 
# /discussion
# 

@app.post(
    "/discussion",
    summary="Creates a new discussion board in the database"
)
async def create_discussion(discussion: create_classes.Discussion):
    """
    Creates a new discussion board in the database from a Discussion object

    - **discussion**: a Discussion object
    """
    dictionary = discussion.dict()
    del dictionary['id']
    sb_response = supabase.table('Discussion').insert(dictionary).execute()
    return {'message': 'discussion created'}
    # return JSONResponse(content={'message': 'discussion created'})

# 
# /grade
# 

@app.post(
    "/grade",
    summary="Creates a new grade in the database"
)
async def create_grade(grade: create_classes.Grade):
    """
    Creates a new grade in the database from a Grade object

    - **grade**: a Grade object
    """
    sb_response = supabase.table('Grade').insert(grade.dict()).execute()
    return {'message': 'grade created'}
    # return JSONResponse(content={'message': 'grade created'})

@app.get(
    "/grade/{student_id}", 
    response_model=List[create_classes.Grade],
    summary="Gets a list of all grades of a specific student from the database"
)
async def get_grades(student_id):
    """
    Gets a list of all grades for the student associated with 'student_id'

    - **student_id**: the student's database ID
    """
    sb_response = supabase.table('Grade').select('score', 'taskId').eq('studentId', student_id).execute()
    grades = sb_response.data
    return {'grades': grades}

@app.put(
    "grade/",
    summary="Updates a grade in the database"
)
async def update_grade(grade: create_classes.Grade):
    """
    Updates a grade in the database using a Grade object

    - **grade**: a Grade object
    """
    # This makes no sense we are inserting instead of updating
    sb_response = supabase.table("Grade").insert(grade.dict()).execute()
    return {'message': "grade updated"}
    # return JSONResponse({"message": "grade updated"})

# 
# /quiz
#

@app.get(
    "/quiz/",
    summary="Gets a specific quiz from the database"
)
async def get_quiz(channel_id: int):
    """
    Gets the quiz associated with 'channel_id' from the database

    - **channel_id**: the quiz's Discord channel ID
    """
    response = supabase.table("Quiz").select('*').eq('channelId', channel_id).execute()
    return {'quiz': response.data[0]}

@app.post(
    "/quiz",
    summary="Creates a new quiz in the database"
)
async def create_quiz(quiz: create_classes.Quiz):
    """
    Creates a new quiz in the database from a Quiz object

    - **quiz**: a Quiz object
    """
    dictionary = quiz.dict()
    del dictionary['id']
    response = supabase.table('Quiz').insert(dictionary).execute()
    return {'message': 'quiz created'}
    # return JSONResponse(content={'message': 'quiz created'})

@app.put(
    "/quiz/",
    summary="Updates a quiz in the database"
)
async def update_quiz(dictionary: dict, channel_id: int):
    """
    Updates the quiz associated with 'channel_id' in the database using information in 'dictionary'

    - **dictionary**: the quiz information to be updated in dictionary format
    - **channel_id**: the quiz's Discord channel ID
    """
    supabase.table("Quiz").update(dictionary).eq('channelId', channel_id).execute()
    return {'message': 'quiz updated'}
    # return JSONResponse(content={'message': 'quiz updated'})

@app.get(
    "/quiz/{quiz_id}/questions/",
    summary="Gets the URL containing the questions of a specific quiz from the database"
)
async def get_questions(quiz_id: int):
    """
    Gets a URL that links to questions of the quiz associated with 'quiz_id' in JSON format

    - **quiz_id**: the quiz's database ID
    """
    response = supabase.table("Quiz").select('questions').eq('id', quiz_id).execute()
    url = response.data[0]['questions']
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {'questions': data}
    else:
        return {'message': 'Error retrieving questions'}
    # return JSONResponse(content=response.data[0])

@app.post(
    "/quiz/questions/",
    summary="Creates URL containing questions for a quiz"
)
async def create_questions(questions: List[create_classes.Question]):
    """
    Creates a URL that links to quiz questions in JSON format

    - **questions**: a list of Question objects
    """
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
@app.post(
    "/token/",
    summary="Updates a token in the database"
)
async def update_token(token: create_classes.Token):
    """
    Updates a token in the database from a Token object

    - **user**: a Token object
    """
    list = {'created_at': 'now()', 'userId': token.userId, 'unique_id': token.unique_id}
    res = supabase.table("Tokens").insert(list).execute()

    return {'message': 'token updated'}

# 
# /user
# 

@app.post(
    "/user",
    summary="Creates a new user in the database"
)
async def create_user(user: create_classes.User):
    """
    Creates a new user in the database from a User object

    - **user**: a User object
    """
    user_dict = user.dict()
    del user_dict['id']
    sb_response = supabase.table('User').insert(user_dict).execute()
    return {'message': 'user created'}

@app.get(
    "/user/{discord_id}",
    response_model=create_classes.User,
    summary="Gets a specific user from the database"
)
async def get_user(discord_id: int):
    """
    Gets the user associated with 'discord_id' from the databse

    - **discord_id**: the user's discord ID
    """
    sb_response = supabase.table('User').select('*').eq('discordId', discord_id).execute()
    if not sb_response.data:
        return {'message': 'user not found'}
    else:
        user = create_classes.User.parse_obj(sb_response.data[0])
        return {'user': user}

@app.get(
    "/user/{discord_id}/id",
    summary="Gets the ID of a specific user from the database",
)
async def get_user_id(discord_id: int):
    """
    Updates the database ID of the user associated with 'discord_id'

    - **discord_id**: the user's discord ID
    """
    sb_response = supabase.table('User').select('*').eq('discordId', discord_id).execute()
    if not sb_response.data:
        return {'message': 'user not found'}
    return {'id': sb_response.data[0]['id']}

@app.put(
    "/user/{discord_id}/nick",
    summary="Updates the username of a specific user in the database",
)
async def update_user_name(discord_id: int, name: str):
    """
    Updates the username associated with 'discord_id' to 'name' in the database

    - **discord_id**: the user's discord ID
    - **name**: the user's new username
    """
    sb_response = supabase.table('User').update({'name': name}).eq('discordId', discord_id).execute()
    return {'message': 'nickname updated'}