#trying to display word under cursor
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QTextCursor
from PyQt5.uic import loadUi

class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        loadUi('textcursor.ui', self)

        self.inputText.cursorPositionChanged.connect(self.showWord)
        self.pushButton.clicked.connect(self.clickText)        

#datamuse lineedit button connect check
        self.jjaButton.clicked.connect(self.setjjaText)
        self.jjbButton.clicked.connect(self.setjjbText)
        self.synButton.clicked.connect(self.setsynText)
        self.trgButton.clicked.connect(self.settrgText)
        self.antButton.clicked.connect(self.setantText)
        self.spcButton.clicked.connect(self.setspcText)
        self.genButton.clicked.connect(self.setgenText)
        self.comButton.clicked.connect(self.setcomText)
        self.parButton.clicked.connect(self.setparText)
        self.bgaButton.clicked.connect(self.setbgaText)
        self.bgbButton.clicked.connect(self.setbgbText)
        
           
        

    def setjjaText(self):
        self.jjaLineEdit.setText('clicked')
    def setjjbText(self):
        self.jjbLineEdit.setText('clicked')
    def setsynText(self):
        self.synLineEdit.setText('clicked')
    def settrgText(self):
        self.trgLineEdit.setText('clicked')
    def setantText(self):
        self.antLineEdit.setText('clicked')
    def setspcText(self):
        self.spcLineEdit.setText('clicked')
    def setgenText(self):
        self.genLineEdit.setText('clicked')
    def setcomText(self):
        self.comLineEdit.setText('clicked')
    def setparText(self):
        self.parLineEdit.setText('clicked')
    def setbgaText(self):
        self.bgaLineEdit.setText('clicked')
    def setbgbText(self):
        self.bgbLineEdit.setText('clicked')


    def showWord(self):
        tcursor = self.inputText.textCursor()
        tcursor.select(tcursor.WordUnderCursor)
        selectedWord = tcursor.selectedText()
        self.answerLine.setText(selectedWord)
        print(selectedWord)

    def clickText(self):
        print('ok')

    #testing cursor and position thigns    
    def testCursor(self):
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
