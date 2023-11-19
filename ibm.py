# Takes advantage of IBM's wattson tts demo allowing for free medium quality tts
import requests, string, random
from enum import Enum

s_pattern = string.ascii_lowercase + string.digits
s_chunck = lambda r: "".join([random.choice(s_pattern) for _ in range(r)])
def createId():
	return f"{s_chunck(8)}-{s_chunck(4)}-{s_chunck(4)}-{s_chunck(4)}-{s_chunck(12)}"


def wrap(x):
	return f'<prosody pitch="0%" rate="-0%">{x}</prosody>'

class Voices(Enum):
	allison_expressive = "en-US_AllisonExpressive"
	emma_expressive = "en-US_EmmaExpressive"
	lisa_expressive = "en-US_LisaExpressive"
	michael_expressive = "en-US_MichaelExpressive"
	allison = "en-US_AllisonV3Voice"
	emily ="en-US_EmilyV3Voice"
	henry ="en-US_HenryV3Voice"
	kevin ="en-US_KevinV3Voice"
	lisa ="en-US_LisaV3Voice"
	michael = "en-US_MichaelV3Voice"
	olivia ="en-US_OliviaV3Voice"

class Imbtts:
	def __init__(self, proxy=None):
		self.prox = proxy
		self.ses = requests.session()
		if proxy:
			self.ses.proxies.update(proxy)
		h = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
		self.ses.get("https://www.ibm.com/demos/live/tts-demo/self-service/home", headers=h)
	def chunck(self, ssml):
		headers = {
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
		    'Accept': 'application/json, text/plain, */*',
		    'Accept-Language': 'en-US,en;q=0.5',
		    'Content-Type': 'application/json;charset=utf-8',
		    'Origin': 'https://www.ibm.com',
		    'Connection': 'keep-alive',
		    'Referer': 'https://www.ibm.com/demos/live/tts-demo/self-service/home',
		    'Sec-Fetch-Dest': 'empty',
		    'Sec-Fetch-Mode': 'cors',
		}
		idd = createId()
		json_data = {
		    'ssmlText': ssml,
		    'sessionID': idd,
		}

		r =self.ses.post('https://www.ibm.com/demos/live/tts-demo/api/tts/store', headers=headers, json=json_data)
		return idd
	def download(self, idd, loc, voice = Voices.michael_expressive):
		headers = {
		    'authority': 'www.ibm.com',
		    'accept': '*/*',
		    'accept-language': 'en-US,en;q=0.5',
		    'range': 'bytes=0-',
		    'referer': 'https://www.ibm.com/demos/live/tts-demo/self-service/home',
		    'sec-fetch-dest': 'audio',
		    'sec-fetch-mode': 'no-cors',
		    'sec-fetch-site': 'same-origin',
		    'sec-gpc': '1',
		    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
		}

		f = open(loc, "wb")
		r = self.ses.get("https://www.ibm.com/demos/live/tts-demo/api/tts/newSynthesize?voice="+voice.value+"&id="+idd, headers=headers, timeout=60*7)
		c = r.content
		f.write(c)
		f.close()
		return len(c)