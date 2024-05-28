from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.binary = QLabel(self)
        self.binary.setAlignment(Qt.AlignCenter)

        self.processed = QLabel(self)
        self.processed.setAlignment(Qt.AlignCenter)

        openButton = QPushButton("Open Image", self)
        openButton.clicked.connect(self.openImage)

        exeButton = QPushButton("Execute", self)
        exeButton.clicked.connect(self.execute)

        self.ksSlide = QSlider(Qt.Horizontal, self)
        self.ksSlide.setMinimum(5)
        self.ksSlide.setMaximum(15)
        self.ksSlide.setValue(5)
        self.ksSlide.valueChanged[int].connect(self.changeSliderValue)
        self.ksEditor = QLineEdit(self)
        self.ksEditor.setText('5')
        self.ksEditor.textChanged.connect(self.changeTextValue)

        self.kernel_shape = QComboBox(self)
        self.kernel_shape.addItems(['ellipse', 'cross', 'rectangle'])
        self.kernel_shape.currentIndexChanged.connect(self.setKernelShape)
        self.SE_shape = cv2.MORPH_ELLIPSE  # default

        self.opt = QComboBox(self)
        self.opt.addItems(['dilation', 'erosion', 'opening', 'closing'])

        hbox1 = QHBoxLayout(self)
        hbox1.addWidget(self.binary)
        hbox1.addWidget(self.processed)

        hbox2 = QHBoxLayout(self)
        hbox2.addWidget(self.kernel_shape)
        hbox2.addWidget(self.opt)
        hbox2.addWidget(self.ksSlide)
        hbox2.addWidget(self.ksEditor)

        hbox3 = QHBoxLayout(self)
        hbox3.addWidget(openButton)
        hbox3.addWidget(exeButton)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(700, 200, 800, 600)
        self.setWindowTitle('Temel İkili Morfolojik İşlemler')
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border: none;
                padding: 15px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
                border: 1px solid #ddd;
                padding: 10px;
                background-color: #f9f9f9;
                margin: 5px;
            }
            QComboBox {
                padding: 5px;
                margin: 5px;
            }
            QLineEdit {
                padding: 5px;
                margin: 5px;
                font-size: 14px;
                width: 60px;
            }
        """)
        self.show()

        self.img_name = ''
        self.img_shape = (300, 300)

    def openImage(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        if self.img_name:
            self.img = cv2.imread(self.img_name, 0)
            self.img_shape = self.img.shape
            if self.img_shape[0] > 300 or self.img_shape[1] > 300:
                self.img = cv2.resize(self.img, (300, 300), interpolation=cv2.INTER_CUBIC)
                self.img_shape = (300, 300)
            cv2.imwrite('./image_to_show/source.jpg', self.img)

            ret, thr = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU)
            self.binary_img = thr
            cv2.imwrite('./image_to_show/thr.jpg', thr)
            pixmap_binary = QPixmap('./image_to_show/thr.jpg')
            self.binary.setPixmap(pixmap_binary)

    def execute(self):
        kernel_size = int(self.ksSlide.value())
        kernel = cv2.getStructuringElement(self.SE_shape, (kernel_size, kernel_size))
        if self.opt.currentText() == 'dilation':
            processed_img = cv2.dilate(self.binary_img, kernel)
        elif self.opt.currentText() == 'erosion':
            processed_img = cv2.erode(self.binary_img, kernel)
        elif self.opt.currentText() == 'opening':
            processed_img = cv2.morphologyEx(self.binary_img, cv2.MORPH_OPEN, kernel)
        elif self.opt.currentText() == 'closing':
            processed_img = cv2.morphologyEx(self.binary_img, cv2.MORPH_CLOSE, kernel)
        cv2.imwrite('./image_to_show/processed_img.jpg', processed_img)
        pixmap_pro = QPixmap('./image_to_show/processed_img.jpg')
        self.processed.setPixmap(pixmap_pro)

    def setKernelShape(self):
        shape_text = self.kernel_shape.currentText()
        if shape_text == 'rectangle':
            self.SE_shape = cv2.MORPH_RECT
        elif shape_text == 'cross':
            self.SE_shape = cv2.MORPH_CROSS
        elif shape_text == 'ellipse':
            self.SE_shape = cv2.MORPH_ELLIPSE

    def changeSliderValue(self, value):
        self.ksEditor.setText(str(value))

    def changeTextValue(self, txt):
        if txt.isdigit():
            self.ksSlide.setValue(int(txt))


if __name__ == '__main__':
    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')

    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
