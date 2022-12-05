import sys
from PyQt5.QtWidgets import *
   
    
class MyWindow(QMainWindow):
         
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setGeometry(1000, 200, 300, 300)

        te = QLineEdit(self)
        te.textChanged.connect(self.fun_te_changed)
        te.editingFinished.connect(self.fun_te_editfinished)
        te.returnPressed.connect(self.fun_te_returnPressed)
       
    def fun_te_changed(self):
        print("event 발생")

    def fun_te_editfinished(self):
        print("edit finish event 발생")
        
    def fun_te_returnPressed(self):
        print("return press event 발생")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
