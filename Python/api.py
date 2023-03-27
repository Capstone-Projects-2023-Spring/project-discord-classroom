from fastapi import FastAPI, File, UploadFile
from storage3.utils import StorageException
from supabase import create_client
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel
from typing import List
from create_classes import Quiz, Assignment, Grade
from create_classes import Question
import hashlib
import pickle
import asyncio
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
async def get_classroom_id(server_id: str):
    response = supabase.table('Classroom').select('*').eq('serverId', server_id).execute()
    if response.data is not []:
        return {'id': response.data[0]['id']}
    return JSONResponse(status_code=404, content={"message": "Classroom not found"})


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

@app.get("/member/id")
async def get_member_id(discord_id: str):
    response = supabase.table('User').select('id').eq('discordId', discord_id).execute()
    return response.data[0]

@app.get("/quiz/")
async def get_quiz(channel_id: str = 0):
    if channel_id == 0:
        return JSONResponse(status_code=404, content={"message": "Channel ID not given"})
    response = supabase.table("Quiz").select('*').eq('channelId', channel_id).execute()
    print(response)
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
async def get_assignment(channel_id: str = 0):
    if channel_id == 0:
        return JSONResponse(status_code=404, content={"message": "Channel ID not given"})
    response = supabase.table("Assignment").select('*').eq('channelId', channel_id).execute()
    print("response", response)
    return {'Assignment': response.data[0]}

# ---------------------------POST Methods-------------------------------

@app.post("/quizzes/")
async def create_quiz(quiz: Quiz, server_id: str):
    list = {'title': quiz.title, 'points': quiz.points, 'startDate': quiz.start, 'dueDate': quiz.due, 'timeLimit': quiz.time, 'channelId': quiz.channel, 'questions': quiz.questions}
    print(list)
    res = supabase.table("Quiz").insert(list).execute()
    print(res)
    response = await get_classroom_id(server_id)
    classroom_id = response['id']

    quiz_id = res.data[0]['id']
    list = {'classroomId': classroom_id, 'taskTypeId': quiz_id, 'taskType': "Quiz"}
    supabase.table("Classroom_Task").insert(list).execute()

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

@app.post("/classroom/")
async def create_classroom(id: str, name: str):
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
async def create_assignment(assignment: Assignment, server_id: str):
    list = {'title': assignment.title, 'startDate': assignment.start, 'dueDate': assignment.due, 'channelId': assignment.channel, 'points': assignment.points}

    res = supabase.table("Assignment").insert(list).execute()

    response = await get_classroom_id(server_id)
    classroom_id = response['id']
    assignment_id = res.data[0]['id']
    list = {'classroomId': classroom_id, 'taskTypeId': assignment_id, 'taskType': "Assignment"}
    supabase.table("Classroom_Task").insert(list).execute()

    return {"message": "assignment created successfully"}

@app.post("/Grade/")
async def update_grade(grade: Grade):
    list = {'graderId': grade.graderId, 'taskId': grade.taskId, 'studentId': grade.studentId, 'score': grade.score}

    res = supabase.table("Grade").insert(list).execute()

    return {"message": "grade updated successfully"}

# --------------------------- PUT Methods-------------------------------

@app.put("/member")
async def update_member_nick(nick: str, id: str):
    response = supabase.table('User').update({'name': nick}).eq('discordId', id).execute()
    return {'message': 'Nickname updated'}

@app.put("/member")
async def update_member_role(role: str, id: int, classroom_id: int):
    response = supabase.table('Classroom_User').update({'role': role}).eq('id', id).eq('classroomId', classroom_id).execute()
    return {'message': 'Role updated'}
