# The puropse of this file is to analyze the book based on the 5 parts, and split into paragraphs. This will help determine the size and bounds of our final graph.
import nltk
import re

def partSum(part, sum, type):
	text = open('part' + str(part) + '.txt', 'r').read()
	tokens = []
	if(type == 'para'):
		tokens = re.split('\n\n\n\n\n|\n\n\n\n|\n\n\n|\n\n', text)
	elif(type == 'ch'):
		tokens = re.split('CHAPTER', text)
		tokens = tokens[1:]
	size = len(tokens)
	print "Part 1 Length: " + str(size)
	return size

def partPercent(part, total, totalFrac, type):
	text = open('part' + str(part) + '.txt', 'r').read()
	tokens = []
	if(type == 'para'):
		tokens = re.split('\n\n\n\n\n|\n\n\n\n|\n\n\n|\n\n', text)
	elif(type == 'ch'):
		tokens = re.split('CHAPTER', text)
		tokens = tokens[1:]
	size = len(tokens)
	print "Total Fraction: " + str(totalFrac + float(size)/total)
	return float(size)/total


text = open('WhiteFang.txt', 'r').read()
tokens = re.split('\n\n\n|\n\n', text)
total = len(tokens)
print "STATS BY PARAGRAPH\nNum Paras in book: " + str(total)
totalLenTest = 0
totalFrac = 0 
for i in range(1,6):
	totalLenTest = totalLenTest + partSum(i, totalLenTest, 'para')
	totalFrac = totalFrac + partPercent(i, total, totalFrac, 'para')
print "Sum of returns: " + str(totalLenTest)


chs = re.split('CHAPTER', text)
chs = chs[1:]
total = len(chs)
print "\n\nSTATS BY CHAPTER\nNum Chs: " + str(total)
totalLenTest = 0
totalFrac = 0 
for i in range(1,6):
	totalLenTest = totalLenTest + partSum(i, totalLenTest, 'ch')
	totalFrac = totalFrac + partPercent(i, total, totalFrac, 'ch')
print "Sum of returns: " + str(totalLenTest)