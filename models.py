from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

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