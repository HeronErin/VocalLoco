# Flask web server for retrieving tts'ed files from the cloud


from flask import Flask, jsonify
from flask import request
import os, base64

app = Flask(__name__)


corrections = lambda x: x.replace("chapter", "chapter ").replace("<", "").replace(">", "").replace("CHAPTER", "CHAPTER ").replace("OceanofPDF.com", "").replace("OceanofPDF .com", "").replace("OceanofPDF", "").replace("«", "").replace("»", "").replace("ﬀ", "").replace("www.freeclassicebooks.com", "").replace("wikileak", "wiki leak").replace("cypherpunk", 'cypher punk').replace("cryptome", "crypto me").replace("blacknet", "black net").replace("mixnetwork", "mix network").replace("electroniccommunications", "electronic communications").replace("theonetime", "the one time").replace("siprnet", "sipr net")

txts = []
for bk in os.listdir("books"):
	txts += [b for b in [os.path.join("books", bk, "crop", f) for f in os.listdir(os.path.join("books", bk, "crop"))]  if b.endswith(".txt") and not os.path.exists(b.replace("books", "rcv").replace("crop/", "")+".wav")]
txts = list(sorted(txts))

# print(txts[0])
# exit()
@app.route('/submit', methods = ['POST'])
def aaaaaaa():
	if request.method == 'POST':
		file = request.files['file']
		nm = request.headers.get('Name')
		print(nm)
		nm = base64.urlsafe_b64decode(nm.encode("utf-8")).decode("utf-8")
		nm = "rcv/"+os.sep.join(nm.split(os.sep)[1:]).replace("/crop", "")+".wav"

		for f in ("rcv", os.sep.join(nm.split(os.sep)[:2]) ):
			try: os.mkdir(f)
			except FileExistsError: pass
		file.save(nm)
	return ""
@app.route("/next/")
def bbbbb():
	try:
		v = txts.pop(0)
		while os.path.exists(v.replace("books", "rcv").replace("crop/", "")+".wav"):
			v = txts.pop(0)
			
		f = open(v, "r")
		rt = base64.b64encode(corrections( f.read() ).encode("utf-8")).decode("utf-8")
		f.close()
		return jsonify([rt, v])
	except IndexError as e:
		print(e)
		return jsonify([])
if __name__ == "__main__":
	app.run()
#curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@rcv.py" http://127.0.0.1:5000/submit
