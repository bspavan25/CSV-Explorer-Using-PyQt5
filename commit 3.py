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

        self.form_widget = MyWindow('')
        self.setCentralWidget(self.form_widget)

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

        file.triggered.connect(self.respond1)
        edit.triggered.connect(self.respond2)

        self.show()

    def quit_trigger(self):
        sys.exit(app.exec_())

    def respond1(self, q):
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
            self.form_widget.Edit()


class MyWindow(QtWidgets.QWidget):

    def __init__(self, fileName, parent=None):

        super(MyWindow, self).__init__(parent)
        self.fileName = ""
        self.fname = ""
        self.model = QtGui.QStandardItemModel(self)

        self.tableView = QtWidgets.QTableView(self)
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.setShowGrid(True)
        self.tableView.setGeometry(10, 50, 1000, 645)
        self.model.dataChanged.connect(self.finishedEdit)

       

    def loadCsv(self, fileName):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV",
                                                            (QtCore.QDir.homePath()), "CSV (*.csv *.tsv)")
        self.fileName = fileName
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        if fileName:
            print(fileName)
            ff = open(fileName, 'r', newline='')
            lines = [line for line in ff]
            print(lines[0].strip().split(','))
            mytext = ff.read()
            ff.close()
            f = open(fileName, 'r')
            with f:
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)
                if mytext.count(';') <= mytext.count('\t'):
                    reader = csv.reader(f)
                    self.model.clear()
                    for row in reader:
                        print(row)
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)

                    self.tableView.resizeColumnsToContents()
                else:
                    reader = csv.reader(f, delimiter=';')
                    self.model.clear()
                    for row in reader:
                        items = [QtGui.QStandardItem(field) for field in row]
                        self.model.appendRow(items)
                    self.tableView.resizeColumnsToContents()
    def Edit(self):
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)

    def writeCsv(self, fileName):
        # find empty cells
        for row in range(self.model.rowCount()):
            for column in range(self.model.columnCount()):
                myitem = self.model.item(row, column)
                if myitem is None:
                    item = QtGui.QStandardItem("")
                    self.model.setItem(row, column, item)
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File",
                                                            (QtCore.QDir.homePath() + "/" + self.fname + ".csv"),
                                                            "CSV Files (*.csv)")
        if fileName:
            print(fileName)
            f = open(fileName, 'w', newline='')
            with f:
                writer = csv.writer(f, delimiter=',')
                for rowNumber in range(self.model.rowCount()):
                    fields = [self.model.data(self.model.index(rowNumber, columnNumber),
                                              QtCore.Qt.DisplayRole)
                              for columnNumber in range(self.model.columnCount())]
                    writer.writerow(fields)
                self.fname = os.path.splitext(str(fileName))[0].split("/")[-1]
                self.setWindowTitle(self.fname)


    def removeRow(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedRows()
        for index in sorted(indices):
            model.removeRow(index.row())

    def addRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)

    def clearList(self):
        self.model.clear()

    def removeColumn(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedColumns()
        for index in sorted(indices):
            model.removeColumn(index.column())

    def addColumn(self):
        count = self.model.columnCount()
        print(count)
        self.model.setColumnCount(count + 1)
        self.model.setData(self.model.index(0, count), "", 0)
        self.tableView.resizeColumnsToContents()

    def finishedEdit(self):
        self.tableView.resizeColumnsToContents()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('MyWindow')
    main = Outerone()
    main.setMinimumSize(820, 400)
    main.setGeometry(50, 50, 600, 500)
    main.setWindowTitle("CSV Viewer")
    main.show()

    sys.exit(app.exec_())