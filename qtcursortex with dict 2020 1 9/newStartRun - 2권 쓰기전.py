#use v5 to make a db feeder. Feed in all the words from the file
import logging
import sys
import re
import dm
import random
from PyQt5.QtCore import *
#pyqtSlot, QEvent, QTextStream, QFile
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QTextCursor, QFont, QTextFormat, QTextCharFormat, QBrush, QColor, QTextDocument
from PyQt5.uic import loadUi
from PyQt5 import QtSql
#from PyQt5 import QObject
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
        self.tokens={'g':[], 'c':[] ,'b':[], 'a':[]}
        #insertion question variable
        self.insertionTokens=[]
        #irrelevant question variable
        self.irreTokens=[]
        #blank question variable
        self.blankCursorAnchor = 0
        self.answerTableWidget.setRowCount(0)
        self.answerTableWidget.setColumnCount(2)
        #pronoun question variable
        self.proTokens=[]
        self.proUnderList=[]
        #voca question variable
        self.vocaTokens=[]
        self.vocaList=[]
        self.vocaCountAB= {}
        #self.vocaTableWidget.setRowCount(0)
        #self.vocaTableWidget.setColumnCount(2)
        
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

        #token tab 순서맞추기 버튼
        self.givenDownButton.clicked.connect(self.givenDown)  
        self.firstDownButton.clicked.connect(self.firstDown)
        self.secondDownButton.clicked.connect(self.secondDown)
        self.firstUpButton.clicked.connect(self.firstUp)
        self.secondUpButton.clicked.connect(self.secondUp)
        self.thirdUpButton.clicked.connect(self.thirdUp)
        self.tokenChoiceCopyButton.clicked.connect(self.tokenChoiceCopy)
     
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
        self.optionTypeABCRandomButton.clicked.connect(self.optionTypeABCRandom)

        #copies to clipboard when clicked
        self.ABCCopyButton.clicked.connect(self.ABCCopy)
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
        self.irreFormatButton.clicked.connect(self.irreFormat)        
        
        '''
        blank question tab events
        '''
        self.blankAllocateButton.clicked.connect(self.blankAllocate)        
        self.blankButton.clicked.connect(self.blankWords)
        self.answerText.textChanged.connect(self.displayBlankLength)
        self.addToAnswerButon.clicked.connect(self.addToAnswer)
        self.blankRemoveButton.clicked.connect(self.blankRemove)
        self.answerTableWidget.clicked.connect(self.displayAnswerText)
        self.blankFormatAnswersButton.clicked.connect(self.blankFormatAnswers)
        self.blankTextCopyButton.clicked.connect(self.blankTextCopy)
        self.blankAnswersCopyButton.clicked.connect(self.blankAnswersCopy)
        '''
        pro question tab events
        '''
        self.proAllocateButton.clicked.connect(self.proAllocate)
        self.sheButton.clicked.connect(self.markStuff)
        self.youButton.clicked.connect(self.markStuff)
        self.proFormatButton.clicked.connect(self.proFormat)   
        self.proText.textChanged.connect(self.proDisplayCount)
        self.proCopyTextButton.clicked.connect(self.proCopyText)
        '''
        voca question tab events
        '''
        self.vocaAllocateButton.clicked.connect(self.vocaAllocate)
        self.vocaFormatButton.clicked.connect(self.vocaFormat)
        self.vocaCopyTextButton.clicked.connect(self.vocaCopyText)
        self.vocaText.cursorPositionChanged.connect(self.showVoca)
        self.vocaLeftButton.clicked.connect(lambda: self.vocaBracketWords('left'))
       # self.vocaLeftButton.clicked.connect(self.vocaFix)
        self.vocaRightButton.clicked.connect(lambda: self.vocaBracketWords('right')) 
        self.vocaRemoveButton.clicked.connect(self.vocaRemove)
        self.vocaCopyAnswerButton.clicked.connect(self.vocaCopyAnswer)        
        
    '''
    voca functions
    '''
    def vocaFix(self):
        newWord = self.vocaNewWord.toPlainText()
        cursor = self.vocaText.textCursor()
        cursor.select(cursor.WordUnderCursor)
       # cursor.movePosition(cursor.StartOfWord,cursor.MoveAnchor)
        print(cursor.positionInBlock())
        cursor.insertText(newWord)             
    def vocaCopyAnswer(self):
        self.vocaAnswerText.selectAll()
        self.vocaAnswerText.copy()   
    def vocaFormat(self):
        rowCount = self.vocaTableWidget.rowCount()
        if rowCount <3:
            self.vocaStatusLabel.setText(str(rowCount)+' :need more choices')
            return
        elif rowCount > 3:
            self.vocaStatusLabel.setText(str(rowCount)+' :need less choices')
            return

        self.vocaTableWidget.sortByColumn(0,Qt.AscendingOrder)
        self.resetCursorColor(self.proText)

        i = rowCount-1
        print(i)
        while i > -1:

            pos = self.vocaTableWidget.item(i,0).text()
            clearFormat = QTextCharFormat()
            cursor = self.vocaText.textCursor()
            cursor.setPosition(int(pos))
            cursor.movePosition(cursor.PreviousWord,cursor.MoveAnchor)
            cursor.select(cursor.WordUnderCursor)
            num = '{}[{} / {}]'.format(self.circleNumber(i+1),
                                       self.vocaTableWidget.item(i,1).text(),
                                       self.vocaTableWidget.item(i,2).text())
            cursor.insertText(num)
            i -= 1
        temp = self.vocaText.toHtml()
        temp =  temp.replace('<br /><br />',' ')
        self.vocaText.setHtml(temp)
        self.vocaStatusLabel.setText('done')
        self.vocaAnswerFormat()
    def vocaAnswerFormat(self):
        answer =''
        rowCount = self.vocaTableWidget.rowCount()
        i = 0
        while i < rowCount:
            temp = self.vocaTableWidget.item(i,3).text()
            answer += temp
            i += 1
        print('answer :'+answer)
        self.vocaAnswerAB(answer)
    


    #check 'AAA'~'BBB' type word, build 5 choices
    def vocaAnswerAB(self,word):
        a = ['AAB','ABA','ABB','BAA','BAB','BBA','BBB']
        self.vocaCountAB['1A']=1
        self.vocaCountAB['1B']=0
        self.vocaCountAB['2A']=1
        self.vocaCountAB['2B']=0
        self.vocaCountAB['3A']=1
        self.vocaCountAB['3B']=0

        random.shuffle(a)
        c=['AAA']

        if word=='AAA':
            self.vocaAnswerLabel.setText('답: 1')
        else:
            a.remove(word)
            self.analAB(word)
            c.append(word)
            
        while len(c) < 5:
            temp = a.pop()
            if self.analAB(temp):
                c.append(temp)
        sortedList = sorted(c)
        print(sortedList)
        self.vocaAnswerLabel.setText('답: {}'.format(sortedList.index(word)+1))
#        print(self.vocaCountAB)
        temp = '  (A)\t(B)\t(C)'
        choiceA = self.vocaTableWidget.item(0,1).text()
        choiceB = self.vocaTableWidget.item(0,2).text()
        choiceC = self.vocaTableWidget.item(1,1).text()
        choiceD = self.vocaTableWidget.item(1,2).text()
        choiceE = self.vocaTableWidget.item(2,1).text()
        choiceF = self.vocaTableWidget.item(2,2).text()

        
        for i, e in enumerate(sortedList):
            firstE = choiceA if e[0]=='A' else choiceB
            secondE = choiceC if e[1]=='A' else choiceD
            thirdE = choiceE if e[2]=='A' else choiceF
            temp += '\n{}{}\t{}\t{}'.format(self.circleNumber(i+1), firstE, secondE, thirdE)
        self.vocaAnswerText.setText(temp)

    #helper fucntion for answerAB
    def analAB(self, temp):
        if temp[0] == 'A' and self.vocaCountAB['1A']==3:
            print('1')
            return False
        elif temp[0] == 'B' and self.vocaCountAB['1B']==3:
            print('2')
            return  False
        if temp[1] =='A' and self.vocaCountAB['2A']==3:
            print('3')        
            return  False
        elif temp[1] == 'B' and self.vocaCountAB['2B']==3:
            print('4')        
            return  False
        if temp[2] =='A' and self.vocaCountAB['3A']==3:
            print('5')        
            return  False
        elif temp[2] == 'B' and self.vocaCountAB['3B']==3:
            print('6')        
            return  False
        if temp[0] == 'A':
            self.vocaCountAB['1A'] = self.vocaCountAB['1A']+1
        else:
            self.vocaCountAB['1B'] = self.vocaCountAB['1B']+1

        if temp[1] == 'A':
            self.vocaCountAB['2A'] = self.vocaCountAB['2A']+1
        else:
            self.vocaCountAB['2B'] = self.vocaCountAB['2B']+1

        if temp[2] == 'A':
            self.vocaCountAB['3A'] = self.vocaCountAB['3A']+1
        else:
            self.vocaCountAB['3B'] = self.vocaCountAB['3B']+1    

        return True


            

    def vocaBracketWords(self, orientation):
        # temp variable - 
        # get word from vocaWordText
        # vocaNewWord
        #if ori is left, put vocaNewWord on left
        #  ,else right
        #call self.vocaAddToAnswer(temp)
        temp=''
        originalWord = self.vocaWordText.toPlainText()
        newWord = self.vocaNewWord.toPlainText()
        if orientation =='left':
            print('left clicked')
           # temp = '[{} / {}]'.format(newWord, originalWord)
        else:
            print('right clicked')
            #temp = '[{} / {}]'.format(originalWord, newWord)
        self.vocaAddToAnswer(orientation)

    def vocaRemove(self):
        row=  self.vocaTableWidget.currentRow()
        self.vocaTableWidget.removeRow(row)
        
    def vocaAddToAnswer(self, orientation):
        rowCount = self.vocaTableWidget.rowCount()
        if rowCount >4:
            return
        #QTableWidgetItem(str(len(self.answerText.toPlainText()))))
        self.vocaTableWidget.insertRow(rowCount)
        temp = QTableWidgetItem()
        temp.setData(Qt.DisplayRole, int(self.vocaPos.text()))
        self.vocaTableWidget.setSortingEnabled(False)
        self.vocaTableWidget.setItem(rowCount,0,temp)
        #self.vocaTableWidget.setItem(rowCount,0,QTableWidgetItem(self.vocaPos.text()))
        if orientation =='left':
            self.vocaTableWidget.setItem(rowCount,1,
                                       QTableWidgetItem(self.vocaNewWord.toPlainText()))
            self.vocaTableWidget.setItem(rowCount,2,
                                       QTableWidgetItem(self.vocaWordText.toPlainText()))            
            self.vocaTableWidget.setItem(rowCount,3,
                                       QTableWidgetItem('B'))
        else:
            self.vocaTableWidget.setItem(rowCount,1,
                                       QTableWidgetItem(self.vocaWordText.toPlainText()))
            self.vocaTableWidget.setItem(rowCount,2,
                                       QTableWidgetItem(self.vocaNewWord.toPlainText()))              
            self.vocaTableWidget.setItem(rowCount,3,
                                       QTableWidgetItem('A'))
        self.vocaTableWidget.setSortingEnabled(True)
    
       
            
    def deleteVocaHighlight(self, textEdit): #not used
        tempCursor = self.vocaText.textCursor()
        whiteFormat = QTextCharFormat()
        tempCursor.setCharFormat(whiteFormat)
        textEdit.setTextCursor(tempCursor)
    def vocaHighlight(self):
        cursor = self.vocaText.textCursor()
        cursor.select(cursor.WordUnderCursor)
        highlightFormat = QTextCharFormat()
        temp = cursor.charFormat().background().color()
        if temp != QColor(255, 255, 0):
            highlightFormat.setBackground(QColor(255,255,0))
        else:
            highlightFormat.setBackground(QColor(255,255,255))
        cursor.setCharFormat(highlightFormat)
             
    def showVoca(self):
        cursor = self.vocaText.textCursor()
        cursor.select(cursor.WordUnderCursor)
        selectedWord = cursor.selectedText()
        highlightFormat = QTextCharFormat()

        temp = cursor.charFormat().background().color()
        if temp != QColor(255, 255, 0):
            highlightFormat.setBackground(QColor(255,255,0))
        else:
            highlightFormat.setBackground(QColor(255,255,255))
        cursor.setCharFormat(highlightFormat)
             
        #cursor.movePosition(cursor.StartOfWord,cursor.MoveAnchor)
        pos = cursor.position()
        self.vocaPos.setText(str(pos)) 
   
        selectedWord = self.removeSpecialCharacter(selectedWord)
        self.vocaWordText.setText(selectedWord)
    def vocaAllocate(self):
        self.vocaText.clear()
        self.vocaTokens.clear()
        self.vocaAnswerText.clear()
        self.vocaAnswerLabel.clear()
        self.vocaTableWidget.clear()
        self.vocaTableWidget.setRowCount(0)
        self.vocaTableWidget.setColumnCount(4)
        #self.proUnderList.clear()
        temp = self.tokenizeSent()
        if len(temp) < 5:
            self.vocaAllocateLabel.setText('{} - not enough sents'.format(str(len(temp))))
            return
        self.vocaTokens = temp
        self.vocaAllocateLabel.setText(
            '문장 수: {}\n *:'.format(len(self.vocaTokens))+self.tempTxt)
        self.vocaText.setText('<br><br>'.join(self.vocaTokens))
        	
    def vocaLeft(self):
        temp = self.vocaWordText.toPlainText()
        cursor = self.vocaText.textCursor()
        cursor.select(cursor.WordUnderCursor)
        cursor.insertText(temp)
        self.vocaText.setTextCursor(cursor)
        
    def vocaRight(self):
        print('voca right clicked')
    def vocaCopyText(self):
        self.vocaText.selectAll()
        self.vocaText.copy()                    
    '''
    utility function;
    key binding test fucntion
    circleNumber
    '''
 
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            if self.proText.hasFocus():
                self.proUnderline()
            if self.vocaText.hasFocus():
                self.vocaHighlight()
    def circleNumber(self,num):
        switcher = {1:'①',
                    2:'②',
                    3:'③',
                    4:'④',
                    5:'⑤'}
        return switcher.get(num)    
    '''
    pro question tab functions
    '''

    def proCopyText(self):
        self.proText.selectAll()
        self.proText.copy()   
    def proDisplayCount(self):
        self.proCount.setText(str(len(self.proUnderList)))
    def proFormat(self):
        if len(self.proUnderList) <5:
            self.proCount.setText(str(len(self.proUnderList))+' :need more underline')
            print('too small: {}'.format(str(len(self.proUnderList))))
            return
        elif len(self.proUnderList) > 5:
            self.proCount.setText(str(len(self.proUnderList))+' :more than 5 underline')
            print('too large: '+str(len(self.proUnderList)))
            return
        self.proCount.setText('done')
        self.resetCursorPos(self.proText)
        self.resetCursorColor(self.proText)
        self.proUnderList.sort()
        i = len(self.proUnderList)-1
        while i > -1:
            clearFormat = QTextCharFormat()
            cursor = self.proText.textCursor()
            cursor.setPosition(self.proUnderList[i])
            num = self.circleNumber(i+1)
            cursor.insertText(num,clearFormat)
            self.proText.setTextCursor(cursor)
            i -= 1
        temp = self.proText.toHtml()
        temp =  temp.replace('<br /><br />',' ')
        self.proText.setHtml(temp)

        
    def proUnderline(self):
        cursor = self.proText.textCursor()
        cursor.movePosition(cursor.StartOfWord,cursor.MoveAnchor)
        pos = cursor.position()
        cursor.select(cursor.WordUnderCursor)
        underlineFormat = QTextCharFormat()
        a= cursor.charFormat().fontUnderline()
        
        if a:
            underlineFormat.setFontUnderline(False)
            if pos in self.proUnderList:
                del self.proUnderList[self.proUnderList.index(pos)]
        else:
            underlineFormat.setFontUnderline(True)
            self.proUnderList.append(pos)
        selectedWord = cursor.selectedText()
        cursor.insertText(selectedWord,underlineFormat)
        self.proText.setTextCursor(cursor)


    def resetCursorColor(self,textEdit):
        tempCursor = textEdit.textCursor()
        whiteFormat = QTextCharFormat()
        tempCursor.setCharFormat(whiteFormat)
        textEdit.setTextCursor(tempCursor)
    def resetCursorPos(self,textEdit):
        tempCursor = textEdit.textCursor()
        tempCursor.movePosition(tempCursor.Start, tempCursor.MoveAnchor)
        textEdit.setTextCursor(tempCursor)

    def markStuff(self):
        if QObject.sender(self) == self.sheButton:
            sheList = ['she','her']
            heList = ['he','him','his']
            self.proMark(sheList, QColor(255, 153, 255)) #light pink
            self.proMark(heList, QColor(128, 179, 255)) #light blue
        elif QObject.sender(self) == self.youButton:
            meList = ['i','me','my','you','your']  
            self.proMark(meList, QColor(255, 191, 0)) #golden yellow
    #wordList[], Qt.Color
    def proMark(self, wordList, color):
        if len(wordList) <1:
            return
        self.resetCursorColor(self.proText)
        self.resetCursorPos(self.proText)

        colorFormat = QTextCharFormat()
        colorFormat.setBackground(color)
        for n, item in enumerate(wordList):
            while self.proText.find(item,QTextDocument.FindWholeWords):
                foundCursor = self.proText.textCursor()
                word = foundCursor.selectedText()
                foundCursor.insertText(word, colorFormat)
                self.proText.setTextCursor(foundCursor)
            self.resetCursorPos(self.proText)
        
    def proAllocate(self):
        self.proTokens.clear()
        self.proUnderList.clear()
        temp = self.tokenizeSent()
        if len(temp) < 5:
            self.proAllocateLabel.setText('{} - not enough sents'.format(str(len(temp))))
            return
        self.proTokens = temp
        self.proAllocateLabel.setText(
            '문장 수: {}\n *:'.format(len(self.proTokens))+self.tempTxt)        
        self.proText.setText('<br><br>'.join(self.proTokens))        
        
    
        
    '''
    blank question tab functions
    '''
    def blankTextCopy(self):
        self.blankText.selectAll()
        self.blankText.copy()   
    def blankAnswersCopy(self):
        temp = []
        rowCount = self.answerTableWidget.rowCount()
        i = 0
        while i<rowCount:
            temp.append(self.answerTableWidget.item(i,1).text())
            i += 1
        temp = self.addCircleNumberOnly(temp)
        self.answerText.setText('\n'.join(temp))
        self.answerText.selectAll()
        self.answerText.copy()   

    def blankFormatAnswers(self):
        temp = self.answerTableWidget.item(0,1).text()
        self.answerTableWidget.sortByColumn(0,Qt.AscendingOrder)
        findRow =  self.answerTableWidget.findItems(temp, Qt.MatchExactly)[0].row()
        self.blankFormatAnswersLabel.setText(str(findRow+1))
    def displayAnswerText(self):
        self.answerText.setText(self.answerTableWidget.item(
            self.answerTableWidget.currentRow(),1).text())
    def blankRemove(self):
        row=  self.answerTableWidget.currentRow()
        self.answerTableWidget.removeRow(row)
    def addToAnswer(self):
        rowCount = self.answerTableWidget.rowCount()
        if rowCount >4:
            return
        #QTableWidgetItem(str(len(self.answerText.toPlainText()))))
        self.answerTableWidget.insertRow(rowCount)
        temp = QTableWidgetItem()
        temp.setData(Qt.DisplayRole, len(self.answerText.toPlainText()))
        self.answerTableWidget.setItem(rowCount,0,temp)
        self.answerTableWidget.setItem(rowCount,1,
                                       QTableWidgetItem(self.answerText.toPlainText()))
        
        
    def displayBlankLength(self):
        self.answerTextLabel.setText(str(len(self.answerText.toPlainText())))
        
        
    def blankAllocate(self):
        temp = self.tokenizeSent()
        self.blankAllocateLabel.setText(
            '문장 수: {}\n *:'.format(len(temp))+self.tempTxt)          
        self.blankText.setText(' '.join(temp))        

    def blankWords(self):
        tcursor = self.blankText.textCursor()
        selectedWord = tcursor.selectedText()

        HighlightFormat = QTextCharFormat()
        HighlightFormat.setFontUnderline(1)
        HighlightFormat.setBackground(QColor(255,255,0))
        blankLine=''
        numWords = len(selectedWord.split())
        if numWords < 2:
            blankLine = '         '
        elif len(selectedWord)>39:
            blankLine = '                              '
        else:
            blankLine = '                    '
        tcursor.insertText(blankLine,HighlightFormat)
        #print('color is {}'.format(HighlightFormat.background().color().name()))
        self.blankText.setTextCursor(tcursor)
        self.answerText.setText(selectedWord)


    '''
    irrelevant tab functions
    '''
    def irreGivenCopy(self):
        self.irreGivenText.selectAll()
        self.irreGivenText.copy()        
    def irreTextCopy(self):
        self.irreFullText.selectAll()
        self.irreFullText.copy()        
    def irreFormat(self):
       #check group box, insert at tokens.len , -4 -3 -2 -1
        if self.irreOne.isChecked():
           self.irreTokens.insert(len(self.irreTokens)-4, self.irreGivenText.toPlainText())
        if self.irreTwo.isChecked():
           self.irreTokens.insert(len(self.irreTokens)-3, self.irreGivenText.toPlainText())
        if self.irreThree.isChecked():
           self.irreTokens.insert(len(self.irreTokens)-2, self.irreGivenText.toPlainText())
        if self.irreFour.isChecked():
           self.irreTokens.insert(len(self.irreTokens)-1, self.irreGivenText.toPlainText())
        if self.irreFive.isChecked():
           self.irreTokens.insert(len(self.irreTokens), self.irreGivenText.toPlainText())
           
        self.irreTokens = self.addCircleNumber(self.irreTokens)           
        self.irreFullText.setText(' '.join(self.irreTokens))
        self.irreFullText.append(self.astrix)
    def irreAllocate(self):
        self.irreTokens.clear()
        self.irreGivenText.clear()
        temp = self.tokenizeSent()
        if len(temp) < 5:
            self.irreAllocateLabel.setText('{} - not enough sents'.format(str(len(temp))))
            return
        self.irreTokens = temp[:]
        tempList = self.addCircleNumber(temp,False)
        self.irreAllocateLabel.setText(
            '문장 수: {}\n *:'.format(len(tempList))+self.tempTxt)        
        self.irreFullText.setText('\n\n'.join(tempList))
    '''
    insertion tab functions
    '''

    def insertionGivenCopy(self):
        print('hi')
        self.insertionGivenText.selectAll()
        self.insertionGivenText.copy()    
    def insertionTextCopy(self):
        self.insertionFullText.append(self.astrix)
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
    

    
    def addCircleNumberOnly(self,temp):
        temp[-1] = '{} '.format(CIRCLE_FIVE) + temp[-1]
        temp[-2] = '{} '.format(CIRCLE_FOUR) + temp[-2]
        temp[-3] = '{} '.format(CIRCLE_THREE) + temp[-3]
        temp[-4] = '{} '.format(CIRCLE_TWO) + temp[-4]
        temp[-5] = '{} '.format(CIRCLE_ONE) + temp[-5]        
        return temp        

    def addCircleNumber(self, temp, forward = True):
        if forward == True:
            temp[-1] = '( {} ) '.format(CIRCLE_FIVE) + temp[-1]
            temp[-2] = '( {} ) '.format(CIRCLE_FOUR) + temp[-2]
            temp[-3] = '( {} ) '.format(CIRCLE_THREE) + temp[-3]
            temp[-4] = '( {} ) '.format(CIRCLE_TWO) + temp[-4]
            temp[-5] = '( {} ) '.format(CIRCLE_ONE) + temp[-5]        
            return temp

        temp[-1] =  temp[-1] +'( {} ) '.format(CIRCLE_FIVE)
        temp[-2] =  temp[-2] +'( {} ) '.format(CIRCLE_FOUR)
        temp[-3] =  temp[-3] +'( {} ) '.format(CIRCLE_THREE)
        temp[-4] =  temp[-4] +'( {} ) '.format(CIRCLE_TWO)
        temp[-5] =  temp[-5] +'( {} ) '.format(CIRCLE_ONE)
        return temp
    
    '''
    rearrange token function
    '''
    def clipboard(self, word):
        cb =QApplication.clipboard()
        cb.setText(word)
    def tokenChoiceCopy(self):
        choices = '① (A)-(C)-(B)\n② (B)-(A)-(C)\n③ (B)-(C)-(A)\n④ (C)-(A)-(B)\n⑤ (C)-(B)-(A)'
        self.clipboard(choices)
    def ABCCopy(self):
        temp = '{}\n{}\n{}'.format(self.firstText.toPlainText() , self.secondText.toPlainText() , self.thirdText.toPlainText())
        self.firstText.setText(temp)
        self.firstText.selectAll()
        self.firstText.copy()        
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
       # self.firstCopyButton.setText('A')
       # self.secondCopyButton.setText('B')
       # self.thirdCopyButton.setText('C')
        self.firstText.setText(' '.join(self.tokens['a']))
        self.secondText.setText(' '.join(self.tokens['c']))
        self.thirdText.setText(' '.join(self.tokens['b']))
       

            
    def ABCTwoCLicked(self):
        if not self.optionTypeABCButtonTwo.isChecked():
            return
       # self.firstCopyButton.setText('A')
       # self.secondCopyButton.setText('A')
       # self.thirdCopyButton.setText('C')
        self.firstText.setText(' '.join(self.tokens['b']))
        self.secondText.setText(' '.join(self.tokens['a']))
        self.thirdText.setText(' '.join(self.tokens['c']))
        
    def ABCThreeCLicked(self):
        if not self.optionTypeABCButtonThree.isChecked():        
            return
       # self.firstCopyButton.setText('B')
     #   self.secondCopyButton.setText('C')
     #   self.thirdCopyButton.setText('A')
        self.firstText.setText(' '.join(self.tokens['c']))
        self.secondText.setText(' '.join(self.tokens['a']))
        self.thirdText.setText(' '.join(self.tokens['b']))
        
    def ABCFourCLicked(self):
        if not self.optionTypeABCButtonFour.isChecked():
            return
     #   self.firstCopyButton.setText('C')
     #   self.secondCopyButton.setText('A')
     #   self.thirdCopyButton.setText('B')
        self.firstText.setText(' '.join(self.tokens['b']))
        self.secondText.setText(' '.join(self.tokens['c']))
        self.thirdText.setText(' '.join(self.tokens['a']))
        
            
    def ABCFiveCLicked(self):
        if not self.optionTypeABCButtonFive.isChecked():        
            return
    #    self.firstCopyButton.setText('C')
     #   self.secondCopyButton.setText('B')
       # self.thirdCopyButton.setText('A')
        self.firstText.setText(' '.join(self.tokens['c']))
        self.secondText.setText(' '.join(self.tokens['b']))
        self.thirdText.setText(' '.join(self.tokens['a']))
        
    def optionTypeABCRandom(self):
        print('hi')        
        num = random.randint(1,5)
        print(num)
        if num ==1:
            self.optionTypeABCButtonOne.setChecked(True)
            self.ABCOneCLicked()
        if num ==2:
            self.optionTypeABCButtonTwo.setChecked(True)            
            self.ABCTwoCLicked()
        if num ==3:
            self.optionTypeABCButtonThree.setChecked(True)               
            self.ABCThreeCLicked()
        if num ==4:
            self.optionTypeABCButtonFour.setChecked(True)               
            self.ABCFourCLicked()
        if num ==5:
            self.optionTypeABCButtonFive.setChecked(True)                           
            self.ABCFiveCLicked()            
        return
    
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
        self.givenText.setText(' '.join(self.tokens['g']))
        self.firstText.setText(' '.join(self.tokens['a']))
    def firstDown(self):
        if len(self.tokens['a']) < 2 :
            return
        
        self.tokens['b'].insert(0,self.tokens['a'].pop())
        self.firstText.setText(' '.join(self.tokens['a'])) 
        self.secondText.setText(' '.join(self.tokens['b']))
       
    def secondDown(self):
        if len(self.tokens['b']) < 2 :
            return
        
        self.tokens['c'].insert(0,self.tokens['b'].pop())
        self.secondText.setText(' '.join(self.tokens['b']))
        self.thirdText.setText(' '.join(self.tokens['c']))        
    def thirdUp(self):
        if len(self.tokens['c']) < 2 :
            return
        
        self.tokens['b'].append(self.tokens['c'].pop(0))
        self.secondText.setText(' '.join(self.tokens['b']))
        self.thirdText.setText(' '.join(self.tokens['c']))              
    def secondUp(self):
        if len(self.tokens['b']) < 2 :
            return
        
        self.tokens['a'].append(self.tokens['b'].pop(0))
        self.secondText.setText(' '.join(self.tokens['b']))
        self.firstText.setText(' '.join(self.tokens['a']))
    def firstUp(self):
        if len(self.tokens['a']) < 2 :
            return
        
        self.tokens['g'].append(self.tokens['a'].pop(0))
        self.givenText.setText(' '.join(self.tokens['g']))
        self.firstText.setText(' '.join(self.tokens['a']))         

        

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
        texts.setCodec("UTF-8");
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
