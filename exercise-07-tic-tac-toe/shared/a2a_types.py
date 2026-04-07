from __future__ import annotations
from typing import Any
from uuid import uuid4
from enum import Enum
from dataclasses import dataclass, field

class TaskState(str, Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Message:
    role: str
    parts: list[dict[str, Any]]


@dataclass
class Task:
    id: str
    message: Message


@dataclass
class RequestContext:
    task_id: str
    context_id: str
    message: Message
    current_task: Task | None = None


@dataclass
class TaskStatus:
    state: TaskState
    message: Message | None = None


@dataclass
class TaskStatusUpdateEvent:
    task_id: str
    context_id: str
    status: TaskStatus


@dataclass
class TaskArtifactUpdateEvent:
    task_id: str
    context_id: str
    artifact: dict[str, Any]


@dataclass
class EventQueue:
    events: list[Any] = field(default_factory=list)

    async def enqueue_event(self, event: Any) -> None:
        self.events.append(event)


def new_text_message(text: str, role: str = "user") -> Message:
    return Message(role=role, parts=[{"type": "text", "text": text}])


def new_agent_text_message(text: str) -> Message:
    return new_text_message(text=text, role="agent")


def new_task(message: Message) -> Task:
    return Task(id=str(uuid4()), message=message)


def new_text_artifact(name: str, text: str) -> dict[str, Any]:
    return {
        "type": "text_artifact",
        "name": name,
        "text": text,
    }
