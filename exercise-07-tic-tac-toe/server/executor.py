from __future__ import annotations

from shared.a2a_types import (
    EventQueue,
    RequestContext,
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    new_agent_text_message,
    new_task,
    new_text_artifact,
)


class AgentExecutor:
    def __init__(self, agent) -> None:
        self.agent = agent

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        task = context.current_task or new_task(context.message)
        await event_queue.enqueue_event(task)

        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context.context_id,
                status=TaskStatus(
                    state=TaskState.WORKING,
                    message=new_agent_text_message("Processing request..."),
                ),
            )
        )

        try:
            self.agent.set_context(context)
            result = await self.agent.invoke()

            await event_queue.enqueue_event(
                TaskArtifactUpdateEvent(
                    task_id=context.task_id,
                    context_id=context.context_id,
                    artifact=new_text_artifact(name="result", text=result),
                )
            )
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=context.task_id,
                    context_id=context.context_id,
                    status=TaskStatus(state=TaskState.COMPLETED),
                )
            )
        except Exception as exc:
            await event_queue.enqueue_event(
                TaskArtifactUpdateEvent(
                    task_id=context.task_id,
                    context_id=context.context_id,
                    artifact=new_text_artifact(name="error", text=str(exc)),
                )
            )
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=context.task_id,
                    context_id=context.context_id,
                    status=TaskStatus(
                        state=TaskState.FAILED,
                        message=new_agent_text_message("Execution failed."),
                    ),
                )
            )
