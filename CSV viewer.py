import re
from PyQt5.QtWidgets import QTabWidget
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5 import QtCore, QtGui, QtWidgets

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
        add = file.addMenu('Add Data')
        save = file.addMenu('save plots')

        save_1 = QAction('&Save-Scatterplot', self)
        save_2 = QAction('&Save-Scatterplot with smooth lines', self)
        save_3 = QAction('&Save-plot with lines', self)

        new_action = QAction('Clear', self)
        open_action = QAction('&Load', self)
        save_action = QAction('&Save', self)

        quit_action = QAction('&Quit', self)

        edit_action = QAction('&Edit(double click)', self)
        addrow_action = QAction('&add row', self)
        addcoloumn_action = QAction('&add coloumn', self)
        delrow_action = QAction('&del row', self)
        delcoloumn_action = QAction('&del coloumn', self)

        file.addAction(open_action)
        file.addAction(save_action)
        file.addMenu(add)

        save.addAction(save_1)
        save.addAction(save_2)
        save.addAction(save_3)
        file.addMenu(save)
        file.addAction(new_action)

        add.addAction(addrow_action)
        add.addAction(addcoloumn_action)

        edit.addAction(edit_action)

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
        elif signal == '&Save-Scatterplot':
            self.form_widget.plotScatterPointsSave('')
        elif signal == '&Save-Scatterplot with smooth lines':
            self.form_widget.plotScatterPointsWithLinesSave('')
        elif signal == '&Save-plot with lines':
            self.form_widget.plotLinesSave('')

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


        self.plotLabel=QtWidgets.QLabel("                                                                REMARK :: First Selected Coloumn - X :: Second Selected Coloumn - Y")
        myfont=QtGui.QFont()
        myfont.setBold(True)
        myfont.setWordSpacing(1.5)
        self.plotLabel.setFont(myfont)


        # for 3 plots ,3 figures

        self.figure2 = plt.figure()
        self.figure3 = plt.figure()
        self.figure4 = plt.figure()

        # Canvas Widget that displays the `figure`
        # it takes the `figure` as argument to constructor

        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas3 = FigureCanvas(self.figure3)
        self.canvas4 = FigureCanvas(self.figure4)

        # 3 save buttons for 3 plots respectively

        self.pushButtonSavePng2 = QtWidgets.QPushButton(self)
        self.pushButtonSavePng2.setText("Save Image")
        self.pushButtonSavePng2.clicked.connect(self.savePngPlot)
        self.pushButtonSavePng2.setFixedWidth(80)

        self.pushButtonSavePng3 = QtWidgets.QPushButton(self)
        self.pushButtonSavePng3.setText("Save Image")
        self.pushButtonSavePng3.clicked.connect(self.savePngPlot)
        self.pushButtonSavePng3.setFixedWidth(80)

        self.pushButtonSavePng4 = QtWidgets.QPushButton(self)
        self.pushButtonSavePng4.setText("Save Image")
        self.pushButtonSavePng4.clicked.connect(self.savePngPlot)
        self.pushButtonSavePng4.setFixedWidth(80)

        self.label=QtWidgets.QLabel()
        self.label.setFont(myfont)


        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.plotLabel)
        grid.addWidget(self.tableView, 1, 0, 1, 9)
        grid.addWidget(self.label)

        #labels

        self.label2=QtWidgets.QLabel()
        self.label3 = QtWidgets.QLabel()
        self.label4 = QtWidgets.QLabel()
        self.label2.setFont(myfont)
        self.label3.setFont(myfont)
        self.label4.setFont(myfont)


        # tabs things
        # tab1 just consists of the whole grid i.e the previous thing

        self.tabs = QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()  # Scatter Plot 1
        self.tab3 = QtWidgets.QWidget()  # Scatter Plot 2
        self.tab4 = QtWidgets.QWidget()  # Line Plot 1

        self.tabs.addTab(self.tab1, "Data Display")
        self.tabs.addTab(self.tab2, "Scatter Points")
        self.tabs.addTab(self.tab3, "Scatter points with smooth lines")
        self.tabs.addTab(self.tab4, "Lines")

        self.tab1.layout = QtWidgets.QVBoxLayout(self)
        self.tab2.layout = QtWidgets.QVBoxLayout(self)
        self.tab3.layout = QtWidgets.QVBoxLayout(self)
        self.tab4.layout = QtWidgets.QVBoxLayout(self)

        self.pushButton2 = QtWidgets.QPushButton("1. Plot Scatter Points")
        self.tab2.layout.addWidget(self.pushButton2)
        self.tab2.layout.addWidget(self.label2)
        self.tab2.layout.addWidget(self.canvas2)


        self.pushButton3 = QtWidgets.QPushButton("2. Plot Scatter Points with smooth lines")
        self.tab3.layout.addWidget(self.pushButton3)
        self.tab3.layout.addWidget(self.label3)
        self.tab3.layout.addWidget(self.canvas3)

        self.pushButton4 = QtWidgets.QPushButton("3. Plot Lines")
        self.tab4.layout.addWidget(self.pushButton4)
        self.tab4.layout.addWidget(self.label4)
        self.tab4.layout.addWidget(self.canvas4)

        # Adding save button to all tabs

        self.tab2.layout.addWidget(self.pushButtonSavePng2, QtCore.Qt.AlignTop)
        self.tab3.layout.addWidget(self.pushButtonSavePng3, QtCore.Qt.AlignTop)
        self.tab4.layout.addWidget(self.pushButtonSavePng4, QtCore.Qt.AlignTop)




        # adding layouts to tabs

        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        self.tab3.setLayout(self.tab3.layout)
        self.tab4.setLayout(self.tab4.layout)
        self.tab1.layout.addLayout(grid)

        # connecting plot buttons in tabs

        self.pushButton2.clicked.connect(self.plotScatterPoints)
        self.pushButton3.clicked.connect(self.plotScatterPointsWithLines)
        self.pushButton4.clicked.connect(self.plotLines)

        # creating an outer layout and adding tabs

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        item = QtGui.QStandardItem()
        self.model.appendRow(item)
        self.model.setData(self.model.index(0, 0), "", 0)
        self.tableView.resizeColumnsToContents()

        # Selection of columns

        self.selectionModel = self.tableView.selectionModel()

        #error messages using lables

        self.error1 = "                                                           !!!YOU HAVE SELECTED MORE OR LESS THAN TWO COLOUMNS (GO BACK AND SELECT TWO)!!!"
        self.error2 = "                                                          !!!YOU HAVE SELECTED WRONG DATATYPE FOR PLOTTING (GO BACK AND SELECT VALID ONE)!!!"

    # selected columns

    def selectedColumns(self):

        # return indexes
        indexes = self.selectionModel.selectedIndexes()
        index_columns = []

        for index in indexes:
            index_columns.append(index.column())
        index_columns = list(set(index_columns))

        return index_columns

    # plot functions for three plots one after other


    def plotScatterPoints(self, fileName):
        self.label2.setVisible(False)
        if len(self.selectedColumns()) != 2:
            self.label2.setVisible(True)
            self.label2.setText(self.error1)
            return -999
        self.figure2.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        # field names
        header = next(reader)
        year = []
        value = []

        # used regex to eliminiate invalid data for plotting i.e if string data is selected to plot

        for row in reader:
            if bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[0]])) and bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                self.label2.setVisible(True)
                self.label2.setText(self.error2)
                return -999



        ax = self.figure2.add_subplot(111)

        # plot data
        colors = [0, 0, 0]
        ax.scatter(year, value, s=np.pi * 3 * 2, c=colors, alpha=0.5, marker='*')
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("scatter points")

        self.figure2.savefig("plot.png")

        # refresh canvas
        self.canvas2.draw()

        # add it to a button
        # self.figure.savefig("plot.png")

    def plotScatterPointsWithLines(self, fileName):

        self.label3.setVisible(False)
        if len(self.selectedColumns()) !=2:
            self.label3.setVisible(True)
            self.label3.setText(self.error1)
            return -999
        self.figure3.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        # field names
        header = next(reader)
        year = []
        value = []
        for row in reader:

            if bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[0]])) and bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                self.label3.setVisible(True)
                self.label3.setText(self.error2)
                return -999


        ax = self.figure3.add_subplot(111)

        # plot data
        ax.plot(year, value, '*-')
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("scatter points with lines")

        # refresh canvas
        self.canvas3.draw()
        self.figure3.savefig("plot.png")

    def plotLines(self, fileName):
        self.label4.setVisible(False)
        if len(self.selectedColumns()) != 2:
            self.label4.setVisible(True)
            self.label4.setText(self.error1)

            return -999

        self.figure4.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        # field names
        header = next(reader)
        year = []
        value = []
        for row in reader:
            if bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[0]])) and bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                self.label4.setVisible(True)
                self.label4.setText(self.error2)
                return -999


        ax = self.figure4.add_subplot(111)

        # plot data
        ax.plot(year, value)
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("plot lines")
        self.figure4.savefig("plot.png")

        # refresh canvas
        self.canvas4.draw()

        # add it to a button
        # self.figure.savefig("plot.png")

    def savePngPlot(self):

        im = Image.open('plot.png')

        #used tinkter class for filedialogue for saving

        window = Tk()
        window.withdraw()
        file = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
        if file:
            im.save(file)

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

    #functions for saving plots through menu

    def plotScatterPointsSave(self, fileName):
        self.label.setVisible(False)
        if len(self.selectedColumns()) != 2:
            self.label.setVisible(True)
            self.label.setText(self.error1)
            return -999

        self.figure2.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        # field names
        header = next(reader)
        year = []
        value = []
        for row in reader:
            if bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[0]])) and bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                self.label.setVisible(True)
                self.label.setText(self.error2)
                return -999

        ax = self.figure2.add_subplot(111)

        # plot data
        colors = [0, 0, 0]
        ax.scatter(year, value, s=np.pi * 3 * 2, c=colors, alpha=0.5, marker='*')
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("scatter points")

        self.figure2.savefig("plot.png")
        self.savePngPlot()



    def plotScatterPointsWithLinesSave(self, fileName):
        self.label.setVisible(False)
        if len(self.selectedColumns()) != 2:
            self.label.setVisible(True)
            self.label.setText(self.error1)
            return
        self.figure3.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        # field names
        header = next(reader)
        year = []
        value = []
        for row in reader:
            if bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[0]])) and bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                self.label.setVisible(True)
                self.label.setText(self.error2)
                return -999

        ax = self.figure3.add_subplot(111)

        # plot data
        ax.plot(year, value, '*-')
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("scatter points with lines")


        self.figure3.savefig("plot.png")
        self.savePngPlot()

    def plotLinesSave(self, fileName):
        self.label.setVisible(False)
        if len(self.selectedColumns()) != 2:
            self.label.setVisible(True)
            self.label.setText(self.error1)
            return

        self.figure4.clf()

        f = open(self.fileName, 'r')
        reader = csv.reader(f)
        style.use('ggplot')
        # field names
        header = next(reader)
        year = []
        value = []
        for row in reader:
            if bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[0]])) and bool(re.match('^[0-9\.\- ]*$',row[self.selectedColumns()[1]])):
                year.append(float(row[self.selectedColumns()[0]]))
                value.append(float(row[self.selectedColumns()[1]]))
            else:
                self.label.setVisible(True)
                self.label.setText(self.error2)
                return -999

        ax = self.figure4.add_subplot(111)

        # plot data
        ax.plot(year, value)
        ax.set_xlabel(header[self.selectedColumns()[0]])
        ax.set_ylabel(header[self.selectedColumns()[1]])
        ax.set_title("plot lines")
        self.figure4.savefig("plot.png")

        # refresh canvas
        self.savePngPlot()







    def removeRow(self):
        model = self.model
        indices = self.tableView.selectionModel().selectedRows()
        for index in sorted(indices):
            model.removeRow(index.row())

    def addRow(self):
        item = QtGui.QStandardItem("")
        self.model.appendRow(item)
        self.tableView.scrollToBottom()

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
    main.setGeometry(50, 50, 800, 600)
    main.setWindowTitle("CSV Viewer")
    main.show()

    sys.exit(app.exec_())