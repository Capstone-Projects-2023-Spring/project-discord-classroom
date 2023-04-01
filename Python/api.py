from fastapi import FastAPI, File, UploadFile
from storage3.utils import StorageException
from supabase import create_client
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel
from typing import List
from create_classes import Quiz, Assignment, Grade, Discussion
from create_classes import Question
import hashlib
import pickle
import asyncio
import requests

app = FastAPI(
    title="ClassroomBotAPI",
    version="0.0.1"
)

json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Python/config.json"))

print(json_path)

if json_path:
    with open(json_path) as f:
        configData = json.load(f)
else:
    print("ERROR: config.json does not exist")
    exit

# Create a Supabase client instance
supabase = create_client(
    configData["SupaUrl"],
    configData["SupaKey"]
)

#classes
class Classroom(BaseModel):
    id: int
    serverId: str
    serverName: str

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
    classroomId: int
    totalAttendance: int
    totalGrade: int

class Message(BaseModel):
    message: str


@app.get("/classrooms", response_model=List[Classroom])
async def get_classrooms():
    response = supabase.table('Classroom').select('*').execute()
    classrooms = response.data
    return classrooms


@app.get("/classroomId", response_model=ClassroomId, responses={404: {"model": Message}})
async def get_classroom_id(server_id: int):
    response = supabase.table('Classroom').select('*').eq('serverId', server_id).execute()
    if response.data is not []:
        return {'id': response.data[0]['id']}
    return JSONResponse(status_code=404, content={"message": "Classroom not found"})

@app.get("/classroomAttendance")
async def get_classroom_attendance(server_id: int):
    response = supabase.table('Classroom').select('attendance').eq('serverId', server_id).execute()
    if response.data is not []:
        return {'attendance': response.data[0]['attendance']}
    return JSONResponse(status_code=404, content={"message": "Classroom not found"})


@app.get("/user")
async def get_user_id(discord_id: int):
    response = supabase.table('User').select('id').eq('discordId', discord_id).execute()
    if response.data:
        return {'id': response.data[0]['id']}
    return JSONResponse(status_code=404, content={"message": "User not found"})

@app.get("/userAttendance")
async def get_user_attendance(user_id: int, classroom_id: int):
    response = supabase.table('Classroom_User').select('attendance').match({'classroomId': classroom_id, 'userId': user_id}).execute()
    if response.data:
        return {'attendance': response.data[0]['attendance']}
    return JSONResponse(status_code=404, content={"message": "User not found"})

@app.put("/userAttendance")
async def update_user_attendance(old_attendance: int, user_id: int, classroom_id: int):
    response = supabase.table('Classroom_User').update({'attendance': old_attendance+1}).match({'classroomId': classroom_id, 'userId': user_id}).execute()


@app.get("/educators/", response_model=List[Educator], responses={404: {"model": Message}})
async def get_educators(classroom_id: int = 0):
    if classroom_id == 0:
        return JSONResponse(status_code=404, content={"message": "ClassroomId not given"})
    response = supabase.table('Classroom_User').select('*').match(
        {'role': "Educator", 'classroomId': classroom_id}).execute()
    edu_ids = []
    data = response.data
    for d in data:
        edu_ids.append(d['userId'])
    educators = []
    for id in edu_ids:
        stu = supabase.table('User').select('*').eq('id', id).execute()
        if stu.data:
            educators.append(stu.data[0])
    if educators:
        return educators
    return JSONResponse(status_code=404, content={"message": "Classroom not found"})


@app.get("/students/", response_model=List[Student], responses={404: {"model": Message}})
async def get_students(classroom_id: int = 0):
    if classroom_id == 0:
        return JSONResponse(status_code=404, content={"message": "ClassroomId not given"})
    response = supabase.table('Classroom_User').select('*').match({'role': "Student", 'classroomId': classroom_id}).execute()
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
    else:
        print('Failed to download JSON data.')
        return {'message', "Error retrieving question"}

@app.get("/Assignment/")
async def get_assignment(channel_id: int = 0):
    if channel_id == 0:
        return JSONResponse(status_code=404, content={"message": "Channel ID not given"})
    response = supabase.table("Assignment").select('*').eq('channelId', channel_id).execute()
    return {'Assignment': response.data[0]}

# ---------------------------POST Methods-------------------------------

@app.post("/quizzes/")
async def create_quiz(quiz: Quiz):
    list = {'title': quiz.title, 'points': quiz.points, 'startDate': quiz.start, 'dueDate': quiz.due, 'timeLimit': quiz.time,
            'channelId': quiz.channelId, 'classroomId': quiz.classroomId, 'questions': quiz.questions}
    res = supabase.table("Quiz").insert(list).execute()

    return {"message": "Quiz created successfully"}

@app.post("/questions/")
async def create_questions(questions: List[Question]):

    ques_list = []
    for question in questions:
        temp = {'question': question.question, 'answer': question.answer, 'wrong': question.wrong,
                'points': question.points}
        ques_list.append(temp)

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

    response = requests.get(public_url)

    if response.status_code == 400:
        res = supabase.storage().from_('questions').upload(f"{hex_dig}.json", json_string.encode())
        public_url = supabase.storage().from_('questions').get_public_url(f"{hex_dig}.json")
        os.remove(f'{hex_dig}.json')

    return public_url

@app.delete("/classroom/")
async def remove_classroom(id: int):
    supabase.table('Classroom').delete().eq('serverId', id).execute()
    return {'message': 'Classroom deleted'}

@app.post("/classroom/")
async def create_classroom(id: int, name: str):
    list = {'serverId': id, 'serverName': name}
    supabase.table('Classroom').insert(list).execute()
    return {'message': 'Classroom created'}

@app.post("/educator/")
async def create_educator(id: str, name:str, server: str):
    response = supabase.table("Classroom").select('id').eq("serverId", server).execute()
    classroom_id = response.data[0]['id']
    list = {'discordId': id, 'name': name}
    response = supabase.table('User').insert(list).execute()
    user_id = response.data[0]['id']
    list = {'classroomId': classroom_id, 'userId': user_id, 'role': "Educator"}
    supabase.table('Classroom_User').insert(list).execute()
    return {'message': 'Educator created'}

@app.post("/student/")
async def create_student(id: str, name:str, server: str):
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
    list = {'title': assignment.title, 'points': assignment.points, 'startDate': assignment.start, 'dueDate': assignment.due,
            'channelId': assignment.channelId, 'classroomId': assignment.classroomId}

    res = supabase.table("Assignment").insert(list).execute()

    return {"message": "assignment created successfully"}

@app.post("/Discussions/")
async def create_discussion(discussion: Discussion):
    list = {'title': discussion.title, 'points': discussion.points, 'startDate': discussion.start, 'dueDate': discussion.due,
            'channelId': discussion.channelId, 'classroomId': discussion.classroomId}

    res = supabase.table("Discussion").insert(list).execute()

    return {"message": "assignment created successfully"}

@app.post("/Grade/")
async def update_grade(grade: Grade):
    list = {'graderId': grade.graderId, 'taskId': grade.taskId, 'studentId': grade.studentId, 'score': grade.score}

    res = supabase.table("Grade").insert(list).execute()

    return {"message": "grade updated successfully"}

# --------------------------- PUT Methods-------------------------------

# /user

@app.put("/user")
async def create_user(nick: str, discord_id: int):
    response = supabase.table('User').insert({'discordId': discord_id, 'name': nick }).execute()
    return {'message': 'User created', 'id': response.data[0]['id']}

@app.get("/user/id")
async def get_user_id(discord_id: int):
    response = supabase.table('User').select('id').eq('discordId', discord_id).execute()
    if response.data:
        return response.data[0]
    else:
        return {'message': 'User not found'}

@app.put("/user/nick")
async def update_user_nick(nick: str, discord_id: int):
    response = supabase.table('User').update({'name': nick}).eq('discordId', discord_id).execute()
    return {'message': 'Nickname updated'}

@app.put("/member")
async def update_member_role(role: str, id: int, classroom_id: int):
    if role == "Student":
        response = supabase.table('Classroom_User').update({'role': role, 'attendance': 0}).match({'userId': id, 'classroomId': classroom_id}).execute()
    else:
        response = supabase.table('Classroom_User').update({'role': role, 'attendance': None}).match({'userId': id, 'classroomId': classroom_id}).execute()
# /classroom_user

@app.post('/classroom_user')
async def create_classroom_user(classroom_id: int, user_id: int, name: str, role:str):
    if role == 'Student':
        attendance = 0
    else:
        attendance = None
    supabase.table("Classroom_User").insert({"classroomId": classroom_id, 'userId': user_id, 'role': role, 'attendance': attendance}).execute()
    return {'message': 'Classroom user created'}
    
@app.put("/classroom_user")
async def update_classroom_user_role(role: str, user_id: int, classroom_id: int):
    if role == 'Student':
        attendance = 0
    else:
        attendance = None
    response = supabase.table('Classroom_User').update({'role': role, 'attendance': attendance}).eq('userId', user_id).eq('classroomId', classroom_id).execute()
    return {'message': 'Role updated'}
