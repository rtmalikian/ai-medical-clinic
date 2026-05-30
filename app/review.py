from __future__ import annotations

from app.schemas import ReviewTask, WorkflowRunOutput

REVIEW_TASKS: dict[str, ReviewTask] = {}


def create_review_task(workflow_id: str, output: WorkflowRunOutput) -> ReviewTask:
    task = ReviewTask(
        workflow_id=workflow_id,
        run_id=output.run_id,
        title=f"Review {workflow_id} draft before action",
        artifact=output,
    )
    REVIEW_TASKS[task.id] = task
    return task


def list_review_tasks() -> list[ReviewTask]:
    return list(REVIEW_TASKS.values())


def update_review_task(task_id: str, status: str, note: str | None = None) -> ReviewTask | None:
    task = REVIEW_TASKS.get(task_id)
    if not task:
        return None
    task.status = status  # type: ignore[assignment]
    task.reviewer_note = note
    REVIEW_TASKS[task.id] = task
    return task
