import datetime
import json
from models import TodoList, TodoItem
from schema import TodoListType, TodoItemType
from apistar import http
from apistar.backends.sqlalchemy_backend import Session


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