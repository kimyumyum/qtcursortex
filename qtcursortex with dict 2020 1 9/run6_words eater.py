#use v5 to make a db feeder. Feed in all the words from the file

import sys
import re
import dm
from PyQt5.QtCore import pyqtSlot, QEvent, QTextStream, QFile
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QTextCursor
from PyQt5.uic import loadUi
from PyQt5 import QtSql
from nltk_stemmer import *
from nltk.corpus import stopwords

class MainPage(QMainWindow):
    def __init__(self):
        #initialize
        super(MainPage, self).__init__()
        loadUi('textcursor.ui', self)
    
        
        self.maxDisplay = 100 #max number of dm search
        self.tableC = 3         #table column number
        self.tableR = 34        #table row number
        self.globalDict = {}  #dictionary where dm results are saved as list of string
        self.wList=[]
        self.textEditWordList=[] #words from inputTextEdit
                
        #init database
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("wordbank.db")
        print(self.db.open())
        self.q = QtSql.QSqlQuery()
        print("creating table in the database: "+str(self.q.exec("CREATE TABLE dm (word TEXT UNIQUE NOT NULL, freq INTEGER DEFAULT 0, jja TEXT DEFAULT NULL, jjb TEXT DEFAULT NULL, syn TEXT DEFAULT NULL, trg TEXT DEFAULT NULL, ant TEXT DEFAULT NULL, spc TEXT DEFAULT NULL, gen TEXT DEFAULT NULL, com TEXT DEFAULT NULL, par TEXT DEFAULT NULL, bga TEXT DEFAULT NULL, bgb TEXT DEFAULT NULL)"))) 

        self.startWList()

        #check buttons
        self.openFileButton.clicked.connect(self.fileOpen)
        self.allWordsButton.clicked.connect(self.textEditToWords)
        self.progressBar.setValue(0)
             
        #left TextEdit on click. show word on the LineEdit below
        self.inputText.cursorPositionChanged.connect(self.showWord)
    
        #run all DM operations
        self.workButton.clicked.connect(self.clickAll)        

        #toSimpleButton connect 
        self.toSimpleButton.clicked.connect(self.toSimpleForm)        
        
        #datamuse lineedit button connect check
        #self.jjaButton.clicked.connect(lambda: self.setjjaText(word))
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



    def someShit(self,word=''):
        if not word:
            word=''
        print('tword is {}'.format(word))
        print('1st the type is: {0} and {1}'.format(type(word), word))

            
    #testing cursor and position thigns    
    def moveCursor(self):
        tcursor = self.inputText.textCursor()
        tcursor.movePosition(tcursor.Start, tcursor.MoveAnchor,1)
        self.inputText.setTextCursor(tcursor)
        
    def fileOpen(self):
        #name = ()
        name = QFileDialog.getOpenFileName()
        #print(type(name))
        file = QFile(name[0])
        if not(file.open(QFile.ReadOnly)):
            print('file can\'t be opened for some reason')
            return
        
        texts = QTextStream(file)
        self.inputText.clear()
        while not texts.atEnd():
            text = texts.readLine()
            self.inputText.append(text)
            #print(text)
        self.moveCursor()            
            
    #file = QFile(open(name[0], 'r', encoding='UTF8')
       #file = open(name[0], 'r', encoding='UTF8')
       #texts = QTextStream(file)

    def textEditToWords(self):
        del self.textEditWordList
        self.textEditWordList = re.split('[^A-Za-z0-9]+',self.inputText.toPlainText())

        count =0
        size = len(self.textEditWordList)
        for word in self.textEditWordList:
            self.clickAll(word)
            count += 1 
            self.progressBar.setValue((count/size)*100)

        print('\n\n****Finished feeding words to DB****')
        
        
    #regex remove special character
    def removeSpecialCharacter(self, word):
        newWord =  re.sub('[^A-Za-z0-9]+', "", word)
        return newWord
    
    
    def startWList(self):
        print('fetching words from db: '+ str(self.q.exec("SELECT word from dm")))

        while(self.q.next()):
           self.wList.append(self.q.value(0))

        #print('items in the wList: ')
        #for item in self.wList:
        #    print(item)
            
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

    #save word search  result in the database
    #def insertDB(self, word):
        
    


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
            
    def toSimpleForm(self, word=''):
        if not word:
            word = self.answerLine.text()
            if word=='':
                return
        
        convertedNoun = toSimpleNoun(word)
        print('WORD: {0}   NOUNFORM: {1}'.format(word,convertedNoun))
        self.nounSimpleLineEdit.setText(convertedNoun)
        convertedVerb = toSimpleVerb(word)
        print('WORD: {0}   VERBFORM: {1}'.format(word,convertedVerb))
        self.verbSimpleLineEdit.setText(convertedVerb)

    def searchAll(self, word=''):
        self.setjjaText(word)
        self.setjjbText(word)
        self.setsynText(word)
        self.settrgText(word)
        self.setantText(word)
        self.setspcText(word)
        self.setgenText(word)
        self.setcomText(word)
        self.setparText(word)
        self.setbgaText(word)
        self.setbgbText(word)  
        
    def clickAll(self, word=''):
           
        if not word:
            word = self.answerLine.text()
            if word=='':
                return
            
        word = word.lower()    
        stopWords = set(stopwords.words('english'))       

        if word in stopWords:
            print('## {} is a stopword'.format(word))
            return

        if word in self.wList:
            print('word is in a wList.')
            return
        
        self.toSimpleForm(word)

        #search default clicked word, and then add to DB       
        self.searchAll(word)
        self.wordToDB(word)
        
        #if simple nounform exist,search it, and then add to DB       
        nounFormWord = self.nounSimpleLineEdit.text()
        if word != nounFormWord:
            self.searchAll(nounFormWord)
            self.wordToDB(nounFormWord)

        #if simple verbform exist,search it, and then add to DB       
        verbFormWord = self.verbSimpleLineEdit.text()
        if word != verbFormWord:
            self.searchAll(verbFormWord)
            self.wordToDB(verbFormWord)
                

    def wordToDB(self, word):
        if word in self.wList:
            return
        else:
            self.addToDB(word)
            self.wList.append(word)

    def addToDB(self, word):
        #if word not in wList, add to DB    

        self.q.prepare("INSERT INTO dm(word, freq, jja, jjb, syn, trg, ant, spc, gen, com, par, bga, bgb)" "VALUES (:word, :freq, :jja, :jjb, :syn, :trg, :ant, :spc, :gen, :com, :par, :bga, :bgb)")
        self.q.bindValue(":word", word)
        self.q.bindValue(":freq", 1)
        self.q.bindValue(":jja", ",".join(self.globalDict['jja']))
        self.q.bindValue(":jjb", ",".join(self.globalDict['jjb']))
        self.q.bindValue(":syn", ",".join(self.globalDict['syn']))
        self.q.bindValue(":trg", ",".join(self.globalDict['trg']))
        self.q.bindValue(":ant", ",".join(self.globalDict['ant']))
        self.q.bindValue(":spc", ",".join(self.globalDict['spc']))
        self.q.bindValue(":gen", ",".join(self.globalDict['gen']))
        self.q.bindValue(":com", ",".join(self.globalDict['com']))
        self.q.bindValue(":par", ",".join(self.globalDict['par']))
        self.q.bindValue(":bga", ",".join(self.globalDict['bga']))
        self.q.bindValue(":bgb", ",".join(self.globalDict['bgb']))
        print('['+word+'] prepared insert - '+str(self.q.exec()))

    #check list functionality
    def addItem(self):
        print("add item here")
        self.fullListWidget.addItem("Hello")

    def addItems(self):
        #wordList = self.convertToStringList(wordList)
        print("add item here")
        self.fullListWidget.addItems(self.wList)       
    
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
        #print (words)                    
        return words
        
    def stringToList(self, someString):
        text.split()

    #set lineedit for each 
    def setjjaText(self, word=''):
        #  print('inside setjjaText: '+str(self.a))
        stringList=[]
        self.jjaLineEdit.clear()
        if word=='':
            word = self.answerLine.text()

        if not word:
            self.jjaLineEdit.setText('nothing entered!')
            return
        elif word in self.wList:
            self.q.prepare("SELECT jja FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
            #print('jja db works?: ' + str(self.q.exec("SELECT jja FROM WHERE word ="+word)))
        else:
            stringList= self.getJjaStringList(word)

        self.jjaLineEdit.setText(self.showWords(stringList))
        self.globalDict['jja'] = stringList[:]
                        
    #def addToDict(self, word):
        

    # fetch word from answerLine, get dm result as sList,
    # show word in the line edit, save sList in the dictionary    
    def setjjbText(self, word=''):
        stringList=[]
        self.jjbLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.jjbLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT jjb FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getJjbStringList(word)

        self.jjbLineEdit.setText(self.showWords(stringList))
        self.globalDict['jjb'] = stringList[:]
        
    def setsynText(self, word=''):
        stringList=[]
        self.synLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.synLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT syn FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getSynStringList(word)

        self.synLineEdit.setText(self.showWords(stringList))
        self.globalDict['syn'] = stringList[:]
        
    def settrgText(self, word=''):
        stringList=[]
        self.trgLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.trgLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT trg FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getTrgStringList(word)

        self.trgLineEdit.setText(self.showWords(stringList))
        self.globalDict['trg'] = stringList[:]
        
    def setantText(self, word=''):
        stringList=[]
        self.antLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.antLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT ant FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getAntStringList(word)

        self.antLineEdit.setText(self.showWords(stringList))
        self.globalDict['ant'] = stringList[:]
        
    def setspcText(self, word=''):
        stringList=[]
        self.spcLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.spcLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT spc FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getSpcStringList(word)

        self.spcLineEdit.setText(self.showWords(stringList))
        self.globalDict['spc'] = stringList[:]
        
    def setgenText(self, word=''):
        stringList=[]
        self.genLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.genLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT gen FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getGenStringList(word)

        self.genLineEdit.setText(self.showWords(stringList))
        self.globalDict['gen'] = stringList[:]
        
    def setcomText(self, word=''):
        stringList=[]
        self.comLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.comLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT com FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getComStringList(word)

        self.comLineEdit.setText(self.showWords(stringList))
        self.globalDict['com'] = stringList[:]
        
    def setparText(self, word=''):
        stringList=[]
        self.parLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.parLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT par FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getParStringList(word)

        self.parLineEdit.setText(self.showWords(stringList))
        self.globalDict['par'] = stringList[:]
        
    def setbgaText(self, word=''):
        stringList=[]
        self.bgaLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.bgaLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT bga FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getBgaStringList(word)

        self.bgaLineEdit.setText(self.showWords(stringList))
        self.globalDict['bga'] = stringList[:]
        
    def setbgbText(self, word=''):
        stringList=[]
        self.bgbLineEdit.clear()
        if word=='':
            word = self.answerLine.text()
        if not word:
            self.bgbLineEdit.setText('nothing entered!')
        elif word in self.wList:
            self.q.prepare("SELECT bgb FROM dm WHERE word = :word")
            self.q.bindValue(":word",word)
            self.q.exec()
            self.q.next()
            stringList= self.q.value(0).split(',')
        else:
            stringList= self.getBgbStringList(word)

        self.bgbLineEdit.setText(self.showWords(stringList))
        self.globalDict['bgb'] = stringList[:]


    def showWord(self):
        tcursor = self.inputText.textCursor()
        tcursor.select(tcursor.WordUnderCursor)
        selectedWord = tcursor.selectedText()
        selectedWord = self.removeSpecialCharacter(selectedWord)
        #print(selectedWord)
        self.answerLine.setText(selectedWord.lower())
    
    def clickText(self):
        print('ok')



    def closeEvent(self, event):
         print(self.db.close())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainPage()
    widget.show()
    sys.exit(app.exec_())
