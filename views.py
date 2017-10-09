import datetime
import json

from apistar import http, annotate
from apistar.backends.sqlalchemy_backend import Session
from apistar.interfaces import Auth

from models import TodoList, TodoItem, User
from schema import TodoListType, TodoItemType, UserType
from authentication import BasicAuthentication


def welcome(name=None):
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}


@annotate(authentication=[BasicAuthentication()])
def create_todo_list(session: Session, todo_list: TodoListType, auth:Auth):
	user = session.query(User).filter_by(username=auth.get_user_id()).first()
	if user:
		new_todo_list = TodoList(
			title=todo_list.get('title'), 
			user_id=user.id
		)
		session.add(new_todo_list)
		session.flush()

		user.todo_lists.append(new_todo_list)
		session.commit()
		return http.Response({'id': new_todo_list.id}, status=201)
	return http.Response({"message": "User not found"}, status=400)


@annotate(authentication=[BasicAuthentication()])
def list_todo_lists(session:Session, auth:Auth):
	user = session.query(User).filter_by(username=auth.get_user_id()).first()
	if user:
		queryset = session.query(TodoList).filter_by(user_id=user.id)
		return [
			{
				'id': todo_list.id, 
				'title': todo_list.title,
				'user_id' : todo_list.user_id,
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
	return http.Response({"id": "User not found"}, status=400)

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


def create_user(session: Session, user: UserType):
	user = User(
		username=user.get('username'), 
		password=user.get('password')
	)
	session.add(user)
	session.flush()
	return http.Response({'id': user.id}, status=201)