#use v5 to make a db feeder. Feed in all the words from the file
import logging
import sys
import re
import dm
from PyQt5.QtCore import *
#pyqtSlot, QEvent, QTextStream, QFile
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QTextCursor, QFont, QTextFormat, QTextCharFormat, QBrush, QColor
from PyQt5.uic import loadUi
from PyQt5 import QtSql
from nltk_stemmer import *
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = 'log.txt',
                    level = logging.DEBUG,
                    format = LOG_FORMAT)
logger=logging.getLogger()
CIRCLE_ONE = '①'
CIRCLE_TWO = '②'
CIRCLE_THREE = '③'
CIRCLE_FOUR = '④'
CIRCLE_FIVE = '⑤'

class MainPage(QMainWindow):
    '''class variable'''
    
    
    def __init__(self):
        #initialize
        logger.info("Initialize Main Page")
        super(MainPage, self).__init__()
        loadUi('newStart.ui', self)

        #order question variable
        self.tokens={'g':[], 'a':[] ,'b':[], 'c':[]}
        #insertion question variable
        self.insertionTokens=[]
        #irrelevant question variable
        self.irreTokens=[]
        
        
        self.astrix=''
        self.tempTxt=''

        #left TextEdit on click. show word on the LineEdit below
        self.inputText.cursorPositionChanged.connect(self.showWord)
        
        # self.writeFileButton.clicked.connect(self.fileWrite)
        self.openFileButton.clicked.connect(self.fileOpen)
        self.fireButton.clicked.connect(self.testFire)
        self.boldButton.clicked.connect(self.testBold)
        self.underlineButton.clicked.connect(self.testUnderline)
        self.italicButton.clicked.connect(self.testItalic)
        self.highlightButton.clicked.connect(self.testHighlight)
        self.sentTokenizeButton.clicked.connect(self.sentTokenize)

        #second tab 순서맞추기 버튼
        self.givenDownButton.clicked.connect(self.givenDown)  
        self.firstDownButton.clicked.connect(self.firstDown)
        self.secondDownButton.clicked.connect(self.secondDown)
        self.firstUpButton.clicked.connect(self.firstUp)
        self.secondUpButton.clicked.connect(self.secondUp)
        self.thirdUpButton.clicked.connect(self.thirdUp)    
        #show number of sentences and total size
        self.givenText.textChanged.connect(self.showGivenLength)
        self.firstText.textChanged.connect(self.showFirstLength)
        self.secondText.textChanged.connect(self.showSecondLength)
        self.thirdText.textChanged.connect(self.showThirdLength)

        #option type A-B-C radio buttons
        self.optionTypeABCButtonOne.toggled.connect(self.ABCOneCLicked)
        self.optionTypeABCButtonTwo.toggled.connect(self.ABCTwoCLicked)
        self.optionTypeABCButtonThree.toggled.connect(self.ABCThreeCLicked)
        self.optionTypeABCButtonFour.toggled.connect(self.ABCFourCLicked)
        self.optionTypeABCButtonFive.toggled.connect(self.ABCFiveCLicked)

        #copies to clipboard when clicked
        self.givenCopyButton.clicked.connect(self.givenCopy)
        self.firstCopyButton.clicked.connect(self.firstCopy)
        self.secondCopyButton.clicked.connect(self.secondCopy)
        self.thirdCopyButton.clicked.connect(self.thirdCopy)

    
        '''
        insertion question tab events
        '''
        self.insertionAllocateButton.clicked.connect(self.insertionAllocate)

        #insertion choice radio button
        self.insertionOne.toggled.connect(self.insertionOneClicked)
        self.insertionTwo.toggled.connect(self.insertionTwoClicked)
        self.insertionThree.toggled.connect(self.insertionThreeClicked)
        self.insertionFour.toggled.connect(self.insertionFourClicked)
        self.insertionFive.toggled.connect(self.insertionFiveClicked)

        #copy
        self.insertionGivenCopyButton.clicked.connect(self.insertionGivenCopy)
        self.insertionTextCopyButton.clicked.connect(self.insertionTextCopy)        
        

        '''
        irrelevant question tab events
        '''
        self.irreAllocateButton.clicked.connect(self.irreAllocate)
        self.irreGivenCopyButton.clicked.connect(self.irreGivenCopy)
        self.irreTextCopyButton.clicked.connect(self.irreTextCopy)        
               

    '''
    irrelevant tab functions
    '''
    def irreGivenCopy(self):
        self.irreGivenText.selectAll()
        self.irreGivenText.copy()        
    def irreTextCopy(self):
        self.irreFullText.setText(' '.join(self.irreTokens))
        self.irreFullText.selectAll()
        self.irreFullText.copy()        
        
    def irreAllocate(self):
        self.irreTokens.clear()
        temp = self.tokenizeSent()
        if len(temp) < 5:
            self.irreAllocateLabel.setText('{} - not enough sents'.format(str(len(temp))))
            return
        self.irreTokens = self.addCircleNumber(temp)
        self.irreAllocateLabel.setText(
            '문장 수: {}\n *:'.format(len(self.irreTokens))+self.tempTxt)        
        self.irreFullText.setText('\n\n'.join(self.irreTokens))
    '''
    insertion tab functions
    '''

    def insertionGivenCopy(self):
        print('hi')
        self.insertionGivenText.selectAll()
        self.insertionGivenText.copy()    
    def insertionTextCopy(self):
        self.insertionFullText.selectAll()
        self.insertionFullText.copy()          
    def tokenizeSent(self):
        self.astrix=''
        self.tempTxt=''        
        temp = sent_tokenize(self.inputText.toPlainText())
        for i, t in enumerate(temp):
            if t[0].islower():
                temp[i-1:i+1]=[' '.join(temp[i-1:i+1])]
        if temp[-1][0]== '*':
            self.astrix = temp.pop()
            self.tempTxt='있음'
        else:
            self.tempTxt='없음'
        return temp
        
    def insertionAllocate(self):
        self.insertionTokens.clear()
        temp = self.tokenizeSent()
        if len(temp) < 7:
            self.insertionAllocateLabel.setText('{} - not enough sents'.format(str(len(temp))))
            return
        self.insertionTokens = temp
        self.insertionAllocateLabel.setText(
            '문장 수: {}\n *:'.format(len(self.insertionTokens))+self.tempTxt)
                
    def insertionOneClicked(self):
        if not self.insertionOne.isChecked() or not self.insertionTokens:
            return
        temp = self.insertionTokens[:]
        self.insertionGivenText.setText(temp.pop(-6))
        self.insertionFullText.setText(' '.join(self.addCircleNumber(temp)))
    
    def insertionTwoClicked(self):
        if not self.insertionTwo.isChecked() or not self.insertionTokens:
            return
        temp = self.insertionTokens[:]
        self.insertionGivenText.setText(temp.pop(-5))
        self.insertionFullText.setText(' '.join(self.addCircleNumber(temp)))        
    def insertionThreeClicked(self):
        if not self.insertionThree.isChecked() or not self.insertionTokens:
            return
        temp = self.insertionTokens[:]
        self.insertionGivenText.setText(temp.pop(-4))
        self.insertionFullText.setText(' '.join(self.addCircleNumber(temp)))       
    def insertionFourClicked(self):
        if not self.insertionFour.isChecked() or not self.insertionTokens:
            return
        temp = self.insertionTokens[:]
        self.insertionGivenText.setText(temp.pop(-3))
        self.insertionFullText.setText(' '.join(self.addCircleNumber(temp)))
     
    def insertionFiveClicked(self):
        if not self.insertionFive.isChecked() or not self.insertionTokens:
            return
        temp = self.insertionTokens[:]
        self.insertionGivenText.setText(temp.pop(-2))
        self.insertionFullText.setText(' '.join(self.addCircleNumber(temp)))
    
    #self.insertionFullText.setText(
    
        
    def addCircleNumber(self, temp):
        temp[-1] = '( {} ) '.format(CIRCLE_FIVE) + temp[-1]
        temp[-2] = '( {} ) '.format(CIRCLE_FOUR) + temp[-2]
        temp[-3] = '( {} ) '.format(CIRCLE_THREE) + temp[-3]
        temp[-4] = '( {} ) '.format(CIRCLE_TWO) + temp[-4]
        temp[-5] = '( {} ) '.format(CIRCLE_ONE) + temp[-5]        
        return temp
                
    def givenCopy(self):
        self.givenText.selectAll()
        self.givenText.copy()

    def firstCopy(self):
        self.firstText.selectAll()
        self.firstText.copy()

    def secondCopy(self):
        self.secondText.selectAll()
        self.secondText.copy()

    def thirdCopy(self):
        self.thirdText.append(self.astrix)
        self.thirdText.selectAll()
        self.thirdText.copy()

                    
    def ABCOneCLicked(self):
        if not self.optionTypeABCButtonOne.isChecked():
            return
        self.firstCopyButton.setText('A')
        self.secondCopyButton.setText('C')
        self.thirdCopyButton.setText('B')
        self.firstText.setText(' '.join(self.tokens['a']))
        self.secondText.setText(' '.join(self.tokens['c']))
        self.thirdText.setText(' '.join(self.tokens['b']))
       

            
    def ABCTwoCLicked(self):
        if not self.optionTypeABCButtonTwo.isChecked():
            return
        self.firstCopyButton.setText('B')
        self.secondCopyButton.setText('A')
        self.thirdCopyButton.setText('C')
        self.firstText.setText(' '.join(self.tokens['b']))
        self.secondText.setText(' '.join(self.tokens['a']))
        self.thirdText.setText(' '.join(self.tokens['c']))
        
    def ABCThreeCLicked(self):
        if not self.optionTypeABCButtonThree.isChecked():        
            return
        self.firstCopyButton.setText('B')
        self.secondCopyButton.setText('C')
        self.thirdCopyButton.setText('A')
        self.firstText.setText(' '.join(self.tokens['b']))
        self.secondText.setText(' '.join(self.tokens['c']))
        self.thirdText.setText(' '.join(self.tokens['a']))
        
    def ABCFourCLicked(self):
        if not self.optionTypeABCButtonFour.isChecked():
            return
        self.firstCopyButton.setText('C')
        self.secondCopyButton.setText('A')
        self.thirdCopyButton.setText('B')
        self.firstText.setText(' '.join(self.tokens['c']))
        self.secondText.setText(' '.join(self.tokens['a']))
        self.thirdText.setText(' '.join(self.tokens['b']))
        
            
    def ABCFiveCLicked(self):
        if not self.optionTypeABCButtonFive.isChecked():        
            return
        self.firstCopyButton.setText('C')
        self.secondCopyButton.setText('B')
        self.thirdCopyButton.setText('A')
        self.firstText.setText(' '.join(self.tokens['c']))
        self.secondText.setText(' '.join(self.tokens['b']))
        self.thirdText.setText(' '.join(self.tokens['a']))
        
            
    
    def showGivenLength(self):
        self.givenLabel.setText('{}/{}'.format(len(self.tokens['g']),str(len(self.givenText.toPlainText()))))
    def showFirstLength(self):
        self.firstLabel.setText('{}/{}'.format(len(self.tokens['a']),str(len(self.firstText.toPlainText()))))
    def showSecondLength(self):
        self.secondLabel.setText('{}/{}'.format(len(self.tokens['b']),str(len(self.secondText.toPlainText()))))
    def showThirdLength(self):
        self.thirdLabel.setText('{}/{}'.format(len(self.tokens['c']),str(len(self.thirdText.toPlainText()))))
                     
    def givenDown(self):
        if len(self.tokens['g']) < 2 :
            return
        
        self.tokens['a'].insert(0,self.tokens['g'].pop())
        self.givenText.setText(''.join(self.tokens['g']))
        self.firstText.setText(''.join(self.tokens['a']))
    def firstDown(self):
        if len(self.tokens['a']) < 2 :
            return
        
        self.tokens['b'].insert(0,self.tokens['a'].pop())
        self.firstText.setText(''.join(self.tokens['a'])) 
        self.secondText.setText(''.join(self.tokens['b']))
       
    def secondDown(self):
        if len(self.tokens['b']) < 2 :
            return
        
        self.tokens['c'].insert(0,self.tokens['b'].pop())
        self.secondText.setText(''.join(self.tokens['b']))
        self.thirdText.setText(''.join(self.tokens['c']))        
    def thirdUp(self):
        if len(self.tokens['c']) < 2 :
            return
        
        self.tokens['b'].append(self.tokens['c'].pop(0))
        self.secondText.setText(''.join(self.tokens['b']))
        self.thirdText.setText(''.join(self.tokens['c']))              
    def secondUp(self):
        if len(self.tokens['b']) < 2 :
            return
        
        self.tokens['a'].append(self.tokens['b'].pop(0))
        self.secondText.setText(''.join(self.tokens['b']))
        self.firstText.setText(''.join(self.tokens['a']))
    def firstUp(self):
        if len(self.tokens['a']) < 2 :
            return
        
        self.tokens['g'].append(self.tokens['a'].pop(0))
        self.givenText.setText(''.join(self.tokens['g']))
        self.firstText.setText(''.join(self.tokens['a']))         

        

    def pullUp(self):
        print(len(self.tokens))
        print(len(self.tokens[0]))
        return

    def firstDistribution(self):
        if len(self.tokens['g']) < 4 :
            print('too short? : {}'.format(len(self.tokens['g'])))
            return
        
        for i,k in enumerate(self.tokens):
            if k != 'g':
                self.tokens[k].append(self.tokens['g'].pop())
                #print('type is {}'.format(type(self.tokens[i])))
                    
        self.givenText.setText(' '.join(self.tokens['g']))
        self.firstText.setText(' '.join(self.tokens['a']))
        self.secondText.setText(' '.join(self.tokens['b']))
        self.thirdText.setText(' '.join(self.tokens['c']))
       
    def sentTokenize(self):
        self.tokens['g'].clear()
        self.tokens['a'].clear()
        self.tokens['b'].clear()
        self.tokens['c'].clear()
        self.astrix=''
        tempTxt='없음'
        #print((sent_tokenize(self.inputText.toPlainText())))
        temp = sent_tokenize(self.inputText.toPlainText())
        for i, t in enumerate(temp):
            if t[0].islower():
                temp[i-1:i+1]=[' '.join(temp[i-1:i+1])]
        if temp[-1][0]== '*':
            self.astrix = temp.pop()
            tempTxt = '있음'
        self.tokens['g'] = temp
        #self.tokens[0] = sent_tokenize(self.inputText.toPlainText())
        #for i,t in enumerate(self.tokens[0]):
        #    print('{}: length {} \n\t{}'.format(str(i),str(len(t)),t))
        
        tempText = '문장 수: {}\n *:'.format(len(self.tokens['g']))+tempTxt
        self.totalSentLabel.setText(tempText)
    
        
        self.firstDistribution()


    def testHighlight(self):
        #self.inputText.setTextColor(QColor(0,255,0))
       # self.inputText.append("some new sbhit")
       
        tcursor = self.inputText.textCursor()
        tcursor.select(tcursor.WordUnderCursor)
        selectedWord = tcursor.selectedText()

        HighlightFormat = QTextCharFormat()
        HighlightFormat.setBackground(QColor(255,255,0))

        tcursor.insertText(selectedWord,HighlightFormat)
       
        print('color is {}'.format(HighlightFormat.background().color().name()))
        self.inputText.setTextCursor(tcursor)    
       
        
    
    def testBold(self):
        tcursor = self.inputText.textCursor()
        tcursor.select(tcursor.WordUnderCursor)

        boldFormat = QTextCharFormat()
        boldFormat.setFontWeight(QFont.Bold)

        selectedWord = tcursor.selectedText()
        tcursor.insertText(selectedWord,boldFormat)
        #self.inputText.setFontWeight(QFont.Bold)
        self.inputText.setTextCursor(tcursor)    

    def testItalic(self):
        tcursor = self.inputText.textCursor()
        #        tcursor.movePosition(tcursor.PreviousWord, tcursor.MoveAnchor,1)
        tcursor.select(tcursor.WordUnderCursor)
        italicFormat = QTextCharFormat()
        italicFormat.setFontItalic(1)
        selectedWord = tcursor.selectedText()
        tcursor.insertText(selectedWord,italicFormat)
        #self.inputText.setFontWeight(QFont.Bold)
        self.inputText.setTextCursor(tcursor)


    def testUnderline(self):
        print("italic ok")
        tcursor = self.inputText.textCursor()
        #        tcursor.movePosition(tcursor.PreviousWord, tcursor.MoveAnchor,1)
        tcursor.select(tcursor.WordUnderCursor)
        underlineFormat = QTextCharFormat()
        underlineFormat.setFontUnderline(1)
        selectedWord = tcursor.selectedText()
        tcursor.insertText(selectedWord,underlineFormat)
        #self.inputText.setFontWeight(QFont.Bold)
        self.inputText.setTextCursor(tcursor)
        
        
    def testFire(self):
        font = QFont()
        font.setWeight(QFont.Bold)
        font.setItalic(1)

        font2 = QFont()
        
        self.fireLine.setFont(font)
        self.fireLine.setText("Clicked!")
        #self.fireLine.setFont(font2)
        #self.inputText.setFont(font)
        self.inputText.setFontWeight(QFont.Bold)
       # self.inputText.append("some new sbhit")

        #font2 = QFont()
        #self.inputText.setFont(font2)
    def showWord(self):
        tcursor = self.inputText.textCursor()
        tcursor.select(tcursor.WordUnderCursor)
        selectedWord = tcursor.selectedText()
        selectedWord = self.removeSpecialCharacter(selectedWord)
        self.fireLine.setText(selectedWord.lower())


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



    def clickText(self):
        print('ok')



    def closeEvent(self, event):
         print('---closed---')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainPage()
    widget.show()
    sys.exit(app.exec_())
