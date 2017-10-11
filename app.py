from apistar.backends.sqlalchemy_backend import commands, components
from apistar.frameworks.wsgi import WSGIApp as App

from authentication import BasicAuthentication

from models import Base

from routes import routes


settings = {
    "DATABASE": {
        "URL": "sqlite:///todo_list.db",
        "METADATA": Base.metadata
    },
    "AUTHENTICATION": [BasicAuthentication()]
}


app = App(
    routes=routes,
    settings=settings,
    commands=commands,
    components=components
)


if __name__ == '__main__':
    app.main()
