from os import sep
from PyQt5.QtWidgets import *
from PyQt5 import uic

class MyGui(QMainWindow):
    
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi("button.ui",self)
        self.show()
        self.pushButton.clicked.connect(self.increment)
        self.count = 0
    def increment(self):
        self.count += 1
        print(self.count)

        
app = QApplication([])
window = MyGui()
app.exec_()