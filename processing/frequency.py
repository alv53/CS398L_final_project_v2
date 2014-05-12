import nltk, re

texts = open("WhiteFang.txt", "r").read()
tokens = nltk.word_tokenize(texts)
tokens = nltk.word_tokenize(texts)
tokens = [re.sub('\.','',w) for w in tokens] #remove periods
tokens = [w for w in tokens if w.isalpha()] #just keep words
freq = nltk.FreqDist(tokens)
print freq