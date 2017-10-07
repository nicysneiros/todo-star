from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from apistar import Include, Route, http, typesystem
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.backends.sqlalchemy_backend import Session, commands, components

Base = declarative_base()

class TodoList(Base):
	__tablename__ = "TodoList"
	id = Column(Integer, primary_key=True)
	title = Column(String)


class TodoListType(typesystem.Object):
	properties = {
		'title': typesystem.string(
			max_length=100,
			description="A title for your TODO list"
		)
	}


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}


def create_todo_list(session: Session, todo_list: TodoListType):
	new_todo_list = TodoList(title=todo_list.get('title'))
	session.add(new_todo_list)
	session.flush()
	return http.Response({'id': new_todo_list.id}, status=201)


def list_todo_lists():
	return http.Response(todo_lists, status=200)


settings = {
    "DATABASE": {
        "URL": "sqlite:///todo_list.db",
        "METADATA": Base.metadata
    }
}


routes = [
    Route('/', 'GET', welcome),
    Route('/create_todo_list', 'POST', create_todo_list),
    Route('/list_todo_lists', 'GET', list_todo_lists),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(
	routes=routes, 
	settings=settings,
	commands=commands,
	components=components
)


if __name__ == '__main__':
    app.main()
