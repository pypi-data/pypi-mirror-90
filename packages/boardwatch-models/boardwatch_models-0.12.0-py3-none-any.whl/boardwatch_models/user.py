class User():
	registry = {}

	def __init__(self, id, public_id, username, email, password, created_at):
		self.id = id
		self.public_id = public_id
		self.username = username
		self.email = email
		self.password = password
		self.created_at = created_at

	def add_to_registry(self):
		User.registry[self.id] = self

	@classmethod
	def get_by_id(cls, user_id):
		return cls.registry.get(user_id)

	@classmethod
	def get_all(cls):
		return cls.registry.values()
