import os

a = input("file: ").replace("'", "").strip()
cmd = f"python main.py +\"{a}\""

os.system(f"mv \"rcv/{a}/\"* \"books/{a}/crop\"")



os.system(f"{cmd} plot")
i = input("? ")
while i.lower() == "n":
	os.system(f"{cmd} fix-plot")
	os.system(f"{cmd} tts")

	os.system(f"{cmd} plot")

	i = input("? ")
os.system(f"{cmd} cat")