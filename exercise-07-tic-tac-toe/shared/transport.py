from __future__ import annotations

import json

from .a2a_types import (
    Message,
    RequestContext,
    Task,
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
)


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


def serialize_message(message: Message) -> dict[str, object]:
    return {
        "role": message.role,
        "parts": message.parts,
    }


def deserialize_message(payload: dict[str, object]) -> Message:
    return Message(
        role=str(payload["role"]),
        parts=list(payload["parts"]),
    )


def serialize_task(task: Task) -> dict[str, object]:
    return {
        "id": task.id,
        "message": serialize_message(task.message),
    }


def deserialize_task(payload: dict[str, object]) -> Task:
    return Task(
        id=str(payload["id"]),
        message=deserialize_message(dict(payload["message"])),
    )


def serialize_request(context: RequestContext) -> str:
    payload: dict[str, object] = {
        "task_id": context.task_id,
        "context_id": context.context_id,
        "message": serialize_message(context.message),
    }
    if context.current_task is not None:
        payload["current_task"] = serialize_task(context.current_task)
    return json.dumps(payload)


def deserialize_request(raw: str) -> RequestContext:
    payload = json.loads(raw)
    current_task_payload = payload.get("current_task")
    current_task = None
    if current_task_payload is not None:
        current_task = deserialize_task(dict(current_task_payload))

    return RequestContext(
        task_id=str(payload["task_id"]),
        context_id=str(payload["context_id"]),
        message=deserialize_message(dict(payload["message"])),
        current_task=current_task,
    )


def serialize_event(event: object) -> dict[str, object]:
    if isinstance(event, Task):
        return {
            "type": "task",
            "id": event.id,
            "message": serialize_message(event.message),
        }

    if isinstance(event, TaskStatusUpdateEvent):
        status_payload: dict[str, object] = {
            "state": event.status.state.value,
        }
        if event.status.message is not None:
            status_payload["message"] = serialize_message(event.status.message)

        return {
            "type": "status_update",
            "task_id": event.task_id,
            "context_id": event.context_id,
            "status": status_payload,
        }

    if isinstance(event, TaskArtifactUpdateEvent):
        return {
            "type": "artifact_update",
            "task_id": event.task_id,
            "context_id": event.context_id,
            "artifact": event.artifact,
        }

    raise TypeError(f"Unsupported event type: {type(event)!r}")


def deserialize_event(payload: dict[str, object]) -> object:
    event_type = payload["type"]

    if event_type == "task":
        return Task(
            id=str(payload["id"]),
            message=deserialize_message(dict(payload["message"])),
        )

    if event_type == "status_update":
        status_payload = dict(payload["status"])
        message_payload = status_payload.get("message")
        message = None
        if message_payload is not None:
            message = deserialize_message(dict(message_payload))

        return TaskStatusUpdateEvent(
            task_id=str(payload["task_id"]),
            context_id=str(payload["context_id"]),
            status=TaskStatus(
                state=TaskState(str(status_payload["state"])),
                message=message,
            ),
        )

    if event_type == "artifact_update":
        return TaskArtifactUpdateEvent(
            task_id=str(payload["task_id"]),
            context_id=str(payload["context_id"]),
            artifact=dict(payload["artifact"]),
        )

    raise ValueError(f"Unknown event type: {event_type}")


def serialize_events(events: list[object]) -> str:
    return json.dumps([serialize_event(event) for event in events])


def deserialize_events(raw: str) -> list[object]:
    payload = json.loads(raw)
    return [deserialize_event(dict(event)) for event in payload]
