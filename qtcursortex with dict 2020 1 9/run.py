import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QTextCursor
from PyQt5.uic import loadUi

class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        loadUi('textcursor.ui', self)
        self.pushButton.clicked.connect(self.clickText)        
                       
        
    def clickText(self):
        self.posLabel.setText('clicked!')
        tcursor = self.inputText.textCursor()
        tcursor.movePosition(tcursor.NextWord, tcursor.MoveAnchor,1)
        tcursor.insertText("(^_^)")
        self.inputText.setTextCursor(tcursor)
        #self.inputText.find("extraction")
        #self.inputText.moveCursor(
        #print(str(self.inputText.QTextCursor.position()))
        #print(self.inputText.QText


app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())
