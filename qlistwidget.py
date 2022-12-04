import sys
from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Two QListWidget Window')


        # 첫 번째 QListWidget 추가

        self.listwidget1 = QListWidget(self)
        self.listwidget1.setGeometry(10, 10, 150, 100)

        # 지정한 행 위치에 값 추가
        self.listwidget1.insertItem(0, "Chrome")
        self.listwidget1.insertItem(1, "Explorer")
        self.listwidget1.insertItem(2, "Firefox")
        self.listwidget1.insertItem(4, "Edge")

        self.listwidget2 = QListWidget(self)
        self.listwidget2.setGeometry(300, 10, 150, 100)

        self.left_button = QPushButton(self)
        self.left_button.move(180, 20)
        self.left_button.setText('-->')

        self.right_button = QPushButton(self)
        self.right_button.move(180, 60)
        self.right_button.setText('<--')

        self.left_button.clicked.connect(self.clicked_left_button)
        self.right_button.clicked.connect(self.clicked_right_button)

    def clicked_left_button(self):
        self.move_current_item(self.listwidget1, self.listwidget2)

    def clicked_right_button(self):
        self.move_current_item(self.listwidget2, self.listwidget1)

    def move_current_item(self, src, dst):
        if src.currentItem():
            row = src.currentRow()
            dst.addItem(src.takeItem(row))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())