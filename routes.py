from apistar import Include, Route
from apistar.handlers import docs_urls, static_urls

from views import (
    add_todo_item, create_todo_list,
    create_user, list_todo_lists, welcome
)


routes = [
    Route('/', 'GET', welcome),
    Route('/create_todo_list', 'POST', create_todo_list),
    Route('/list_todo_lists', 'GET', list_todo_lists),
    Route('/add_todo_item', 'POST', add_todo_item),
    Route('/create_user', 'POST', create_user),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
