from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider, QLineEdit)

from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2 as cv
import math
import numpy as np


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        openButton = QPushButton("Open", self)
        openButton.setCheckable(True)
        openButton.clicked[bool].connect(self.openImage)
        openButton.setStyleSheet("font-size: 18px; background-color: green;")

        self.source_image = QLabel(self)
        self.source_image.setAlignment(Qt.AlignCenter)
        self.openclose = QLabel(self)
        self.openclose.setAlignment(Qt.AlignCenter)

        hbox_image = QHBoxLayout(self)
        hbox_image.addWidget(self.source_image)
        hbox_image.addWidget(self.openclose)

        self.kernel_size = QSlider(Qt.Horizontal, self)
        self.kernel_size.setMinimum(3)
        self.kernel_size.setMaximum(25)
        self.kernel_size.setValue(3)
        self.kernel_size.valueChanged[int].connect(self.changeSliderValue)
        self.aEdit = QLineEdit(self)
        self.aEdit.setText('3')
        self.aEdit.textChanged.connect(self.changeTextValue)

        self.shp = QComboBox(self)
        self.shp.addItems(['rectangle', 'cross', 'ellipse'])
        self.shp.currentIndexChanged.connect(self.setkernelshape)
        self.opt = QComboBox(self)
        self.opt.addItems(['dilation', 'erosion', 'opening', 'closing'])

        button_conv = QPushButton("Execute", self)
        button_conv.setCheckable(True)
        button_conv.clicked[bool].connect(self.conv)
        button_conv.setStyleSheet("font-size: 18px; background-color: green;")

        hbox_SEinfo = QHBoxLayout(self)
        hbox_SEinfo.addWidget(self.shp)
        hbox_SEinfo.addWidget(self.opt)
        hbox_SEinfo.addWidget(self.kernel_size)
        hbox_SEinfo.addWidget(self.aEdit)

        hbox_last = QHBoxLayout(self)
        hbox_last.addWidget(openButton)
        hbox_last.addWidget(button_conv)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox_image)
        vbox.addLayout(hbox_SEinfo)
        vbox.addLayout(hbox_last)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(700, 200, 560, 500)
        self.setWindowTitle('Temel Gri Tonlama Morfolojik İşlemler')
        self.show()

        self.img_name = ''
        self.img_shape = (300, 300)
        self.morphtype = cv.MORPH_RECT

    def openImage(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        img = cv.imread(self.img_name, 0)
        self.img_shape = img.shape
        if self.img_shape[0] > 300 or self.img_shape[1] > 300:
            img = cv.resize(img, (300, 300), interpolation=cv.INTER_CUBIC)
            self.img_shape = (300, 300)
        cv.imwrite('./image_to_show/source.jpg', img)
        pixmap_source = QPixmap('./image_to_show/source.jpg')
        self.source_image.setPixmap(pixmap_source)

    def conv(self):
        img = cv.imread('./image_to_show/source.jpg', 0)
        kernel = cv.getStructuringElement(self.morphtype, (self.a, self.a))
        if self.opt.currentText() == 'dilation':
            res = cv.dilate(img, kernel)
        elif self.opt.currentText() == 'erosion':
            res = cv.erode(img, kernel)
        elif self.opt.currentText() == 'opening':
            res = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
        elif self.opt.currentText() == 'closing':
            res = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
        cv.imwrite('./image_to_show/openclose.jpg', res)
        pixmap_openclose = QPixmap('./image_to_show/openclose.jpg')
        self.openclose.setPixmap(pixmap_openclose)

    def changeSliderValue(self, value):
        self.a = value
        self.aEdit.setText(str(value))

    def changeTextValue(self):
        if self.aEdit.text() == '':
            self.a = 3
        elif not self.aEdit.text().isdigit():
            self.a = 3
            self.aEdit.setText(str(self.a))
        else:
            self.a = int(self.aEdit.text())
        self.kernel_size.setValue(self.a)

    def setkernelshape(self):
        if self.shp.currentText() == 'rectangle':
            self.morphtype = cv.MORPH_RECT
        elif self.shp.currentText() == 'cross':
            self.morphtype = cv.MORPH_CROSS
        elif self.shp.currentText() == 'ellipse':
            self.morphtype = cv.MORPH_ELLIPSE


if __name__ == '__main__':

    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')

    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
