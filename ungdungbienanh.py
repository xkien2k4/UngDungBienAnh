# author : Nguyen Vu Xuan Kien | 17/02/2004  | kien1722004@gmail.com
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QSlider, QWidget, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage


class CannyEdgeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng biên ảnh (Canny Edge Detection) by Xuân Kiên")
        self.setGeometry(100, 100, 800, 600)

        self.image = None
        self.edges = None
        self.threshold1 = 50
        self.threshold2 = 150

        self.init_ui()

    def init_ui(self):
        # Layout chính
        layout = QVBoxLayout()

        # Nút chọn ảnh
        self.btn_load = QPushButton("Chọn ảnh")
        self.btn_load.clicked.connect(self.load_image)

        # Hiển thị ảnh gốc và ảnh biên
        self.label_original = QLabel("Ảnh gốc")
        self.label_edges = QLabel("Ảnh biên (Canny)")
        self.label_original.setAlignment(Qt.AlignCenter)
        self.label_edges.setAlignment(Qt.AlignCenter)

        # Thanh trượt điều chỉnh ngưỡng
        slider_layout = QHBoxLayout()
        self.slider_threshold1 = QSlider(Qt.Horizontal)
        self.slider_threshold2 = QSlider(Qt.Horizontal)
        self.slider_threshold1.setRange(0, 255)
        self.slider_threshold2.setRange(0, 255)
        self.slider_threshold1.setValue(self.threshold1)
        self.slider_threshold2.setValue(self.threshold2)
        self.slider_threshold1.valueChanged.connect(self.update_threshold)
        self.slider_threshold2.valueChanged.connect(self.update_threshold)
        slider_layout.addWidget(QLabel("Ngưỡng 1:"))
        slider_layout.addWidget(self.slider_threshold1)
        slider_layout.addWidget(QLabel("Ngưỡng 2:"))
        slider_layout.addWidget(self.slider_threshold2)

        # Gắn vào layout chính
        layout.addWidget(self.btn_load)
        layout.addWidget(self.label_original)
        layout.addWidget(self.label_edges)
        layout.addLayout(slider_layout)

        # Tạo widget trung tâm
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_image(self):
        # Mở hộp thoại chọn ảnh
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn ảnh", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            # Đọc ảnh
            self.image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.display_image(self.image, self.label_original)
            self.apply_canny()

    def apply_canny(self):
        if self.image is not None:
            # Áp dụng kỹ thuật Canny
            self.edges = cv2.Canny(self.image, self.threshold1, self.threshold2)
            self.display_image(self.edges, self.label_edges)

    def update_threshold(self):
        # Cập nhật ngưỡng và áp dụng lại Canny
        self.threshold1 = self.slider_threshold1.value()
        self.threshold2 = self.slider_threshold2.value()
        self.apply_canny()

    def display_image(self, img, label):
        # Chuyển đổi ảnh thành định dạng hiển thị trên QLabel
        if len(img.shape) == 2:  # Ảnh grayscale
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_Grayscale8)
        else:  # Ảnh RGB
            qimg = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CannyEdgeApp()
    window.show()
    sys.exit(app.exec_())
