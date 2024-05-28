from PyQt5.QtWidgets import (QMainWindow, QWidget, QFileDialog, QApplication, QLineEdit, QLabel, QComboBox,
                             QHBoxLayout, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import os
import cv2 as cv
import numpy as np
from skimage import morphology

class AdvancedGrayMorphology(QMainWindow):

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

        exeButton = QPushButton("Execute", self)
        exeButton.setCheckable(True)
        exeButton.clicked[bool].connect(self.execute)

        self.operation = QComboBox(self)
        self.operation.addItems(['Morphological edge detection', 
                                 'Morphological Reconstruction',
                                 'Conditional dilation in binary image',
                                 'Gray scale Reconstruction',
                                 'Morphological gradient'])

        hbox1 = QHBoxLayout(self)
        hbox1.addWidget(self.source)
        hbox1.addWidget(self.processed)

        hbox2 = QHBoxLayout(self)
        hbox2.addWidget(self.operation)

        hbox3 = QHBoxLayout(self)
        hbox3.addWidget(openButton)
        hbox3.addWidget(exeButton)

        vbox = QVBoxLayout(self)
        vbox.addLayout(hbox1, stretch=6)
        vbox.addLayout(hbox2, stretch=1)
        vbox.addLayout(hbox3, stretch=1)

        widget = QWidget()
        widget.setLayout(vbox)
        self.setCentralWidget(widget)

        self.setGeometry(700, 200, 560, 500)
        self.setWindowTitle('Gelişmiş Gri Tonlama Morfolojik İşlemler')
        self.show()

        self.img_name = ''
        self.img_shape = (300, 300)

    def openImage(self):
        self.img_name = QFileDialog.getOpenFileName(self, 'Choose Image File', '')[0]
        self.img = cv.imread(self.img_name, 0)
        self.img_shape = self.img.shape
        if self.img_shape[0] > 300 or self.img_shape[1] > 300:
            self.img = cv.resize(self.img, (300, 300), interpolation=cv.INTER_CUBIC)
            self.img_shape = (300, 300)
        cv.imwrite('./image_to_show/source3.jpg', self.img)
        pixmap_source = QPixmap('./image_to_show/source3.jpg')
        self.source.setPixmap(pixmap_source)

    def execute(self):
        if self.operation.currentText() == 'Morphological edge detection':
            self.morphological_edge_detection()
        elif self.operation.currentText() == 'Morphological Reconstruction':
            self.morphological_reconstruction()
        elif self.operation.currentText() == 'Conditional dilation in binary image':
            self.conditional_dilation()
        elif self.operation.currentText() == 'Gray scale Reconstruction':
            self.grayscale_reconstruction()
        elif self.operation.currentText() == 'Morphological gradient':
            self.morphological_gradient()

    def morphological_edge_detection(self):
        kernel = np.ones((5,5),np.uint8)
        gradient = cv.morphologyEx(self.img, cv.MORPH_GRADIENT, kernel)
        cv.imwrite('./image_to_show/edge_detection.jpg', gradient)
        pixmap_edge = QPixmap('./image_to_show/edge_detection.jpg')
        self.processed.setPixmap(pixmap_edge)

    def morphological_reconstruction(self):
        seed = np.copy(self.img)
        seed[1:-1, 1:-1] = self.img.max()
        mask = self.img
        reconstructed = morphology.reconstruction(seed, mask, method='erosion')
        cv.imwrite('./image_to_show/reconstruction.jpg', reconstructed)
        pixmap_reconstruction = QPixmap('./image_to_show/reconstruction.jpg')
        self.processed.setPixmap(pixmap_reconstruction)

    def conditional_dilation(self):
        selem = morphology.disk(1)
        seed = np.copy(self.img)
        seed[5:-5, 5:-5] = self.img.max()
        dilated = morphology.dilation(seed, selem)
        cv.imwrite('./image_to_show/conditional_dilation.jpg', dilated)
        pixmap_dilation = QPixmap('./image_to_show/conditional_dilation.jpg')
        self.processed.setPixmap(pixmap_dilation)

    def grayscale_reconstruction(self):
        seed = np.copy(self.img)
        seed[1:-1, 1:-1] = self.img.max()
        mask = self.img
        reconstructed = morphology.reconstruction(seed, mask, method='dilation')
        cv.imwrite('./image_to_show/grayscale_reconstruction.jpg', reconstructed)
        pixmap_reconstruction = QPixmap('./image_to_show/grayscale_reconstruction.jpg')
        self.processed.setPixmap(pixmap_reconstruction)

    def morphological_gradient(self):
        kernel = np.ones((5,5),np.uint8)
        gradient = cv.morphologyEx(self.img, cv.MORPH_GRADIENT, kernel)
        cv.imwrite('./image_to_show/gradient.jpg', gradient)
        pixmap_gradient = QPixmap('./image_to_show/gradient.jpg')
        self.processed.setPixmap(pixmap_gradient)


if __name__ == '__main__':

    if not os.path.exists('image_to_show'):
        os.mkdir('image_to_show')

    app = QApplication(sys.argv)
    ex = AdvancedGrayMorphology()
    sys.exit(app.exec_())
