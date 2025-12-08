# PDF Logo / Watermark Removal Tool

This project is a small Python utility that detects and removes a **single recurring logo/watermark** from every page of a PDF file.

The script uses **SIFT + FLANN feature matching** to locate the logo (even if it appears at different positions or slightly transformed) and then removes it using **OpenCV inpainting**, reconstructing the background as naturally as possible.

---

## Features

- Detects a single known logo on each page using SIFT feature matching.
- Works even if the logo:
  - Is slightly rotated or scaled.
  - Appears at different positions on each page.
- Uses OpenCV inpainting to fill the removed area and blend it with the background.
- Preserves overall page colors (proper RGB ↔ BGR handling).
- Outputs a cleaned PDF with the same number of pages as the original.

---

## Requirements

Python 3.8+ is recommended.

Install the required packages:

```bash
pip install opencv-python numpy pdf2image img2pdf
