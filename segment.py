# Script for ttsing on the cloud and sending it back the the main server (as tortoise_tts is slow but SUPER high quality)



# This program is free software; you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation; either 
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program;
# if not, see http://www.gnu.org/licenses/gpl-3.0


sc = "scripts/tortoise_tts.py"
import os, time, concurrent.futures, requests, base64, random




voice = "darknet_monotone"
def strip_non_ascii(string):
  ''' Returns the string without non ASCII characters'''
  stripped = (c for c in string if 0 < ord(c) < 127)
  return ''.join(stripped)


uuu = "2.tcp.ngrok.io:14769"

corrections = lambda x: x.replace("chapter", "chapter ").replace("<", "").replace(">", "").replace("CHAPTER", "CHAPTER ").replace("OceanofPDF.com", "").replace("OceanofPDF .com", "").replace("OceanofPDF", "").replace("«", "").replace("»", "").replace("ﬀ", "").replace("www.freeclassicebooks.com", "").replace("wikileak", "wiki leak").replace("cypherpunk", 'cypher punk').replace("cryptome", "crypto me").replace("blacknet", "black net").replace("mixnetwork", "mix network").replace("electroniccommunications", "electronic communications").replace("theonetime", "the one time").replace("siprnet", "sipr net")

az = os.path.join("/tmp/", str(random.randrange(0, 1_000_000)))
os.mkdir(az)
tfile = os.path.join(az, "t.txt")
afile = os.path.join(az, f"{voice}_combined.wav")

def get():

	

	while True:
		t = time.time()
		try:
			data, name = requests.get("http://"+uuu+"/next/").json()


			text = strip_non_ascii( corrections( base64.b64decode(data.encode("utf-8")).decode("utf-8") ) )
			f = open(tfile, "w")
			f.write(text)
			# f.write("hello")
			f.close()

			os.system(f'cat {tfile} | python "{sc}" --voice {voice} --preset ultra_fast -O "{az}"')
			os.system(f'(curl -s -i -X POST -H "Content-Type: multipart/form-data" -H "Name: {base64.urlsafe_b64encode(name.encode("utf-8")).decode("utf-8")}" -F "file=@{afile}" {uuu}/submit && rm "{az}"/*) &')
			print(name, time.time()-t)
		except ValueError as e:
			print(e)
			return
		except Exception as e:
			print(e)
			time.sleep(3)
	

if __name__ == "__main__":
	get()

