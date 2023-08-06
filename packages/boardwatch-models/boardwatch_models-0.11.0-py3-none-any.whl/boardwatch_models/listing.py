class Listing():
	registry = {}

	def __init__(self, id, native_id, title, body, price, url, date_posted, date_scraped):
		self.id = id
		self.native_id = native_id
		self.title = title
		self.body = body
		self.price = price
		self.url = url
		self.date_posted = date_posted
		self.date_scraped = date_scraped

	def add_to_registry(self):
		Listing.registry[self.id] = self

	@classmethod
	def get_by_id(cls, listing_id):
		return cls.registry[listing_id]

	@classmethod
	def get_all(cls):
		return cls.registry.values()
