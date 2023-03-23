from fastapi import FastAPI, File, UploadFile
from storage3.utils import StorageException
from supabase import create_client
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel
from typing import List
from cr_classes import Quiz
from cr_classes import Question
import hashlib
import pickle
import asyncio

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

class Grade(BaseModel):
    type: str
    name: str
    score: int
    maxScore: int

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
        combined = {'type': r1.data[0]['taskType'], 'name': r2.data[0]['name'], 'score': info['score'],
                    'points': r2.data[0]['points']}
        all.append(combined)
    return all

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

    public_url = supabase.storage().from_('questions').get_public_url(f"{hex_dig}.json")

    try:
        res = supabase.storage().from_('questions').upload(f"{hex_dig}.json", f".\\{hex_dig}.json", {"upsert": 'true'})
        url = str(res.url)
    except StorageException:
        print("StorageException")
        url = public_url
    return url

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

# --------------------------- PUT Methods-------------------------------

@app.put("/member")
async def update_member(before: name, after: name):
    if before.nick != after.nick:
        response = supabase.table('User').update({'name': after.nick}).eq('discordId', str(after.id)).execute()

    if before.role != after.role:
        response = supabase.table('Classroom_User').update({'role': after.role}).eq('discordId', str(after.role)).execute()

    return {'message': 'Member updated'} # TODO: Update return message