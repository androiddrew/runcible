from typing import List
from molten import Route, Include, HTTP_201, HTTP_202, HTTPError, HTTP_404, annotate

from runcible import APIResponse
from runcible.error import EntityNotFound
from .model import Todo
from .manager import TodoManager


def list_todos(todo_manager: TodoManager) -> List[Todo]:
    """Lists all global Todos"""
    return todo_manager.get_todos()


def create_todo(todo: Todo, todo_manager: TodoManager) -> Todo:
    """Creates a new global Todo"""
    _todo = todo_manager.create_todo(todo)
    headers = {"Location": _todo.href}
    return HTTP_201, _todo, headers


@annotate(openapi_param_todo_id_description="The id of an existing Todo")
def delete_todo(todo_id: int, todo_manager: TodoManager) -> APIResponse:
    """Deletes a global Todo"""
    todo_manager.delete_todo(todo_id)
    return (
        HTTP_202,
        APIResponse(status=202, message=f"Delete request for todo: {todo_id} accepted"),
    )


@annotate(openapi_param_todo_id_description="The id of an existing Todo")
def get_todo_by_id(todo_id: int, todo_manager: TodoManager) -> Todo:
    """Retrieves a Todo by id"""
    try:
        _todo = todo_manager.get_todo_by_id(todo_id)
    except EntityNotFound as err:
        raise HTTPError(HTTP_404, APIResponse(status=404, message=err.message))
    return _todo


@annotate(openapi_param_todo_id_description="The id of an existing Todo")
def update_todo(todo_id: int, todo: Todo, todo_manager: TodoManager) -> Todo:
    """Updates a Todo item"""
    return todo_manager.update_todo(todo_id, todo)


todo_routes = Include(
    "/todos",
    [
        Route("", list_todos, method="GET"),
        Route("", create_todo, method="POST"),
        Route("/{todo_id}", delete_todo, method="DELETE"),
        Route("/{todo_id}", get_todo_by_id, method="GET"),
        Route("/{todo_id}", update_todo, method="PATCH"),
    ],
)
