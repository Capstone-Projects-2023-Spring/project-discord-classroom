from typing import List, Any
from pydantic import BaseModel


class Quiz(BaseModel):
    title: str
    points: float
    start: str
    due: str
    time: int
    questions: str
    classroomId: int
    channelId: int


class Question(BaseModel):
    question: str
    answer: str
    wrong: List[str]
    points: float


class Discussion(BaseModel):
    title: str
    points: int
    start: str
    due: str
    channelId: int
    classroomId: int

class Assignment(BaseModel):
    title: str
    start: str
    due: str
    points: int
    classroomId: int
    channelId: int


class Grade(BaseModel):
    graderId: int
    taskId: int
    studentId: int
    score: int