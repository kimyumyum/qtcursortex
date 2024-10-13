from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def toSimpleVerb(word):
    return WordNetLemmatizer().lemmatize(word,'v')


def toSimpleNoun(word):
    return WordNetLemmatizer().lemmatize(word,'n')


