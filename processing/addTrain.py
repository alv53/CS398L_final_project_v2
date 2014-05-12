# The purpose of this file is to generate the training set (with blanks for me to fill in), to be used in processing.py
import nltk
from random import randint

text = open("WhiteFang.txt", "r").read()
toWrite = open("blankTrain.txt", "a")
sentences = nltk.sent_tokenize(text)
for i in range(20): #Picking random sentences from the text to use as the train
	randSent = "\n"
	while(randSent == "\n"):
		randSent = sentences[randint(0,len(sentences)-1)]
	randSent = randSent.replace("\n", " ")
	toWrite.write("(\'" + randSent + "\', \'\'),")

toWrite.write("]")