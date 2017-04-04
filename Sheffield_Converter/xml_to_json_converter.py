import xml.etree.ElementTree as ET
import codecs
import sys
import os
import json


input_file = sys.argv[1]
out_file_name = os.path.splitext(input_file)[0]+'.json'
out_file = codecs.open(out_file_name,encoding='utf-8',mode='w')

tree = ET.parse(input_file)
root = tree.getroot()
corpus = []

def write(array,word,label,initial):
	for i,c in enumerate(word):
		if initial:
			array.append((c,label,"I"))
			#out_file.write(c + " " + label + " I\n")
			initial = False
		else: 
			array.append((c,label,"N"))
			#out_file.write(c + " " + label + " N\n")

for paragraph in root:
	for sentence in paragraph:
		#Create a new sentence Array
		sentence_arr = []
		#Loop through each word in the sentence
		for word in sentence:
			initial = True #Mark that this is the first character of the word
			label = word.tag #Save the original label to use in place of nested labels
			for character in word.itertext(): #Iterate through the nested characters
				write(sentence_arr,character,label,initial) 
				initial = False
		corpus.append(sentence_arr)

json.dump(corpus,out_file)
out_file.close()

