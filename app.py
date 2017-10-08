import datetime
import json
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from apistar import Include, Route, http, typesystem
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar.backends.sqlalchemy_backend import Session, commands, components

Base = declarative_base()

class TodoList(Base):
	__tablename__ = "TodoList"
	id = Column(Integer, primary_key=True)
	title = Column(String)
	itens = relationship("TodoItem", back_populates="todo_list")


class TodoItem(Base):
	__tablename__ = "TodoItem"
	id = Column(Integer, primary_key=True)
	description = Column(String)
	deadline = Column(DateTime)
	is_done = Column(Boolean)
	todo_list_id = Column(Integer, ForeignKey("TodoList.id"))
	todo_list = relationship("TodoList", back_populates="itens")


class TodoListType(typesystem.Object):
	properties = {
		'title': typesystem.string(
			max_length=100,
			description="A title for your TODO list"
		)
	}


class TodoItemType(typesystem.Object):
	properties = {
		'description': typesystem.string(description="Your TODO item description"),
		'deadline': typesystem.string(
			description="A deadline for your item",
			pattern=r'^\d{2}/\d{2}/\d{4}$'
		),
		'todo_list_id': typesystem.Integer
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


def list_todo_lists(session:Session):
	queryset = session.query(TodoList).all()
	return [
		{
			'id': todo_list.id, 
			'title': todo_list.title, 
			'itens': [
				{
					'description': item.description,
					'deadline': item.deadline.strftime('%d/%m/%Y'),
					'is_done': item.is_done
				}
				for item in todo_list.itens
			]
		}
		for todo_list in queryset
	]


def add_todo_item(session: Session, todo_item: TodoItemType):
	todo_list = session.query(TodoList).get(todo_item.get('todo_list_id'))
	if todo_list:
		item = TodoItem(
			description=todo_item.get('description'),
			deadline=datetime.datetime.strptime(todo_item.get('deadline'), '%d/%m/%Y'),
			is_done=False,
			todo_list_id=todo_item.get('todo_list_id')
		)
		session.add(item)
		session.flush()
		todo_list.itens.append(item)
		session.commit()
		return http.Response({'id': item.id}, status=201)
	return http.Response({'message': 'TODO List does not exists'}, status=400)


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
    Route('/add_todo_item', 'POST', add_todo_item),
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
