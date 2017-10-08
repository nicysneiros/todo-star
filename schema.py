from apistar import typesystem


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