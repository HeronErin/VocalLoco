# Vocal Loco

This is some python scripts I wrote for automatically converting PDFS to audiobooks (in the form of videos). There 
This tool is not user friendly and very clunky. But of you get it to work you are free to use it. 

## Dependencies:
	- Linux (or wsl)
	- FFmpeg (installed through apt or pacman)
	- Tesseract (installed through apt or pacman)
	- Pytesseract (installed through pip)
	- Requests (installed through pip)
	- edge-tts (installed through pip)
	- PyPDF2 (installed through pip)
	- pdf2image (installed through pip)

## How to use:

1. Copy your pdf to target/crop.pdf and target/uncrop.pdf
	- crop.pdf is for the cropped page of where you want to be read
	- uncrop.pdf is the full page you want to display in the video to be generated
2. Get the pngs from the pdf:
```bash
	python main.py +"Your books title" get-pages
```
3. Delete any of your don't want in "books/Your books title" OR "files/"
4. Extract the text from the PDF, this can be done in two methods:
	1. Get the text straight from the pdf (meaning you can highlight text in the pdf)
```bash
	python main.py +"Your books title" pdf-ext 
```
	2. OCR that bitch (this can take a while)
```bash
	python main.py +"Your books title" page-ocr
```
5. TTS the pages:
```bash
	python main.py +"Your books title" tts
```
6. Create the video with ffmpeg:
```bash
	python main.py +"Your books title" cat # Creates and Concatenates the videos
```

7. Once you have revied the generated video and uploaded it to YouTube, deleate all the temporary files in "books/Your books title" OR "files/"



## Disclaimer

**Educational Use Only**

This collection of Python scripts is designed for educational purposes only. The tool is not intended for commercial use or for creating audiobooks from works you do not have explicit permission to use.

**Usage Warning:** Please refrain from utilizing this tool for converting copyrighted material or any content without proper authorization. The author does not endorse or support any unauthorized use of this software.

**User Responsibility:** Users are solely responsible for ensuring compliance with relevant copyright laws and permissions when using this tool. The author holds no responsibility for any misuse or violation of intellectual property rights arising from the use of this program.

**Limited Liability:** The author of this tool shall not be held liable for any damages or legal issues resulting from the misuse or improper application of this software.

**License and Warranty Disclaimer:** This work is licensed under the terms of the GPL-3 license. Please review the license terms for more details. This software is distributed without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GPL-3 License for more details.
