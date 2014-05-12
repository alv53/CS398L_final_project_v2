# This file does the actual sentiment analysis on a per paragraph basis
import nltk
import re
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from random import randint
import collections, itertools
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews, stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

def getImportance(word, tfidfArray):
	for elem in tfidfArray:
		if word == elem["word"]:
			return elem["imp"]
	return 0

def returnPureWord(word):
	retVal = word.replace(",", "")
	retVal = word.replace("\'", "")
	retVal = word.replace("\"", "")
	retVal = word.replace(".", "")
	retVal = word.replace("\n", "")
	return retVal

def sentimentTag(paragraph):
	sentences = nltk.sent_tokenize(paragraph)
	pos = 0
	neg = 0
	ret = [dict(sentence=0, tag="")]
	for i in range(len(sentences)):
		wordList = [sentences[i]]
		sentiment = classifier.classify(word_feats(sentences[i]))
		ret.append(dict(sentence=i, tag=sentiment))
	return ret[1:]

def word_feats(words):
    return dict([(word, True) for word in words])

# Train from blankTrain.txt
train=[('He no longer was afraid of anything.', 'pos'), ('It was lean with long-standing hunger.', 'neg'), ('This served as a relish, and his hunger increased mightily; but he was too old in the world to forget his caution.', 'neg'), ('There were hisses from the crowd and cries of protest, but that was all.', 'neg'), ('Something was impending.', 'neg'), ('Grey Beaver never petted nor caressed.', 'neg'), ('With his one eye the elder saw the opportunity.', 'pos'), ('Or at least White Fang thought he was deserted, until he smelled out the master\'s canvas clothes-bags alongside of him, and proceeded to mount guard over them.', 'pos'), ('They made their bread with baking-powder.', 'pos'), ('White Fang was too helpless to defend himself, and it would have gone hard with him had not Grey Beaver\'s foot shot out, lifting Lip-lip into the air with its violence so that he smashed down to earth a dozen feet away.', 'pos'), ('The roar of it no longer dinned upon his ears.', 'pos'), ('Then a huge dog was thrust inside, and the door was slammed shut behind him.', 'neg'), ('This was repeated a number of times.', 'pos'), ('Then she sprang away, up the trail, squalling with every leap she made.', 'pos'), ('\"An\' I\'ll bet it ain\'t far from five feet long.', 'pos'), ('One chance in a thousand is really optimistic.', 'neg'), ('Bitter experiences these, which, perforce, he swallowed, calling upon all his wisdom to cope with them.', 'neg'), ('There was a leap, swifter than his unpractised sight, and the lean, yellow body disappeared for a moment out of the field of his vision.', 'pos'), ('But this was only when the master was not around.', 'neg'), ('Five minutes later the landscape was covered with fleeing boys, many of whom dripped blood upon the snow in token that White Fang\'s teeth had not been idle.', 'neg') ]
all_words = set(word.lower() for passage in train for word in nltk.word_tokenize(passage[0]))
t = [({word: (word in nltk.word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]

classifier = nltk.NaiveBayesClassifier.train(t)

toWrite = open('../web/data/para.tsv', 'wr+')
toWrite.write("para\tpos\tneg\n")
toWrite.close()
currPara = 1
toAppend = open('../web/data/para.tsv', 'a')
text = open('WhiteFang.txt', 'r').read()
tokens = re.split('\n\n\n|\n\n', text)
size = len(tokens)
currIter = 0

myDict = [dict(num=0, para="", sentiment=0)]
for i in range(0,size):
	sentiment = sentimentTag(tokens[i])
	# myDict.append(dict(num=currPara, para=tokens[i], posSent=sentiment[0], negSent=sentiment[1]))
	pos=0
	neg=0
	for sent in sentiment:
		if sent["tag"] == "pos":
			pos = pos + 1
		else:
			neg = neg + 1
	if currPara == 1095:
		toAppend.write(str(currPara) + "\t" + str(pos) + "\t" + str(neg))
	else:			
		toAppend.write(str(currPara) + "\t" + str(pos) + "\t" + str(neg) + "\n")

	currFile = open("../web/paragraphs/paragraph" + str(i+1) + ".html", "wr+")
	currFile.write("<!DOCTYPE html>\n")
	currFile.write("<link rel=\"stylesheet\" href=\"../css/paragraph.css\" type=\"text/css\" media=\"screen\" />\n")
	currFile.write("<body style=\"background-color:#EEEEEE\"><div class=\"container\">")
	currFile.write("<a onClick=\"location.href='../index.html'\"><p style=\"text-align:center\">Paragraph: " + str(i+1) + "<br><br>Back to Visualization</p></a>")
	currFile.write("<p class=\"split-para\">")
	if i != 0:
		currFile.write("<a onClick=\"location.href='paragraph" + str(i) + ".html'\"> Previous Paragraph </a>\n")
	else:
		currFile.write("<a onClick=\"location.href='paragraph" + str(i+2) + ".html'\"> Next Paragraph </a>\n")
	if (i+2) <= size:
		currFile.write("<span><a onClick=\"location.href='paragraph" + str(i+2) + ".html'\"> Next Paragraph </a></span></p>")
	else:
		currFile.write("<span><a onClick=\"location.href='paragraph" + str(i) + ".html'\"> Previous Paragraph </a></span></p>")
	currFile.write("<p>")
	# Now we write the sentences in color
	sentences = nltk.sent_tokenize(tokens[i])
	for x in range(len(sentences)):
		if sentiment[x]["tag"] == "pos":
			currFile.write("<span style=\"color:#00CD66\">" + sentences[x] + " </span>")
		else:
			currFile.write("<span style=\"color:brown\">" + sentences[x] + " </span>")
	currFile.write("</p></div>")
	currPara=currPara+1

