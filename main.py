# Main file for creating audiobooks


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



import pdf2image, os, sys

import time, threading

from ibm import Imbtts, wrap, Voices
import PyPDF2, string
import subprocess
import pytesseract

from concurrent.futures import ThreadPoolExecutor
# from proxymanager import ProxyManager

EDGE_TTS_VOICE = "en-GB-RyanNeural"




corrections = lambda x: x.replace("chapter", "chapter ").replace("<", "").replace(">", "").replace("CHAPTER", "CHAPTER ").replace("OceanofPDF.com", "").replace("OceanofPDF .com", "").replace("OceanofPDF", "").replace("«", "").replace("»", "").replace("ﬀ", "").replace("www.freeclassicebooks.com", "").replace("wikileak", "wiki leak").replace("cypherpunk", 'cypher punk').replace("cryptome", "crypto me").replace("blacknet", "black net").replace("mixnetwork", "mix network").replace("electroniccommunications", "electronic communications").replace("theonetime", "the one time").replace("siprnet", "sipr net").replace("Goldenagato mp4directs.com", "").replace("Goldenagato | mp4directs.com", "").replace("Goldenagato", "").replace("mp4directs.com", "")


outputF = "output.avi"

OUT_CROP_PAGES = "crop/"
OUT_UNCROP_PAGES = "uncrop/"
OUT_VIDEO_PAGES = "videos/"
SPLITS = "splits"

doFiles = True
if len(sys.argv) != 1:
	if sys.argv[1].startswith("+"):
		nm = sys.argv[1][1:]
		outputF ='"' + nm +".avi\""
		try: os.mkdir(os.path.join("books", nm))
		except FileExistsError: pass

		OUT_CROP_PAGES, OUT_UNCROP_PAGES, OUT_VIDEO_PAGES = [os.path.join("books", nm, f) for f in (OUT_CROP_PAGES, OUT_UNCROP_PAGES, OUT_VIDEO_PAGES)]

		sys.argv.pop(1)
		doFiles=False
else:
	print("""
								(* is commonly used commands, - is less common commands)
python main.py test-tts         - Run test of voice with ibm tts
python main.py get-pages        * Get pngs from pdf
python main.py page-ocr         * Get text from pytesseract instead of pdf
python main.py pdf-ext          * Extract text from the pdf file
python main.py tts              * tts the text using the new microsoft edge tts
python main.py img-fix          - Add "image" to 0 len txt files
python main.py plot             * Creates plot of audio size / text size
python main.py cat              * Creates video files
python main.py tts_old          - tts the text using the old ibm tts
python main.py fixt             - Fixes words stuck together
python main.py bad-word-find    - Tells you all the words not in the dictionary
python main.py fix-pgn          - Removes page numbers
python main.py fix-chapter      - Add "chapter" to pages that start with a number followed by a new line
python main.py no-caps          - Lowercase all text


python main.py +"Name of book" fix-pgn - Custom book name
""")
	exit()



if doFiles:
	try: os.mkdir("files")
	except FileExistsError: pass
	OUT_CROP_PAGES, OUT_UNCROP_PAGES, OUT_VIDEO_PAGES = [os.path.join("files", f) for f in (OUT_CROP_PAGES, OUT_UNCROP_PAGES, OUT_VIDEO_PAGES)]


try: os.mkdir("/tmp/vocalLoco")
except FileExistsError: pass
try: os.mkdir(OUT_CROP_PAGES)
except FileExistsError: pass
try: os.mkdir(OUT_UNCROP_PAGES)
except FileExistsError: pass
try: os.mkdir(OUT_VIDEO_PAGES)
except FileExistsError: pass
# try: os.mkdir(SPLITS)
# except FileExistsError: pass


def fixProxDict(p):
	p["http"]=p["http"].replace("http", "socks5")
	p["https"]=p["https"].replace("https", "socks5")


def strip_non_ascii(strr):
	''' Returns the string without non ASCII characters'''
	stripped = (c for c in strr if c in string.ascii_letters)
	return ''.join(stripped)


voice = Voices.michael_expressive


ibb = None
def get(f):

	ibb = Imbtts()
	
	t = time.time()

	while True:
		try:
			f = os.path.join(OUT_CROP_PAGES, f)
			f2 = f+".mp3"
			print(f)
			f4 = open(f, 'r')
			size = ibb.download(ibb.chunck(wrap( corrections( f4.read() ) )), f2, voice)
			f4.close()
			break
		except Exception as e:
			print(e)
			while True:
				try:
					ibb = Imbtts()
					break
				except: time.sleep(3)


	print(time.time()-t)

if len(sys.argv) == 2:
	if sys.argv[-1] == "test-tts":
		# ibb = Imbtts()
		# ibb.download(ibb.chunck(wrap( "This is some example text of how the book might sound. I hope is sounds well! If not I would be mad. How does it sound?" )), "example.mp3", voice)
		text = "This is some example text of how the book might sound. I hope is sounds well! If not I would be mad. How does it sound?"
		os.system(f'edge-tts --file "{text}" -v {EDGE_TTS_VOICE} > example.mp3')

	elif sys.argv[-1] == "get-pages":
		pdf2image.convert_from_path('target/uncrop.pdf', output_folder=OUT_UNCROP_PAGES, fmt="png", output_file="", use_cropbox=True, thread_count=10)
		pdf2image.convert_from_path('target/crop.pdf', output_folder=OUT_CROP_PAGES, fmt="png", output_file="", use_cropbox=True, thread_count=10)

	elif sys.argv[-1] == "page-ocr":

		for f in os.listdir(OUT_CROP_PAGES):
			if not f.endswith(".txt"):
				f = os.path.join(OUT_CROP_PAGES, f)
				f2 = f+".txt"
				f2 = open(f2, "w")
				while True:
					try:
						v = corrections(pytesseract.image_to_string(f, timeout=5))
						f2.write(v)
						break
					except Exception as e:
						print(e, "on", f)
				f2.close()
	elif sys.argv[-1] == "pdf-ext":
		# ld = os.listdir(OUT_CROP_PAGES)



		# pdfReader = PyPDF2.PdfReader("target/crop.pdf")
		# i = 1
		# for pg in pdfReader.pages:
		# 	v = [f for f in ld if f.endswith(".png")]
		# 	v = [f for f in v if int(f.split("-")[-1].split(".png")[0]) == i ]
		# 	if len(v) != 0:
		# 		f2 = open(os.path.join(OUT_CROP_PAGES, v[0]+".txt"), "w")
		# 		f2.write(pg.extract_text())
		# 		f2.close()
		# 	else:
		# 		print(f"Error of {v} on {i}")
		# 	i+=1
		ld = os.listdir(OUT_CROP_PAGES)



		pdfReader = PyPDF2.PdfReader("target/crop.pdf")
		i = 1
		for pg in pdfReader.pages:
			v = [f for f in ld if f.endswith(".png")]
			v = [f for f in v if int(f.split("-")[-1].split(".png")[0]) == i ]
			if len(v) != 0:

				nm = os.path.join(OUT_CROP_PAGES, v[0]+'.txt')
				os.system(f"pdftotext -f {i} -cropbox -l {i} target/crop.pdf && mv target/crop.txt \"{nm}\"")
				f = open(nm, "r")
				r = corrections(f.read()).strip()
				f.close()
				f = open(nm, "w")
				f.write(r)
				f.close()
			else:
				print(f"Error of {v} on {i}")
			i+=1


	elif sys.argv[-1] == "tts":
		if __name__ == "__main__":
			def tmp(text, outpath):
				f = open(text, "r")
				x = f.read().replace("\n", " ").replace("  ", " ")
				f.close()
				f = open(text, "w")
				f.write(x)
				f.close()
				p=1
				while p != 0 and p != 2:
					p=os.system(f'edge-tts --file "{text}" -v {EDGE_TTS_VOICE} > "{outpath}"')




			with ThreadPoolExecutor(max_workers=20) as exe:
				for i, f in enumerate(os.listdir(OUT_CROP_PAGES)):
					mp3 = os.path.join(OUT_CROP_PAGES, f) + ".mp3"
					if f.endswith(".txt") and not os.path.exists( mp3 ) :
						txtPath = os.path.join(OUT_CROP_PAGES, f)
						exe.submit(tmp, txtPath, mp3)
					# tmp(txtPath, mp3)
						# o+=1
				# if not any(( os.path.exists(os.path.join(OUT_CROP_PAGES,u)+ ".mp3") for u in  os.listdir(OUT_CROP_PAGES) )):
				# 	break
	elif sys.argv[-1] == "tts_old":
		speech_threads = []
		ibb = Imbtts()
		if __name__ == "__main__":
			for i, f in enumerate(os.listdir(OUT_CROP_PAGES)):
				if f.endswith(".txt") and not os.path.exists( os.path.join(OUT_CROP_PAGES, f) + ".mp3") :
					while len(speech_threads) == 3:
						for ii, t in enumerate(speech_threads):
							if not t.is_alive():
								speech_threads.pop(ii)
								break
						time.sleep(1)
					else:
						t = threading.Thread(target=get, args=(f, ))
						t.start()
						speech_threads.append(t)
	elif sys.argv[-1] == "cat":
		if __name__ == "__main__":
			for i, f in enumerate(sorted(os.listdir(OUT_CROP_PAGES))):
				if f.endswith(".mp3"):
					audio = os.path.join(OUT_CROP_PAGES, f)
					image = os.path.join(OUT_UNCROP_PAGES, f.replace(".txt.mp3", ""))


					out = os.path.join(OUT_VIDEO_PAGES, str(int(f.split("-")[1].split(".")[0])).zfill(5)  +".avi")

					if not os.path.exists(out):
						# os.system(f"ffmpeg -y -i  \"{image}\" -i \"{audio}\" -c:v libx264 -tune stillimage -c:a copy \"{out}\"")
						os.system(f"ffmpeg -i \"{image}\" -i \"{audio}\" -c:a copy  \"{out}\"")


			slist = sorted(os.listdir(OUT_VIDEO_PAGES))
			print(slist)

			tcount = 0.0
			fcount = 0
			f = open("cat", "w")
			for fn in slist:
				print(fn)

				z=float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", os.path.join(OUT_VIDEO_PAGES, fn)]).decode("utf-8").replace("\n", ""))
				if tcount + z > 60*60*9.75:
					f.close()
					os.system("ffmpeg -y -f concat -safe 0 -i cat -c:a  copy "+str(fcount)+outputF.replace("'", ""))
					fcount+=1
					tcount=0.0
					f = open("cat", "w")

				tcount+=z
				f.write(f"file '{OUT_VIDEO_PAGES}/{fn}'\n")


			f.close()

			os.system("ffmpeg -y -f concat -safe 0 -i cat -c:a  copy "+str(fcount)+outputF.replace("'", ""))
		else:
			print("No correct args")
	elif sys.argv[-1] == "plot":
		audio = sorted([os.path.join(OUT_CROP_PAGES, f) for f in os.listdir(OUT_CROP_PAGES) if f.endswith(".mp3")])
		txt = [f.replace(".mp3", "") for f in audio]

		nums = [int(f.split("-")[-1].split(".png")[0]) for f in txt]

		audio = [os.path.getsize(a) for a in audio]
		txt = [os.path.getsize(t) for t in txt]

		ratio = [(a/txt[i] if txt[i] != 0 and a != 45 else 999)  for i, a in enumerate(audio)]
		

		import matplotlib.pyplot as plt
		# print([nums, ratio])
		plt.plot(nums, ratio)
		plt.show()
	elif sys.argv[-1] == "fix-plot":
		minn = int(input("Min: "))
		audio = sorted([os.path.join(OUT_CROP_PAGES, f) for f in os.listdir(OUT_CROP_PAGES) if f.endswith(".mp3")])
		txt = [f.replace(".mp3", "") for f in audio]

		audio2 = [os.path.getsize(a) for a in audio]
		txt = [os.path.getsize(t) for t in txt]
		for i in range(len(txt)):
			a, t = audio2[i], txt[i]

			rat = (a/t if t != 0 and a != 45 else 999)
			if rat < minn:
				os.system(f"rm \"{audio[i]}\"")

	elif sys.argv[-1] == "fixt":
		f = open("eng.txt", "r")
		words = [w for w in f.read().split("\n") if len(w) != 0]
		f.close()

		for i, f in enumerate(sorted(os.listdir(OUT_CROP_PAGES))):
			if f.endswith(".txt"):
				print(f)
				fnn = os.path.join(OUT_CROP_PAGES, f)
				f = open(fnn, "r")
				text = f.read()
				f.close()
				text=text.replace(",", ",").replace("’", "'").replace("\n", " ").replace(" '", "'").replace(" ,", ",").replace(" .", ".").replace("’ ", "'").replace("’ ", "'")

				while "  " in text:
					text=text.replace('  ', ' ')

				li = []
				while True:
					ws = text.split(" ")
					for i, w in enumerate(ws):
						if i+1 != len(ws):
							rw = w.replace(".", "").replace(",", "").replace("'", "").replace("\"", "").replace("`", "").replace("’", "").replace("“", "")
							rww = ws[i+1].replace(".", "").replace(",", "").replace("'", "").replace("\"", "").replace("`", "").replace("’", "").replace("“", "").replace("'s", "")

							cc=(rw.lower() + rww.lower() ).strip()
							if cc in words and not cc in li:
								print(rw.lower() + rww.lower())
								text = text.replace(rw+" "+rww, rw+rww)

								li.append(cc)
								if len(li) == 5:
									li.pop(0)
								break
					else:
						break
				f = open(fnn, "w")
				f.write(text)
				f.close()
	elif sys.argv[-1] == "bad-word-find":
		f = open("eng.txt", "r")
		words = [w.lower() for w in f.read().split("\n") if len(w) != 0]
		f.close()
		for i, f in enumerate(sorted(os.listdir(OUT_CROP_PAGES))):
			if f.endswith(".txt"):
				f2 = open(os.path.join(OUT_CROP_PAGES, f), "r")
				data = f2.read()
				f2.close()
				unk = {}
				for w in data.split(" "):
					w = strip_non_ascii(w.lower()).strip()
					if not w in words and len(w) != 0: 
						unk[w] = unk.get(w, 0)+1
				print([f for f in sorted(unk.items(), key=lambda k: k[-1]) if f[-1] != 1])

	elif sys.argv[-1] == "img-fix":
		for i, f in enumerate(sorted(os.listdir(OUT_CROP_PAGES))):
			if f.endswith(".txt"):
				f2 = open(os.path.join(OUT_CROP_PAGES, f), "r")
				data = f2.read().strip()
				f2.close()
				if len(data) < 4:
					f2 = open(os.path.join(OUT_CROP_PAGES, f), "w")
					f2.write("image")
					f2.close()
	elif sys.argv[-1] == "fix-pgn":
		for i, f in enumerate(sorted(os.listdir(OUT_CROP_PAGES))):
			if f.endswith(".txt"):

				f2 = open(os.path.join(OUT_CROP_PAGES, f), "r")
				data = f2.read()
				f2.close()
				try:
					print(int(data.split("\n")[-1]), f)
					data = "\n".join(data.split("\n")[:-1])
				except:pass
				f2 = open(os.path.join(OUT_CROP_PAGES, f), "w")
				f2.write(data)
				f2.close()
					# exit(1)
	elif sys.argv[-1] == "fix-chapter":
		for i, f in enumerate(sorted(os.listdir(OUT_CROP_PAGES))):
			if f.endswith(".txt"):


				f2 = open(os.path.join(OUT_CROP_PAGES, f), "r")
				data = f2.read()
				f2.close()
				try:
					i=int(data.split("\n")[0])
					print(i, f)
					data="chapter "+data
				except:
					pass


				f2 = open(os.path.join(OUT_CROP_PAGES, f), "w")
				f2.write(data)
				f2.close()
	elif sys.argv[-1] == "no-caps":
		for i, f in enumerate(sorted(os.listdir(OUT_CROP_PAGES))):
			if f.endswith(".txt"):
				f2 = open(os.path.join(OUT_CROP_PAGES, f), "r")
				data = f2.read()
				f2.close()

				f2 = open(os.path.join(OUT_CROP_PAGES, f), "w")
				f2.write(data.lower())
				f2.close()

	elif sys.argv[-1] == "fix-audio-with-bad-c":
		for i, f in enumerate(sorted(os.listdir(OUT_CROP_PAGES))):
			if f.endswith(".mp3"):
				path = os.path.join(OUT_CROP_PAGES, f)

				if os.path.getsize(path) == 6854:
					print(os.path.getsize(path))
					f = open(path.replace(".mp3", ""), "r")
					r = f.read().replace("<", "").replace(">", "")
					f.close()

					f = open(path.replace(".mp3", ""), "w")
					f.write(r)
					f.close()
					os.system(f"rm \"{path}\"")
	elif sys.argv[-1] == "thumb":
		if 0==os.system(f'convert -resize 20% "{os.path.join(OUT_CROP_PAGES, "0001-001.png")}" "{OUT_CROP_PAGES}"{os.path.join("..", "thumb.png")}'):
			print("Thumbnail created")
		else:
			print("Thumbnail error, try sudo apt install imagemagick or sudo pacman -S imagemagick ")

elif len(sys.argv) == 3:
	if sys.argv[1] == "splits":
		sps = int(sys.argv[2])
		for i in range(sps):
			os.mkdir(os.path.join(SPLITS, str(i)))
		for i, f in enumerate(os.listdir(OUT_CROP_PAGES)):
			if f.endswith(".txt") and not os.path.exists( os.path.join(OUT_CROP_PAGES, f) + ".mp3") :
				os.system(f"cp \"{os.path.join(OUT_CROP_PAGES, f)}\" \"{os.path.join(SPLITS, str(i%sps), f)}\"")


else:	
	print("No correct args")
			


