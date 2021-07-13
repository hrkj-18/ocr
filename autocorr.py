import  grammar_check
from autocorrect import spell
A='th waather is hott'
#B=spell(A)
#print(B)
list=[]

#tool = grammar_check.LanguageTool('en-GB')


# split the text
words = A.split()

# for each word in the line:
for word in words:

	#print(word)
	B=spell(word)
	list.append(B)
str1 = ''.join(str(e) + ' ' for e in list)
print(str1)





