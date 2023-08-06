import requests
class awesome(object):
	def __init__(self,url):
		self.request=requests.get(url)
	def test(self):
		return self.request
class Razberry:
	def __init__(self):
		self.Razberry={"hash":"784657ht7r6434784he08eidhnug747bd7wui89"}
	def random_hash(self):
		return self.Razberry
	def razberry():
		image=requests.get("https://media.discordapp.net/attachments/795757076600979456/796437238061727775/raspberry.jpg").content
		f=open("RAZZZZZZZZ.png","wb")
		f.write(image)
		f.close()