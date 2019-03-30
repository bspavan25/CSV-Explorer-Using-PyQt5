from PyQt5.QtWidgets import QTabWidget
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QAction

from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QFile

import csv
import os
from tkinter import filedialog, Tk
from PIL import Image


""" this a class where we instantiate object of MyWindow class
    (where csv functionalities are defined) and add menubar stuff """


class Outerone(QMainWindow):

    def __init__(self):
        super().__init__()

        # created instance of the other class

        # self.form_widget = MyWindow('')
        # self.setCentralWidget(self.form_widget)

        self.init_ui()

    def init_ui(self):

        # menu bar stuff

        bar = self.menuBar()
        file = bar.addMenu('File')
        edit = bar.addMenu('Edit')

        new_action = QAction('Clear', self)
        open_action = QAction('&Load', self)
        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        quit_action = QAction('&Quit', self)

        edit_action = QAction('&Edit(double click)', self)
        addrow_action = QAction('&add row', self)
        addcoloumn_action = QAction('&add coloumn', self)
        delrow_action = QAction('&del row', self)
        delcoloumn_action = QAction('&del coloumn', self)

        file.addAction(open_action)
        file.addAction(save_action)
        file.addAction(new_action)
        file.addAction(quit_action)

        edit.addAction(edit_action)
        edit.addAction(addrow_action)
        edit.addAction(addcoloumn_action)
        edit.addAction(delrow_action)
        edit.addAction(delcoloumn_action)

        quit_action.triggered.connect(self.quit_trigger)

        # file.triggered.connect(self.respond1)
        # edit.triggered.connect(self.respond2)

        self.show()

    def quit_trigger(self):
        sys.exit(app.exec_())

    ''' def respond1(self, q):
        signal = q.text()

        if signal == 'Clear':
            self.form_widget.clearList()
        elif signal == '&Load':
            self.form_widget.loadCsv(1)
        elif signal == '&Save':
            self.form_widget.writeCsv(1)
        elif signal == '&add row':
            self.form_widget.addRow()
        elif signal == '&add coloumn':
            self.form_widget.addColumn()
            
    def respond2(self, q):
        signal = q.text()

        if signal == '&add row':
            self.form_widget.addRow()
        elif signal == '&add coloumn':
            self.form_widget.addColumn()
        elif signal == '&del row':
            self.form_widget.removeRow()
        elif signal == '&del coloumn':
            self.form_widget.removeColumn()
        elif signal == '&Edit(double click)':
            self.form_widget.Edit()'''

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    main = Outerone()
    main.setMinimumSize(820, 300)
    main.setGeometry(50, 50, 500, 500)
    main.setWindowTitle("CSV Viewer")
    main.show()

    sys.exit(app.exec_())
