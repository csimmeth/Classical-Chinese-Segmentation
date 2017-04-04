import xml.etree.ElementTree as ET
import codecs
import sys
import os


input_file = sys.argv[1]
out_file_name = os.path.splitext(input_file)[0]+'.txt'
out_file = codecs.open(out_file_name,encoding='utf-8',mode='w')

tree = ET.parse(input_file)
root = tree.getroot()

def write(word,label,initial):
	for i,c in enumerate(word):
		if initial:
			out_file.write(c + " " + label + " I\n")
			initial = False
		else: 
			out_file.write(c + " " + label + " N\n")

for paragraph in root:
	for sentence in paragraph:
		for word in sentence:
			initial = True
			label = word.tag
			for character in word.itertext():
				write(character,label,initial)
				initial = False

		out_file.write('\n')		

out_file.close()