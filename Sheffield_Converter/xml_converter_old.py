import xml.etree.ElementTree as ET
import codecs
import sys
import os


input_file = sys.argv[1]
out_file_name = os.path.splitext(input_file)[0]+'.txt'
out_file = codecs.open(out_file_name,encoding='utf-8',mode='w')

tree = ET.parse(input_file)
root = tree.getroot()

for paragraph in root:
	for sentence in paragraph:
		for word in sentence:
				if word.text is not None:
					for i, c in enumerate(word.text):
						if i is 0:
							out_file.write(c + " " + word.tag + " I\n")
						else: 
							out_file.write(c + " " + word.tag + " N\n")

out_file.close()