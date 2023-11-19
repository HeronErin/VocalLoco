
# Vocal Loco

These are some Python scripts I wrote for automatically converting PDFs to audiobooks (in the form of videos). This tool is not user-friendly and is very clunky. However, if you manage to get it to work, feel free to use it.

## Dependencies:
- Linux (or WSL)
- FFmpeg (installed through apt or pacman)
- Tesseract (installed through apt or pacman)
- Pytesseract (installed through pip)
- Requests (installed through pip)
- edge-tts (installed through pip)
- PyPDF2 (installed through pip)
- pdf2image (installed through pip)

## How to Use:

1. Copy your PDFs to `target/crop.pdf` and `target/uncrop.pdf`.
   - `crop.pdf` is for the cropped page of where you want to be read.
   - `uncrop.pdf` is the full page you want to display in the generated video.

2. Get the PNGs from the PDF:
   ```bash
   python main.py +"Your book's title" get-pages
   ```

3. Delete any pages you don't want in `"books/Your book's title"` OR `"files/"`.

4. Extract the text from the PDF, which can be done in two methods:
   1. Get the text straight from the PDF (meaning you can highlight text in the PDF):
      ```bash
      python main.py +"Your book's title" pdf-ext 
      ```
   2. OCR that page (this can take a while):
      ```bash
      python main.py +"Your book's title" page-ocr
      ```

5. Convert the pages to TTS (Text-to-Speech):
   ```bash
   python main.py +"Your book's title" tts
   ```

6. Create the video with FFmpeg:
   ```bash
   python main.py +"Your book's title" cat # Creates and Concatenates the videos
   ```

7. Once you have reviewed the generated video and uploaded it to YouTube, delete all the temporary files in `"books/Your book's title"` OR `"files/"`.


## What it can do:

To save file size, by default a .avi file is created. This is because .avi files support missing frames, otherwise .mp4 files balloon in files size. However this creates the sideffect that when you open it in a media player it can seem glitchey and frames don't display right. This disapears when the video is uploaded to youtube, as they transcode it to mp4, so they get the big file size and you don't need to deal with it. 

Avi:
https://github.com/HeronErin/VocalLoco/raw/main/Network%20File%20System.avi






## Disclaimer

**Educational Use Only**

This collection of Python scripts is designed for educational purposes only. The tool is not intended for commercial use or for creating audiobooks from works you do not have explicit permission to use.

**Usage Warning:** Please refrain from utilizing this tool for converting copyrighted material or any content without proper authorization. The author does not endorse or support any unauthorized use of this software.

**User Responsibility:** Users are solely responsible for ensuring compliance with relevant copyright laws and permissions when using this tool. The author holds no responsibility for any misuse or violation of intellectual property rights arising from the use of this program.

**Limited Liability:** The author of this tool shall not be held liable for any damages or legal issues resulting from the misuse or improper application of this software.

**License and Warranty Disclaimer:** This work is licensed under the terms of the GPL-3 license. Please review the license terms for more details. This software is distributed without any warranty; without even the implied warranty of merchantability or fitness for a particular purpose. See the GPL-3 License for more details.

