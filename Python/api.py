from fastapi import FastAPI
from supabase import create_client
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel
from typing import List

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
    if response.data:
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
async def get_sections(classroomId: int = 0):
    response = supabase.table('Section').select('*').eq('classroomId', classroomId).execute()
    sections = []
    data = response.data
    print("Data:", data)
    for d in data:
        sections.append(d)
    return sections


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
