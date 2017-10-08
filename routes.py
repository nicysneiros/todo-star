from apistar import Include, Route
from apistar.handlers import docs_urls, static_urls
from views import welcome, create_todo_list, list_todo_lists, add_todo_item


routes = [
    Route('/', 'GET', welcome),
    Route('/create_todo_list', 'POST', create_todo_list),
    Route('/list_todo_lists', 'GET', list_todo_lists),
    Route('/add_todo_item', 'POST', add_todo_item),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]