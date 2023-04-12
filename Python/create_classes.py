from typing import List, Any
from pydantic import BaseModel



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
    attendance: Optional[int] = None

class Discussion(BaseModel):
    classroomId: int
    channelId: int
    title: str
    points: int
    startDate: datetime.date
    dueDate: datetime.date

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
    questions: str
    channelId: int
    title: str
    points: float
    startDate: datetime.date
    dueDate: datetime.date
    timeLimit: int
    classroomId: int

class User(BaseModel):
    id: Optional[int] = None
    name: str
    discordId: int