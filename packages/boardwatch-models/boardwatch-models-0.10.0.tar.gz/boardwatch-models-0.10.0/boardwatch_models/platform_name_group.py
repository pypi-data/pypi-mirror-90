class PlatformNameGroup():
	registry = {}

	def __init__(self, id, name, description):
		self.id = id
		self.name = name
		self.description = description
		self.platforms = dict()

	def add_to_registry(self):
		PlatformNameGroup.registry[self.id] = self
		
	def add_platform(self, platform):
		if platform.id not in self.platforms:
			self.platforms[platform.id] = platform

	def get_all_platforms(self):
		return self.platforms.values()


	@classmethod
	def get_by_id(cls, platform_name_group_id):
		return cls.registry[platform_name_group_id]

	@classmethod
	def get_all(cls):
		return cls.registry.values()
