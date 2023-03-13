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
async def get_classroom_id(serverId: int = 0):
    response = supabase.table('Classroom').select('*').eq('serverId', serverId).execute()
    if response.data is not []:
        return {'id': response.data[0]['id']}
    return JSONResponse(status_code=404, content={"message": "Classroom not found"})


@app.get("/educators/", response_model=List[Educator], responses={404: {"model": Message}})
async def get_educators(classroomId: int = 0):
    if classroomId == 0:
        return JSONResponse(status_code=404, content={"message": "ClassroomId not given"})
    response = supabase.table('Section').select('*').eq('classroomId', classroomId).execute()
    sections = []
    data = response.data
    for d in data:
        sections.append(d['id'])
    educators = []
    for sect in sections:
        e = supabase.table('Educator').select('*').eq('sectionId', sect).execute()
        if e.data:
            educators.append(e.data[0])
    if educators:
        return educators
    return JSONResponse(status_code=404, content={"message": "Classroom not found"})


@app.get("/students/", response_model=List[Student], responses={404: {"model": Message}})
async def get_students(classroomId: int = 0):
    response = supabase.table('Section').select('*').eq('classroomId', classroomId).execute()
    sections = []
    data = response.data
    for d in data:
        sections.append(d['id'])
    students = []
    for sect in sections:
        stu = supabase.table('Student').select('*').eq('sectionId', sect).execute()
        if stu.data:
            students.append(stu.data[0])
    return students


@app.get("/sections/", response_model=List[Section], responses={404: {"model": Message}})
async def get_sections(classroomId: int):
    response = supabase.table('Section').select('*').eq('classroomId', classroomId).execute()
    sections = []
    data = response.data
    for d in data:
        sections.append(d)
    return {'sections': sections}


@app.get("/grades/", response_model=List[Grade], responses={404: {"model": Message}})
async def get_grades(studentId: int = 0):
    r = supabase.table('Grade').select('score', 'taskId').eq('studentId', studentId).execute()
    data = r.data
    all = []
    for info in data:
        taskId = info['taskId']
        r1 = supabase.table('Task').select('id', 'taskType', 'taskTypeId').eq('id', taskId).execute()
        r2 = supabase.table(r1.data[0]['taskType']).select('*').eq('id', r1.data[0]['taskTypeId']).execute()
        combined = {'type': r1.data[0]['taskType'], 'name': r2.data[0]['name'], 'score': info['score'],
                    'maxScore': r2.data[0]['maxScore']}
        all.append(combined)
    return all

# ---------------------------POST Methods-------------------------------

@app.post("/quizzes/")
async def create_quiz(quiz: Quiz, server_id: int):
    list = {'title': quiz.title, 'points': quiz.points, 'startDate': quiz.start, 'dueDate': quiz.due, 'timeLimit': quiz.time, 'questions': quiz.questions}
    print(list)
    res = supabase.table("Quiz").insert(list).execute()
    print(res)
    response = await get_classroom_id(server_id)
    classroom_id = response['id']
    response = await get_sections(classroom_id)
    print("Classroom Sections: ", response)
    print("Quiz Sections: ", quiz.sections)

    for section in quiz.sections:
        response = supabase.table("Section").select('id').eq('name', section).execute()
        section_id = response.data[0]['id']
        quiz_id = res.data[0]['id']
        list = {'sectionId': section_id, 'taskTypeId': quiz_id, 'taskType': "Quiz"}
        supabase.table("Task").insert(list).execute()

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
