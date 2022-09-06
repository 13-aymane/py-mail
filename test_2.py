import sys
from os import sep
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtWidgets

class MyWin(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        uic.loadUi("test_2.ui", self)  # load ui
        
        self.counter = 1  #this is going to be used to set unique names
        self.add_product.clicked.connect(self.add)
        self.remove_product.clicked.connect(self.remove)
        
        self.dynamically_added_widgets = list() 

    def add(self):
        self.counter += 1
        h1 = QHBoxLayout()
        self.label = QLabel()
        self.label.setObjectName(f"name{self.counter}")  # set a new, unique name
        self.label.text = "L"
        h1.addWidget(self.label)
        h1.addWidget(QLabel('Weight'))
        h2 = QHBoxLayout()
        h2.addWidget(QLineEdit())
        h2.addWidget(QLineEdit())
        i = self.verticalLayout_2.count()
        self.verticalLayout_2.insertLayout(i - 2, h1)
        self.verticalLayout_2.insertLayout(i - 1, h2)

        self.dynamically_added_widgets.append(self.label) # add the new label to list
        print(self.dynamically_added_widgets)
        print(self.dynamically_added_widgets[-1].objectName())  # print the last added label's objectName
    def remove(self):
        i = self.verticalLayout_2.count()
        if i > 3:
            QWidget().setLayout(self.verticalLayout_2.takeAt(i - 3))
            QWidget().setLayout(self.verticalLayout_2.takeAt(i - 4))

app = QApplication(sys.argv)  # create app
mw = MyWin()  # create object of MyWin class
mw.show()  # to show gui
sys.exit(app.exec_())  # execute app