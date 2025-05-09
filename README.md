This includes all the necessary Python dependencies for your project:

PySide6>=6.5.0
opencv-python
pillow
pix2tex
pypandoc
python-Levenshtein

    ⚠️ Note: pix2tex has its own dependencies including PyTorch, torchvision, and transformers, so make sure has a compatible environment with those. You can guide them to install it via the official instructions if needed.


# 🧮  Image to Word/PDF Converter

Image To Math is a Python-based GUI application that allows you to extract math equations from images and convert them into editable Word (DOCX) or PDF documents with proper formatting using LaTeX.

## ✨ Features

- 📤 Upload or drag-and-drop image functionality.
- 🧠 Uses `pix2tex` to convert images to LaTeX.
- 📄 Export to DOCX or PDF formats.
- 🎨 Beautiful and minimal PySide6 GUI.
- ✅ Real-time LaTeX preview and confirmation.
- 📂 Message prompts and error handling.
- 💡 Designed for students, teachers, and researchers.

## 🚀 How It Works

1. Upload or drop an image containing a math equation.
2. The app uses `pix2tex` to extract LaTeX code from the image.
3. The LaTeX is compiled using `pdflatex` (for PDF) or converted using `pandoc` (for DOCX).
4. Final output is saved as either `output_equation.pdf` or `output_equation.docx`.

## 🛠 Installation

First, clone the repository and install the dependencies:


pip install -r requirements.txt

Install pix2tex

Make sure to follow the official installation guide here: https://github.com/lukas-blecher/LaTeX-OCR

Or install it directly if you have the environment ready:

pip install pix2tex

pix2tex requires PyTorch, which may need a CUDA-compatible environment.

Install LaTeX and Pandoc

Ensure pdflatex and pandoc are available in your system:

Windows: Install MiKTeX and Pandoc.

Linux: Install via apt or your package manager:

sudo apt install texlive pandoc

📸 Screenshots

![alt text](image.png)
![alt text](image-1.png)
![alt text](image-3.png)


💡 Future Features

    ✅ Copy LaTeX to clipboard.

    🌙 Dark Mode toggle.

    📄 Export to HTML, MathML, or PDF with multiple equations.

    📦 Portable App packaging.