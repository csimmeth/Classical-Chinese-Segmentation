import codecs
import json
import sys
import os

from langconv import *

input_name = sys.argv[1]
output_name = os.path.splitext(input_name)[0]+'c.txt'

punctuations = ['，','。','：','；','？','！','、']

input_f = open(input_name, encoding='utf-8', mode='r')
output_f = open(output_name, encoding='utf-8', mode='w')

# Parse json
file_array = json.load(input_f)
for passage_obj in file_array:

	''' passage_obj has 2 keys: Text and Title'''
	text = passage_obj["Text"] 

	''' Convert from complex form of character to simplified Chinese character'''
	text = Converter('zh-hans').convert(text)
	# output_f.write(text+'\n')

	'''
		Each text has 3 lines:
		-> page header
		-> blank line
		-> article
	'''
	lines = text.splitlines()
	line = lines[2]

	''' Process the article'''
	word, tag = "", ""
	seek_word, seek_tag, in_bracket = True, False, False
	for c in line:
		# Information in brackets will be ignored
		if in_bracket:
			if c == ']':
				in_bracket = False
			else:
				continue
		# If character is in parenthes it is part of tag
		elif seek_tag:
			# Find a tag, write each character of the word into file
			if c == ')':
				seek_tag = False
				if word != "":
					output_f.write(word[0] + " " + tag + " I\n")
					for ch in word[1:]:
						output_f.write(ch + " " + tag + " N\n")
					word = ""
				tag = ""
			else:
				tag += c
		# If c is not in a tag or in brackets
		else:
			if c in  punctuations:
				# blank line after a punctuation
				output_f.write(c + " Punctuation I\n\n")
			elif c == '(':
				seek_tag = True
			elif c == '[':
				in_bracket = True
			elif ord(c) in range(ord('\u4e00'), ord('\u9fff')+1):
				word += c

input_f.close()
output_f.close()









