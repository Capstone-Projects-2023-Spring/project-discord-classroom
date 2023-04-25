from pydantic import BaseModel
from typing import List, Optional


class Assignment(BaseModel):
    id: Optional[int] = None
    channelId: int
    points: int
    startDate: str
    dueDate: str
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
    attendance: Optional[int] = None

class Discussion(BaseModel):
    id: Optional[int] = None
    classroomId: int
    channelId: int
    title: str
    points: int
    startDate: str
    dueDate: str

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
    id: Optional[int] = None
    questions: str
    channelId: int
    title: str
    points: float
    startDate: str
    dueDate: str
    timeLimit: int
    classroomId: int

class Token(BaseModel):
    userId: int
    unique_id: str

class User(BaseModel):
    id: Optional[int] = None
    name: str
    discordId: int