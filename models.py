import bcrypt

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class TodoList(Base):
    __tablename__ = "TodoList"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    itens = relationship("TodoItem", back_populates="todo_list")
    user_id = Column(Integer, ForeignKey("User.id"))
    user = relationship("User", back_populates="todo_lists")


class TodoItem(Base):
    __tablename__ = "TodoItem"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    deadline = Column(DateTime)
    is_done = Column(Boolean)
    todo_list_id = Column(Integer, ForeignKey("TodoList.id"))
    todo_list = relationship("TodoList", back_populates="itens")


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    todo_lists = relationship("TodoList", back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt())

    def validate_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
