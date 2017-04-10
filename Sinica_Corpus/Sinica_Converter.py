# Jiayi Yao

import sys
import os

input_name = sys.argv[1]
output_name = os.path.splitext(input_name)[0]+'c.txt'

punctuations = ['，','。','：','；','？','！','、']

input_f = open(input_name, encoding='utf-8', mode='r')
text = input_f.read()
output_f = open(output_name, encoding='utf-8', mode='w')

for c in text:
	if c in punctuations:
		output_f.write(c+" Punctuation"+" I\n")

output_f.write(text)

input_f.close()
output_f.close()



