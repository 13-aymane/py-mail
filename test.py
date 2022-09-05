import sys
from PyQt5.QtWidgets import (QLineEdit, QLabel, QGridLayout, QWidget, 
                             QPushButton, QApplication, QSpinBox)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.home()

    def home(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.label = QLabel(self)
        self.label.setText("NO")
        self.grid.addWidget(self.label, 0, 1)

#        self.input1 = QLineEdit(self)
        self.input1 = QSpinBox(self)           # +++
        self.input1.setMinimum(1)
        self.input1.setMaximum(12)
        self.input1.setValue(3)

        self.grid.addWidget(self.input1, 0, 5)

        self.pushButton_ok = QPushButton("Press me", self)
        self.pushButton_ok.clicked.connect(self.addtextbox) #(self.addCheckbox)
        self.grid.addWidget(self.pushButton_ok, 0, 10)



    def addtextbox(self):
        countLayout = self.layout().count()
        if countLayout > 3:
            for it in range(countLayout - 3):  
                w = self.layout().itemAt(3).widget()
                self.layout().removeWidget(w)     
                w.hide()
        self.lineEdits = []   # +++

        for n in range(self.input1.value()):
            self.bursttime = QLabel(self)
            self.bursttime.setText("b_{}".format(n))

            self.timeinput = QLineEdit(self)
            self.timeinput.textChanged.connect(lambda text, i=n : self.editChanged(text, i)) # +++

            self.grid.addWidget(self.bursttime, 2*n+1, 0)
            self.grid.addWidget(self.timeinput, 2*n+1, 1)

            self.lineEdits.append('')                                                        # +++

        self.go = QPushButton("GO") #, self)
        self.grid.addWidget(self.go, 2*n+2, 0)
        self.go.clicked.connect(self.printvalues)

    def printvalues(self):  
        # fetch data in some way  
        for i, v in enumerate(self.lineEdits):                                               # +++
            print("bursttime: b_{}, timeinput: {}".format(i, v))                             # +++


    def editChanged(self, text, i):   # +++
        self.lineEdits[i] = text      # +++

    def addCheckbox(self):
        print("def addCheckbox(self):")

if __name__ == "__main__":
    application = QApplication(sys.argv)
    window = Window()
    window.setWindowTitle('Dynamically adding textboxes using a push button')
    window.resize(250, 180)
    window.show()
    sys.exit(application.exec_())