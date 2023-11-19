import os

a = input("file: ").replace("'", "").strip()
# print(a)
# exit()
os.system(f"cp \"{a}\" target/crop.pdf")
os.system(f"cp \"{a}\" target/uncrop.pdf")

name = input("Name: ")

doimg = input("Img? (y/n): ").lower() == "y"
desc = input("Description: ")	
au = input("Author: ")

cmd = f"python main.py +\"{name}\""
os.system(f"{cmd} get-pages")

if input("Next? (y/n): ").lower() == "y":


	os.system(f"{cmd} pdf-ext")
	if doimg:
		os.system(f"{cmd} img-fix")

	f = open(f"/home/void1/vocal_loco_pdf/books/{name}/crop/0001-001.png.txt", "w")
	f.write(f"{name} {desc} by {au}")
	f.close()