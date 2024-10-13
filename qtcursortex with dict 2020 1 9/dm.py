from datamuse import datamuse

api = datamuse.Datamuse()

#get a NOUN, print adjective of the NOUN 'num' of times
def jja(word , num=5):
    found_words = api.words(rel_jja=word, max=num)
    #print(found_words)
    return found_words

#get a ADJECTIVE, print noun of the ADJECTIVE 'num' of times
def jjb(word , num=5):
    found_words = api.words(rel_jjb=word, max=num)
    #print(found_words)
    return found_words

#get a word, print synonym 'num' of times
def syn(word , num=5):
    found_words = api.words(rel_syn=word, max=num)
    #print(found_words)
    return found_words

#get a word, print triggered words 'num' of times
def trg(word , num=5):
    found_words = api.words(rel_trg=word, max=num)
    #print(found_words)
    return found_words

#get a word, print antonym 'num' of times
def ant(word , num=5):
    found_words = api.words(rel_ant=word, max=num)
    #print(found_words)
    return found_words

#get a word, print hypernym 'num' of times
def spc(word , num=5):
    found_words = api.words(rel_spc=word, max=num)
    #print(found_words)
    return found_words

#get a word, print hypernym (more general than spc)'num' of times
def gen(word , num=5):
    found_words = api.words(rel_gen=word, max=num)
    #print(found_words)
    return found_words

#get a word, print holonyms (comprises of)'num' of times
def com(word , num=5):
    found_words = api.words(rel_com=word, max=num)
    #print(found_words)
    return found_words

#get a word, print meronyms (part of)'num' of times
def par(word , num=5):
    found_words = api.words(rel_par=word, max=num)
    #print(found_words)
    return found_words

#get a word, print frequent followers 'num' of times
def bga(word , num=5):
    found_words = api.words(rel_bga=word, max=num)
    #print(found_words)
    return found_words

#get a word, print frequent predecessors 'num' of times
def bgb(word , num=5):
    found_words = api.words(rel_bgb=word, max=num)
    #print(found_words)
    return found_words


def ml(word , num=5):
    found_words = api.words(ml=word, max=num)
    #print(found_words)
    return found_words


