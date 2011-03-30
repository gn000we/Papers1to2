#! /usr/bin/python

# Converts a latex file with Papers 1 citations to Papers 2 citations using bibtex libraries

# Program name - papers1to2.py
# Written by - Tim Crawford (cstc@swansea.ac.uk)
# Date (YYYYMMDD) and version No (.d):  20110330.1

# This program uses two bibtex libraries (one generated from Papers 1 and one generated from Papers 2)
# and a Latex file with the citations from Papers 1 in it
# It runs through all the bibtex entries for Papers 1 and Papers 2 and builds a corresponding array
# The code finally generates a new Latex file with the Papers 2 citations in place of the original Papers 1 citations

# As this is my first Python development I have been stringent in variable declarations and in copy and pasting code.
# There are blatent ways of improving this and feel free to comment

# LEGAL
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above permission notice shall be included in all copies or substantial 
# portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

#start vars
#filenames: change accrodingly
oldPapersBibFile = './bibs/old_papers1.bib' 
newPapersBibFile = './bibs/new_papers2.bib'
latexFile = './bibs/my_current_papers1_latex.tex'
newLatexFile = './new_latex_with_paper2_citations.tex'

#permissions on files
permissionsOnOld = 'r'
permissionsOnNew = 'r'
permissionsOnLatex = 'r'
permissionsOnNewLatex = 'w'

#identification of cite 
symbol = '@'
citeSymbol = '{'
endCiteSymbol = ','

#identification of title 
oldTitleSymbol = 'title = {'
oldEndTitleSymbol = '},'
newTitleSymbol = oldTitleSymbol + '{'
newEndTitleSymbol = '}' + oldEndTitleSymbol

#arrays of info
oldCites = []
oldTitles = []
newCites = []
newTitles = []
oldIndexInNew = [] 
#from the old titles, the corresponding new cites can be mapped e.g. if oldTitles[45] = newTitles[23], then oldCites[45] is in exact relation to newCites[23], so oldIndexInNew[45] = 23.

#temp vars
cite = ''
title = ''
whereComma = ''
begCite = 0
whereEndTitle = 0
testline = ''
theNewBit = ''

#cite template
citeTemplateBegin = '\cite{'
citeTemplateEnd = '}'
theOldCitation = ''
theNewCitation = ''

#>>>> prog start

#get all info from old bibtex (corresponding cites and titles)

f = open(oldPapersBibFile,permissionsOnOld)
#print f #file info

print '\n seeking old bib for cites and titles \n'

while True: 
	testline = f.readline()
	if len(testline) == 0:
		break #eof
	if symbol in testline[0]:
		if citeSymbol in testline:
			begCite = testline.find(citeSymbol) + 1
			#print '%s has cite on %d' % (testline,begCite)
			whereComma = testline.find(endCiteSymbol)
			cite = testline[begCite:whereComma]
	if oldTitleSymbol in testline:
		whereEndTitle = testline.find(oldEndTitleSymbol)
		title = testline[9:whereEndTitle]
		title = title.lower()
		print 'Old cite is %s' % (cite)
		print 'Title is %s \n\n' % (title)
		oldTitles.append(title)
		oldCites.append(cite)	
	#print f.read()
		#print testline
	
f.close()

print '\n now seeking new bib for titles and replacement cites \n'

#compare old titles with new titles, if same, then grab new cite

#open new bibtex
f = open(newPapersBibFile,permissionsOnNew)
#print f #file info

#print 'new title symbol %s, new end title %s' % (newTitleSymbol, newEndTitleSymbol)

while True: 
	testline = f.readline() 
	#print testline
	if len(testline) == 0:
		break #eof
	if symbol in testline[0]:
		if citeSymbol in testline:
			begCite = testline.find(citeSymbol) + 1
			#print '%s has cite on %d' % (testline,begCite)
			whereComma = testline.find(endCiteSymbol)
			cite = testline[begCite:whereComma]
	if newTitleSymbol in testline:
		whereEndTitle = testline.find(newEndTitleSymbol)
		title = testline[10:whereEndTitle]
		title = title.lower()
		print '\n' + cite
		print title
		newTitles.append(title)
		newCites.append(cite)

f.close()

print '\n now replace the old citeations in the latex file with new citations from papers2 \n'
f = open(latexFile,permissionsOnLatex)
print f

newfile = open(newLatexFile,permissionsOnNewLatex)

for ot in oldTitles:
	nti = newTitles.index(ot)
	oldIndexInNew.append(nti)
	#print '%d index of %s' % (nti,ot)
			

while True: 
	testline = f.readline() 
	print 'OLD= %s' % (testline)	
	if len(testline) == 0:
		break #eof
	for i in oldCites:
		theOldCitation = citeTemplateBegin + i + citeTemplateEnd
		theNewBit = newCites[oldIndexInNew[oldCites.index(i)]]
		theNewCitation = citeTemplateBegin + theNewBit + citeTemplateEnd
		#print 'old cite = %s, corresponding cite in new = %s' % (theOldCitation,theNewCitation)
		if (theOldCitation) in testline:
			testline = testline.replace(theOldCitation,theNewCitation)
			print 'NEW=%s' % (testline)		
	newfile.write(testline)	


f.close()
newfile.close()		

