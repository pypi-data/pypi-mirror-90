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

	def referencial_name(self):
		referencial_name = None

		if self.name:
			if self.official_color:
				referencial_name = f"""{self.name}: {self.official_color}"""
			elif len(self.colors) > 0:
				referencial_name = f"""{self.name} ({', '.join(self.colors)})"""
		elif self.official_color:
			referencial_name = self.official_color
		elif len(self.colors) > 0:
			referencial_name = ', '.join(self.colors)
		elif self.has_matte:
			referencial_name = 'matte'
		elif self.has_transparency:
			referencial_name = 'transparency'
		elif self.has_gloss:
			referencial_name = 'gloss'

		if referencial_name is None:
			raise Exception()
		
		return referencial_name

	@classmethod
	def get_by_id(cls, platform_edition_id):
		return cls.registry.get(platform_edition_id)

	@classmethod
	def get_all(cls):
		return cls.registry.values()
