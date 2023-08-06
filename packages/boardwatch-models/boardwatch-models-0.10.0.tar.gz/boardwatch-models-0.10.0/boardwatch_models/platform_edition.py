class PlatformEdition():
	registry = {}

	def __init__(self, id, name, official_color, has_matte, has_transparency, has_gloss, note, image_url):
		self.id = id
		self.name = name
		self.official_color = official_color
		self.has_matte = has_matte
		self.has_transparency = has_transparency
		self.has_gloss = has_gloss
		self.note = note
		self.image_url = image_url
		self.colors = list()

	def add_to_registry(self):
		PlatformEdition.registry[self.id] = self

	@classmethod
	def get_by_id(cls, platform_edition_id):
		return cls.registry[platform_edition_id]

	@classmethod
	def get_all(cls):
		return cls.registry.values()
