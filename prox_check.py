import concurrent.futures, requests


def test(p):
	try:
		r= requests.get("https://oceanofpdf.com", proxies ={
			"http": "socks5://"+p,
			"https": "socks5://"+p
			}, timeout=10, verify=False, headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"})
		return r.text!= "75.186.28.218"
	except Exception as e:
		print(e)
		return False
def workMe(p):
	if test(p):
		f = open("proxies2.txt", "a")
		f.write(p+"\n")
		f.close()

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
	f = open("rawP.txt", "r")
	lines = f.read().split("\n")
	f.close()
	for line in lines:
		executor.submit(workMe, (line))
