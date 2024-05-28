from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton, QSlider)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2
import numpy as np


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.source = QLabel(self)
        self.source.setAlignment(Qt.AlignCenter)

        self.processed = QLabel(self)
        self.processed.setAlignment(Qt.AlignCenter)

        openButton = QPushButton("Open Image", self)
        openButton.setCheckable(True)
        openButton.clicked[bool].connect(self.openImage)
        openButton.setStyleSheet("font-size: 18px; background-color: green;")

        exeButton = QPushButton("Execute", self)
        exeButton.setCheckable(True)
        exeButton.clicked[bool].connect(self.execute)
        exeButton.setStyleSheet("font-size: 18px; background-color: green;")

        self.alpha = QSlider(Qt.Horizontal, self)
        self.alpha.setMinimum(0)
        self.alpha.setMaximum(10)
        self.alpha.setValue(2)
        self.alpha.valueChanged[int].connect(self.changeAlpha)

        self.beta = QSlider(Qt.Horizontal, self)
        self.beta.setMinimum(0)
        self.beta.setMaximum(10)
        self.beta.setValue(5)
        self.beta.valueChanged[int].connect(self.changeBeta)

        self.gamma = QSlider(Qt.Horizontal, self)
        self.gamma.setMinimum(0)
        self.gamma.setMaximum(10)
        self.gamma.setValue(9)
        self.gamma.valueChanged[int].connect(self.changeGamma)

        self.operation = QComboBox(self)
        self.operation.addItems(['internal gradient', 'external gradient', 'mean gradient',
                                 'Laplacian of Gaussian', 'top hat', 'black hat'])

        hbox1 = QHBoxLayout(self)
        hbox1.addWidget(self.source)
        hbox1.addWidget(self.processed)

        hbox2 = QHBoxLayout(self)
        hbox2.addWidget(openButton)
        hbox2.addWidget(exeButton)

        hbox3 = QHBoxLayout(self)
        hbox3.addWidget(self.alpha)
        hbox3.addWidget(self.beta)
        hbox3.addWidget(self.gamma)
        hbox3.addWidget(self.operation)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1, stretch=6)
        vbox.addLayout(hbox2, stretch=1)
        vbox.addLayout(hbox3, stretch=1)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(700, 200, 560, 500)
        self.setWindowTitle('Gelişmiş Gri Tonlama Morfoloji')
        self.show()

        self.img_name = ''
        self.img_shape = (300, 300)

    def openImage(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        self.img = cv2.imread(self.img_name, 0)
        self.img_shape = self.img.shape
        if self.img_shape[0] > 300 or self.img_shape[1] > 300:
            self.img = cv2.resize(self.img, (300, 300), interpolation=cv2.INTER_CUBIC)
            self.img_shape = (300, 300)
        cv2.imwrite('./image_to_show/source3.jpg', self.img)
        pixmap_source = QPixmap('./image_to_show/source3.jpg')
        self.source.setPixmap(pixmap_source)

    def execute(self):
        if self.operation.currentText() == 'internal gradient':
            self.internal_gradient()
        elif self.operation.currentText() == 'external gradient':
            self.external_gradient()
        elif self.operation.currentText() == 'mean gradient':
            self.mean_gradient()
        elif self.operation.currentText() == 'Laplacian of Gaussian':
            self.LoG()
        elif self.operation.currentText() == 'top hat':
            self.tophat()
        elif self.operation.currentText() == 'black hat':
            self.blackhat()

    def changeAlpha(self, value):
        self.alpha_value = value

    def changeBeta(self, value):
        self.beta_value = value

    def changeGamma(self, value):
        self.gamma_value = value

    def internal_gradient(self):
        kernel = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(self.img, kernel, iterations=1)
        erosion = cv2.erode(self.img, kernel, iterations=1)
        internal_gradient = dilation - erosion
        cv2.imwrite('./image_to_show/internal_gradient.jpg', internal_gradient)
        pixmap_processed = QPixmap('./image_to_show/internal_gradient.jpg')
        self.processed.setPixmap(pixmap_processed)

    def external_gradient(self):
        kernel = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(self.img, kernel, iterations=1)
        erosion = cv2.erode(self.img, kernel, iterations=1)
        external_gradient = dilation + erosion
        cv2.imwrite('./image_to_show/external_gradient.jpg', external_gradient)
        pixmap_processed = QPixmap('./image_to_show/external_gradient.jpg')
        self.processed.setPixmap(pixmap_processed)

    def mean_gradient(self):
        kernel = np.ones((3, 3), np.uint8)
        dilation = cv2.dilate(self.img, kernel, iterations=1)
        erosion = cv2.erode(self.img, kernel, iterations=1)
        mean_gradient = (dilation + erosion) / 2
        cv2.imwrite('./image_to_show/mean_gradient.jpg', mean_gradient)
        pixmap_processed = QPixmap('./image_to_show/mean_gradient.jpg')
        self.processed.setPixmap(pixmap_processed)

    def LoG(self):
        laplacian = cv2.Laplacian(self.img, cv2.CV_64F)
        cv2.imwrite('./image_to_show/LoG.jpg', laplacian)
        pixmap_processed = QPixmap('./image_to_show/LoG.jpg')
        self.processed.setPixmap(pixmap_processed)

    def tophat(self):
        kernel = np.ones((5, 5), np.uint8)
        tophat = cv2.morphologyEx(self.img, cv2.MORPH_TOPHAT, kernel)
        cv2.imwrite('./image_to_show/tophat.jpg', tophat)
        pixmap_processed = QPixmap('./image_to_show/tophat.jpg')
        self.processed.setPixmap(pixmap_processed)

    def blackhat(self):
        kernel = np.ones((5, 5), np.uint8)
        blackhat = cv2.morphologyEx(self.img, cv2.MORPH_BLACKHAT, kernel)
        cv2.imwrite('./image_to_show/blackhat.jpg', blackhat)
        pixmap_processed = QPixmap('./image_to_show/blackhat.jpg')
        self.processed.setPixmap(pixmap_processed)


if __name__ == '__main__':

    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')

    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
