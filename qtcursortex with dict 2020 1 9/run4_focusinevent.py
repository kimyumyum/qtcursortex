import sys
import re
import dm
from PyQt5.QtCore import pyqtSlot, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QTextCursor
from PyQt5.uic import loadUi
from PyQt5 import QtSql

class MainPage(QMainWindow):
    #TO DO: lineToTable
    #
    #
    a = 777
    def __init__(self):
        #initialize
        super(MainPage, self).__init__()
        loadUi('textcursor.ui', self)
    
        
        
        self.maxDisplay = 100 #max number of dm search
        self.tableC = 3         #table column number
        self.tableR = 34        #table row number
        self.globalDict = {}  #diction where dm results are saved as list of string
 
         
        #left TextEdit on click. show word on the LineEdit below
        self.inputText.cursorPositionChanged.connect(self.showWord)
    
        #run all DM operations
        self.workButton.clicked.connect(self.clickAll)        
        
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


        self.jjaLineEdit.installEventFilter(self)
        self.jjbLineEdit.installEventFilter(self)
        self.synLineEdit.installEventFilter(self)
        self.trgLineEdit.installEventFilter(self)
        self.antLineEdit.installEventFilter(self)
        self.spcLineEdit.installEventFilter(self)
        self.genLineEdit.installEventFilter(self)
        self.comLineEdit.installEventFilter(self)
        self.parLineEdit.installEventFilter(self)
        self.bgaLineEdit.installEventFilter(self)
        self.bgbLineEdit.installEventFilter(self)
        
    
        #connect lineEdit to return pressed
        # self.jjaLineEdit.returnPressed.connect(self.lineToTable(self.jja))

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FocusIn:
            if obj == self.jjaLineEdit:
                print("jja focus")
                self.addToTable('jja')
            elif obj == self.jjbLineEdit:
                print("jjb focus")
                self.addToTable('jjb')
            elif obj == self.synLineEdit:
                print("syn focus")
                self.addToTable('syn')
            elif obj == self.trgLineEdit:
                print("trg focus")
                self.addToTable('trg')
            elif obj == self.antLineEdit:
                print("ant focus")
                self.addToTable('ant')
            elif obj == self.spcLineEdit:
                print("spc focus")
                self.addToTable('spc')
            elif obj == self.genLineEdit:
                print("gen focus")
                self.addToTable('gen')
            elif obj == self.comLineEdit:
                print("com focus")
                self.addToTable('com')
            elif obj == self.parLineEdit:
                print("par focus")
                self.addToTable('par')
            elif obj == self.bgaLineEdit:
                print("bga focus")
                self.addToTable('bga')
            elif obj == self.bgbLineEdit:
                print("bgb focus")
                self.addToTable('bgb')
                
          #  elif obj == self.comboBox:
             #   print("combobox")
        return super(MainPage, self).eventFilter(obj, event)
    


    def addToTable(self, word):
                      
        if word not in self.globalDict:
            return
        
        temp = self.globalDict.get(word)
        
        # clear table /        for list,          fill the table
        self.fullTableWidget.clearContents()
        self.fullTableWidget.setColumnCount(self.tableC)    #index 0~2
        self.fullTableWidget.setRowCount(self.tableR)       #index 0~34

        

        listLength = len(temp)
        #for item in temp:
            
        itemCount = 0
        i=0
        while (i<self.tableR):
            if itemCount >= listLength:
                break
            
            j = 0
            while (j<self.tableC):
                if itemCount >= listLength:
                    break
                self.fullTableWidget.setItem(i,j,QTableWidgetItem(temp[itemCount-1]))
                itemCount += 1
                j += 1
            i += 1
        #print(str(itemCount))
        #self.fullTableWidget.setItem(1,1,QTableWidgetItem("first item"))
        
        
    def lineToTable(self, word):
        #print(self.globalDict.get(word)[0])
        print(word)

       
        '''
        tcursor = self.jjaLineEdit.textCursor()
        tcursor.select(tcursor.WordUnderCursor)
        selectedWord = tcursor.selectedText()
        selectedWord = self.removeSpecialCharacter(selectedWord)
        print(selectedWord)
        self.answerLine.setText(selectedWord)
        '''
        #return word        

    def getSynStringList(self, word):
        #get datamuse synonym of WORD and then return it as string list
        someDict = dm.syn(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList
    
    def getJjaStringList(self, word):
        #get datamuse jja of WORD and then return it as string list
        someDict = dm.jja(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList

    def getJjbStringList(self, word):
        #get datamuse jjb of WORD and then return it as string list
        someDict = dm.jjb(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList

    def getTrgStringList(self, word):
        #get datamuse trg of WORD and then return it as string list
        someDict = dm.trg(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList

    def getAntStringList(self, word):
        #get datamuse ant of WORD and then return it as string list
        someDict = dm.ant(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList

    def getSpcStringList(self, word):
        #get datamuse spc of WORD and then return it as string list
        someDict = dm.spc(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList

    def getGenStringList(self, word):
        #get datamuse gen of WORD and then return it as string list
        someDict = dm.gen(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList        

    def getComStringList(self, word):
        #get datamuse com of WORD and then return it as string list
        someDict = dm.com(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList

    def getParStringList(self, word):
        #get datamuse par of WORD and then return it as string list
        someDict = dm.par(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList

    def getBgaStringList(self, word):
        #get datamuse ant of WORD and then return it as string list
        someDict = dm.bga(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList        

    def getBgbStringList(self, word):
        #get datamuse ant of WORD and then return it as string list
        someDict = dm.bgb(word, self.maxDisplay)
        sList = self.convertToStringList(someDict)
        return sList      
    
        
        
    
    def printStringList(self, sList):
        #print out list of string
        for x in range(len(sList)): 
            print (sList[x])
            

    def clickAll(self):
        self.setjjaText()
        self.setjjbText()
        self.setsynText()
        self.settrgText()
        self.setantText()
        self.setspcText()
        self.setgenText()
        self.setcomText()
        self.setparText()
        self.setbgaText()
        self.setbgbText()
        
        

    #check list functionality
    def addItem(self):
        print("add item here")
        self.fullListWidget.addItem("Hello")

    def addItems(self, wordList):
        wordList = self.convertToStringList(wordList)
        print("add item here")
        self.fullListWidget.addItems(wordList)       

    def convertToStringList(self, someDict):
        someStringList = []
        for item in someDict:
            temp = item['word'] 
            someStringList.append(temp)
        return someStringList

    #accept a string list, return a string in a concatenated string of maxNumber of elements
    def showWords(self, stringList, maxNumber = 3):
        #if list is empty, return
        if not stringList:
            return

        length = len(stringList)
        smallList =stringList[:maxNumber]
        words = ' / '.join(smallList)
        print (words)                    
        return words
        


    #set lineedit for each 
    def setjjaText(self):
        #self.jjaLineEdit.setText('clicked')
        self.a = 5
      #  print('inside setjjaText: '+str(self.a))
        word = self.answerLine.text()
        if not word:
            self.jjaLineEdit.setText('nothing entered!')
        else:
            stringList= self.getJjaStringList(word)
            self.jjaLineEdit.setText(self.showWords(stringList))
            self.globalDict['jja'] = stringList[:]
                        
        
    def setjjbText(self):
        word = self.answerLine.text()
        if not word:
            self.jjbLineEdit.setText('nothing entered!')
        else:
            stringList= self.getJjbStringList(word)
            self.jjbLineEdit.setText(self.showWords(stringList))
            self.globalDict['jjb'] = stringList[:]
            
    def setsynText(self):
        word = self.answerLine.text()
        if not word:
            self.synLineEdit.setText('nothing entered!')
        else:
            stringList= self.getSynStringList(word)
            self.synLineEdit.setText(self.showWords(stringList))
            self.globalDict['syn'] = stringList[:]
            
    def settrgText(self):
        word = self.answerLine.text()
        if not word:
            self.trgLineEdit.setText('nothing entered!')
        else:
            stringList= self.getTrgStringList(word)
            self.trgLineEdit.setText(self.showWords(stringList))
            self.globalDict['trg'] = stringList[:]
            
    def setantText(self):
        word = self.answerLine.text()
        if not word:
            self.antLineEdit.setText('nothing entered!')
        else:
            stringList= self.getAntStringList(word)
            self.antLineEdit.setText(self.showWords(stringList))
            self.globalDict['ant'] = stringList[:]
            
    def setspcText(self):
        word = self.answerLine.text()
        if not word:
            self.spcLineEdit.setText('nothing entered!')
        else:
            stringList= self.getSpcStringList(word)
            self.spcLineEdit.setText(self.showWords(stringList))
            self.globalDict['spc'] = stringList[:]
            
    def setgenText(self):
        word = self.answerLine.text()
        if not word:
            self.genLineEdit.setText('nothing entered!')
        else:
            stringList= self.getGenStringList(word)
            self.genLineEdit.setText(self.showWords(stringList))
            self.globalDict['gen'] = stringList[:]
            
    def setcomText(self):
        word = self.answerLine.text()
        if not word:
            self.comLineEdit.setText('nothing entered!')
        else:
            stringList= self.getComStringList(word)
            self.comLineEdit.setText(self.showWords(stringList))
            self.globalDict['com'] = stringList[:]
            
    def setparText(self):
        word = self.answerLine.text()
        if not word:
            self.parLineEdit.setText('nothing entered!')
        else:
            stringList= self.getParStringList(word)
            self.parLineEdit.setText(self.showWords(stringList))
            self.globalDict['par'] = stringList[:]
            
    def setbgaText(self):
        word = self.answerLine.text()
        if not word:
            self.bgaLineEdit.setText('nothing entered!')
        else:
            stringList= self.getBgaStringList(word)
            self.bgaLineEdit.setText(self.showWords(stringList))
            self.globalDict['bga'] = stringList[:]
            
    def setbgbText(self):
        word = self.answerLine.text()
        if not word:
            self.bgbLineEdit.setText('nothing entered!')
        else:
            stringList= self.getBgbStringList(word)
            self.bgbLineEdit.setText(self.showWords(stringList))
            self.globalDict['bgb'] = stringList[:]


    def showWord(self):
        tcursor = self.inputText.textCursor()
        tcursor.select(tcursor.WordUnderCursor)
        selectedWord = tcursor.selectedText()
        selectedWord = self.removeSpecialCharacter(selectedWord)
        print(selectedWord)
        self.answerLine.setText(selectedWord)

    
    
    #regex remove special character
    def removeSpecialCharacter(self, word):
        newWord =  re.sub('[^A-Za-z0-9]+', "", word)
        return newWord
        
    
    def clickText(self):
        print('ok')

    #testing cursor and position thigns    
    def testCursor(self):
        self.workLabel.setText('clicked!')
        tcursor = self.inputText.textCursor()
        tcursor.movePosition(tcursor.NextWord, tcursor.MoveAnchor,1)
        tcursor.insertText("(^_^)")
        self.inputText.setTextCursor(tcursor)
        #self.inputText.find("extraction")
        #self.inputText.moveCursor(
        #print(str(self.inputText.QTextCursor.position()))
        #print(self.inputText.QText

    def closeEvent(self, event):
         print("Close Test 1")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainPage()
    widget.show()
    sys.exit(app.exec_())
