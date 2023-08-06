class Game():
	registry = {}

	def __init__(self, id, name, year_first_release, is_bootleg):
		self.id = id
		self.name = name
		self.year_first_release = year_first_release
		self.is_bootleg = is_bootleg

	def add_to_registry(self):
		Game.registry[self.id] = self

	@classmethod
	def get_by_id(cls, game_id):
		return cls.registry[game_id]

	@classmethod
	def get_all(cls):
		return cls.registry.values()
