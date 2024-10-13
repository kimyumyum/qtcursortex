import sys
from PyQt5.QtCore import pyqtSlot, QBasicTimer
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QTextCursor
from PyQt5.uic import loadUi

class MainPage(QMainWindow):
    def __init__(self):
        super(MainPage, self).__init__()
        loadUi('progress.ui', self)
        self.pushButton.clicked.connect(self.clickText)        
        self.pushButton.clicked.connect(self.startProgress)

        self.timer = QBasicTimer()
        self.step= 0
        
    def clickText(self):
        i= 0
        while i<10:
            self.lineEdit.setText('{0} clicked!'.format(str(i)))
            i+=1
    def startProgress(self):
        if self.timer.isActive():
                self.timer.stop()
        else:
            #self.timer.start(100, self)
            self.progressBar.setValue(100.5)
    def timerEvent(self, event):
        if self.step >= 100:
            self.timer.stop()
            return
        self.step += 1
        self.progressBar.setValue(self.step)
        
            
app = QApplication(sys.argv)
widget = MainPage()
widget.show()
sys.exit(app.exec_())
