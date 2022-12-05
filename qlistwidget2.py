import sys

from PIL import Image

from PyQt5.QtWidgets import QApplication, QListWidget, \
    QListWidgetItem, QMainWindow, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

import clipboard

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = Service(r'C:\chromedriver.exe')
browser = webdriver.Chrome(service=service, options=chrome_options)



class myItem(QListWidgetItem):
    link = ""
    zh = ""

    def __init__(self, text):
        super().__init__(text)

    def setLink(self, text):
        self.link = text

    def setZh(self, text):
        self.zh = text

    def getZh(self):
        return self.zh

    def printLink(self):
        print("호출!")
        print(self.link)

    def getLink(self):
        return self.link

    

    

        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 500) #x, y, w, h
        self.setWindowTitle('status Window')

        self.listwidget = QListWidget(self)
        self.listwidget.resize(500, 200)

        self.entry_title_lbl = QLabel(self)
        self.entry_title_lbl.move(0, 200)

        self.hanja_list_lbl = QLabel(self)
        self.hanja_list_lbl.move(0, 300)

        self.mean_list_lbl = QLabel(self)
        self.mean_list_lbl.move(0, 350)

       

         # 시그널 연결
        self.listwidget.itemSelectionChanged.connect(self.selectchanged_listwidget)
        self.listwidget.itemDoubleClicked.connect(self.clipboard_copy)

        # --- 삭제 버튼 생성
        self.delete_button = QPushButton(self)
        self.delete_button.move(400, 5)
        self.delete_button.setText('Delete')

        # 삭제 시그널
        self.delete_button.clicked.connect(self.clicked_delete_button)

        self.qle = QLineEdit(self)
        self.qle.move(600, 5)
        self.qle.returnPressed.connect(self.pressEnter)
        
    def clipboard_copy(self):
        print('더블클릭 발생')
        for item in self.listwidget.selectedItems():
            clipboard.copy(item.getZh())

    def selectchanged_listwidget(self):
        lst_item = self.listwidget.selectedItems() # 선택된 데이터 체크
        
        # 선택된 데이터 출력
        for item in lst_item:
            print(item.text())
            browser.get('https://hanja.dict.naver.com/' + item.getLink())
            time.sleep(0.3)

            path = r"D:\pyq5연습\test.png"

            #초기파일
            browser.find_element(By.CSS_SELECTOR, '.entry_title._guide_lang').screenshot("entry_title.png")
            browser.find_element(By.CSS_SELECTOR, '.hanja_list').screenshot('hanja_list.png')   
            browser.find_element(By.CSS_SELECTOR, '.mean_list.my_mean_list').screenshot('mean_list.png')

            #원래사진으로 나오게하기전

            pixmap = QPixmap('entry_title.png')
            self.entry_title_lbl.setPixmap(pixmap)
            self.entry_title_lbl.adjustSize()

            pixmap = QPixmap('hanja_list.png')
            self.hanja_list_lbl.setPixmap(pixmap)
            self.hanja_list_lbl.adjustSize()

            pixmap = QPixmap('mean_list.png')
            self.mean_list_lbl.setPixmap(pixmap)
            self.mean_list_lbl.adjustSize()


    def pressEnter(self):
        
        keyword = self.qle.text()
        self.listwidget.clear()
        
        browser.get('https://hanja.dict.naver.com/#/search?query=' + keyword)
        time.sleep(0.2)

        soup = BeautifulSoup(browser.page_source, "html.parser")

        for i in soup.select('#searchPage_entry > .component_keyword.has-saving-function > .row'):

            origin = i.select_one('a[href]')

            link = origin.attrs["href"]

            zh = origin.text
            zh = re.sub('\t|\n', "", zh)
            
            mean = i.select_one('.mean').text
            
            txt = i.select_one('.mean_list').text
            txt = re.sub('\t|\n', "", txt)
            txt = re.sub("([2-9])", "\n\\1", txt)

            item = myItem(zh + ' '+ mean + '\n' + txt + '\n')
            item.setLink(link)
            item.setZh(zh)

            
            self.listwidget.addItem(item)
            #self.listwidget
            
        
    def clicked_delete_button(self):
        # 선택된 데이터가 있는지 체크
        lst_modelindex = self.listwidget.selectedIndexes()
        for item in self.listwidget.selectedItems():
            
            item.printLink()
          
        # 선택된 데이터 삭제
        for modelindex in lst_modelindex:
            print(modelindex.row())
            self.listwidget.model().removeRow(modelindex.row())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())



