import random



countAB= {}

#check 'AAA'~'BBB' type word, build 5 choices
def vocaAnswerAB(word):
    a = ['AAB','ABA','ABB','BAA','BAB','BBA','BBB']
    countAB['1A']=1
    countAB['1B']=0
    countAB['2A']=1
    countAB['2B']=0
    countAB['3A']=1
    countAB['3B']=0

    random.shuffle(a)
    c=['AAA']

    if word=='AAA':
        self.vocaAnswerLabel.setText('답: 1')
    elif word in a:
        a.remove(word)
        c.append(word)
        
    while len(c) < 5:
        temp = a.pop()
        if temp == word:
             self.vocaAnswerLabel.setText('답: {}'.format(str(len(c))))    
        print(temp)
        if self.analAB(temp):
            c.append(temp)
    print(c)
    print(count)

#helper fucntion for answerAB
def analAB(temp):
    if temp[0] == 'A' and count['1A']==3:
        print('1')
        return False
    elif temp[0] == 'B' and count['1B']==3:
        print('2')
        return  False
    if temp[1] =='A' and count['2A']==3:
        print('3')        
        return  False
    elif temp[1] == 'B' and count['2B']==3:
        print('4')        
        return  False
    if temp[2] =='A' and count['3A']==3:
        print('5')        
        return  False
    elif temp[2] == 'B' and count['3B']==3:
        print('6')        
        return  False
    if temp[0] == 'A':
        count['1A'] = count['1A']+1
    else:
        count['1B'] = count['1B']+1

    if temp[1] == 'A':
        count['2A'] = count['2A']+1
    else:
        count['2B'] = count['2B']+1

    if temp[2] == 'A':
        count['3A'] = count['3A']+1
    else:
        count['3B'] = count['3B']+1    

    return True

    
