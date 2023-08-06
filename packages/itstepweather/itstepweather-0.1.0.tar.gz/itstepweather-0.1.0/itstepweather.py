import requests

class Weather:
	def __init__(self, city, API):
		self.API = API
		self.city = city
		self.data = {}
		try:
			res = requests.get("http://api.openweathermap.org/data/2.5/find", params={'q': self.city, 'type': 'like', 'units': 'metric', 'APPID': self.API})
			self.data = res.json()['list'][0]['main']
		except Exception as e:
			print("Неправильно выбран город или API: ", e)
	def get_data(self):
		res = requests.get("http://api.openweathermap.org/data/2.5/find", params={'q': self.city, 'type': 'like', 'units': 'metric', 'APPID': self.API})
		self.data = res.json()['list'][0]['main']
		return self.data