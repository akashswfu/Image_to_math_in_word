import sys
import cv2
import os
import subprocess
from PIL import Image
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QFileDialog, QVBoxLayout, QWidget, QMessageBox, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt, QSize

class DropLabel(QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.parent().load_image(file_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation to Word/PDF")
        self.setGeometry(100, 100, 650, 700)

        from pix2tex import cli as pix2tex
        self.model = pix2tex.LatexOCR()
        self.image_path = None

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Image To Word(Math)")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        self.lbl_image = DropLabel(self)
        self.lbl_image.setAlignment(Qt.AlignCenter)
        self.lbl_image.setMinimumSize(400, 300)
        self.lbl_image.setStyleSheet("""
            QLabel {
                border: 2px dashed #7f8c8d;
                border-radius: 10px;
                background-color: #f8f9fa;
                color: #95a5a6;
                font-size: 14px;
            }
        """)
        self.lbl_image.setText("\U0001F4C2 Click 'Upload Image'\n\nPlease upload a good quality image.")
        layout.addWidget(self.lbl_image, 1)

        btn_layout = QHBoxLayout()

        self.btn_upload = QPushButton("Upload Image")
        self.btn_upload.setIcon(QIcon.fromTheme("document-open"))
        self.btn_upload.setStyleSheet(self.style_button("#3498db", "#2980b9"))
        self.btn_upload.clicked.connect(self.upload_image)
        btn_layout.addWidget(self.btn_upload)

        self.btn_convert_docx = QPushButton("Export as DOCX")
        self.btn_convert_docx.setIcon(QIcon.fromTheme("document-save"))
        self.btn_convert_docx.setStyleSheet(self.style_button("#2ecc71", "#27ae60"))
        self.btn_convert_docx.clicked.connect(lambda: self.convert_to("docx"))
        self.btn_convert_docx.setEnabled(False)
        btn_layout.addWidget(self.btn_convert_docx)

        self.btn_convert_pdf = QPushButton("Export as PDF")
        self.btn_convert_pdf.setIcon(QIcon.fromTheme("document-print"))
        self.btn_convert_pdf.setStyleSheet(self.style_button("#e67e22", "#d35400"))
        self.btn_convert_pdf.clicked.connect(lambda: self.convert_to("pdf"))
        self.btn_convert_pdf.setEnabled(False)
        btn_layout.addWidget(self.btn_convert_pdf)

        layout.addLayout(btn_layout)

    def style_button(self, color, hover):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }}
        QPushButton:hover {{
            background-color: {hover};
        }}"""

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg);;All Files (*)")
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        self.image_path = file_path
        pixmap = QPixmap(file_path)
        img = Image.open(file_path)
        width, height = img.size
        max_dim = 500
        if width > height:
            new_width = min(width, max_dim)
            new_height = int((height / width) * new_width)
        else:
            new_height = min(height, max_dim)
            new_width = int((width / height) * new_height)

        self.lbl_image.setPixmap(pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.btn_convert_docx.setEnabled(True)
        self.btn_convert_pdf.setEnabled(True)

    def convert_to(self, format):
        if not self.image_path:
            QMessageBox.warning(self, "Error", "Upload an image first.")
            return

        try:
            img = cv2.imread(self.image_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(img_rgb)
            latex_code = self.model(pil_image).strip()

            print(f"Extracted LaTeX: {latex_code}")

            tex_code = f"""\\documentclass{{article}}
\\usepackage{{amsmath}}
\\begin{{document}}
\\[
{latex_code}
\\]
\\end{{document}}"""

            with open("temp.tex", "w", encoding="utf-8") as f:
                f.write(tex_code)

            if format == "pdf":
                subprocess.run(["pdflatex", "temp.tex"], check=True)
                os.replace("temp.pdf", "output_equation.pdf")
            elif format == "docx":
                import pypandoc
                pypandoc.convert_file("temp.tex", "docx", outputfile="output_equation.docx")

            QMessageBox.information(
                self, "Success",
                f"File saved as output_equation.{format}\n\nExtracted LaTeX:\n{latex_code}"
            )

            for ext in ["aux", "log", "tex"]:
                if os.path.exists(f"temp.{ext}"):
                    os.remove(f"temp.{ext}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Conversion failed:\n{str(e)}")

    def calculate_accuracy(self, ground_truth, predicted):
        import Levenshtein
        dist = Levenshtein.distance(ground_truth, predicted)
        max_len = max(len(ground_truth), len(predicted))
        return (1 - dist / max_len) * 100 if max_len else 100

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
