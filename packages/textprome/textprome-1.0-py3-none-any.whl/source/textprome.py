from bs4 import BeautifulSoup as bs4
import requests, json

class TextProMe:
	def __init__(self):
		self.ses = requests.Session()
		self.headers = {
			"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
			"Accept": "*/*",
			"DNT" : "1"
		}
		self.ses.headers.update(self.headers)
		self.url = None
		self.inputparam = None
		self.token = None

	def setdata(self,settype,value):
		if settype == "url":
			self.url=value
		elif settype == "input":
			self.inputparam = value
		elif settype == "headers":
			self.headers = value

	def getandsettoken(self):
		r =  self.ses.get(self.url)
		html_bytes = r.text
		soup = bs4(html_bytes, 'lxml')
		self.token = soup.find('input', {'name':'token'})['value']

	def createimage(self):
		r =  self.ses.post(self.url, files = self.inputparam)
		html_bytes = r.text
		soup = bs4(html_bytes, 'lxml')
		result = soup.find('input', {'name':'share_link'})['value']
		try:
			result = result.split("-")
			result = result[0]
		except:
			pass
		return result

	def style_blackpink(self,text1):
		self.url = "https://textpro.me/create-blackpink-logo-style-online-1001.html"
		self.getandsettoken()
		self.inputparam = (
						('text[]', (None, text1)),
						('submit', (None, 'Go')),
						('token', (None, self.token)),
					)
		return self.createimage()

	def style_neon(self,text1):
		self.url = "https://textpro.me/neon-light-text-effect-online-882.html"
		self.getandsettoken()
		self.inputparam = (
						('text[]', (None, text1)),
						('submit', (None, 'Go')),
						('token', (None, self.token)),
					)
		return self.createimage()

	def style_thunder(self,text1):
		self.url = "https://textpro.me/thunder-text-effect-online-881.html"
		self.getandsettoken()
		self.inputparam = (
						('text[]', (None, text1)),
						('submit', (None, 'Go')),
						('token', (None, self.token)),
					)
		return self.createimage()

	def style_tiktok_glitch(self,text1,text2):
		self.url = "https://textpro.me/create-glitch-text-effect-style-tik-tok-983.html"
		self.getandsettoken()
		self.inputparam = (
						('text[]', (None, text1)),
						('text[]', (None, text2)),
						('submit', (None, 'Go')),
						('token', (None, self.token)),
					)
		return self.createimage()

	def style_pornhub_logo(self,text1,text2):
		self.url = "https://textpro.me/pornhub-style-logo-online-generator-free-977.html"
		self.getandsettoken()
		self.inputparam = (
						('text[]', (None, text1)),
						('text[]', (None, text2)),
						('submit', (None, 'Go')),
						('token', (None, self.token)),
					)
		return self.createimage()


'''Example :

	textpro = TextProMe()
	print(textpro.style_pornhub_logo("Minato", "Aqua"))
'''
