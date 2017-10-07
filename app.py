import json
from apistar import Include, Route, http, typesystem
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls


todo_lists = []

class TodoList(typesystem.Object):
	properties = {
		'title': typesystem.string(max_length=100)
	}


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}


def create_todo_list(todo_list: TodoList):
	todo_lists.append(todo_list)
	return http.Response({}, status=201)


def list_todo_lists():
	return http.Response(todo_lists, status=200)


routes = [
    Route('/', 'GET', welcome),
    Route('/create_todo_list', 'POST', create_todo_list),
    Route('/list_todo_lists', 'GET', list_todo_lists),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
