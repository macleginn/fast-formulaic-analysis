#! /usr/bin/env python3

# This is the client code for FormulaicAnalysisLib.py,
# which is presumed to be present in the same directory.
# Usage: python3 compute_formulaic_density.py [options] pathToFileWithText
# Options include -s (show formulas on the screen) and -f
# (create an html file with the text with formulas in square
# brackets). These arguments can be used separately or combined as -sh or -hs.
# The alphabet and stop-list for the analysis are taken from
# alpha_stop.conf. Several options (Russian, Anglo-Saxon, and Homeric Greek)
# are provided there.

from FormulaicAnalysisLib import *
import sys
import ast
import re
import os.path

if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help', 'help'}:
	print('Usage: python3 %s [-sf] path_to_file_with_text' % sys.argv[0])
	sys.exit(0)

show_formulas_on_screen = False
output_to_html			= False

for arg in sys.argv[1:]:
	if arg[0] == '-':
		for char in arg[1:]:
			if char == 's':
				show_formulas_on_screen = True
			elif char == 'f':
				output_to_html = True
			else:
				print('An unrecognised option: %s' % char)
				sys.exit(1)

path_to_input = sys.argv[-1]

# Populating alphabet and stop-list

ALPHABET  = set()
STOP_LIST = set()

try:
	with open('alpha_stop.conf', 'r', encoding = 'utf-8') as inp:
		for line in inp:
			if line.startswith('ALPHABET'):
				line = line.strip('\n')
				fields = re.split(r'\s*=\s*', line)
				ALPHABET = ast.literal_eval(fields[1])
			elif line.startswith('STOP_LIST'):
				line = line.strip('\n')
				fields = re.split(r'\s*=\s*', line)
				STOP_LIST = ast.literal_eval(fields[1])
except FileNotFoundError:
	print('Error: configuration file alpha_stop.conf not found')
	sys.exit(1)

if not ALPHABET or not STOP_LIST:
	print('Error: unable to recover alphabet and stop-list from the configuration file')
	sys.exit(1)

# Opening input file for processing

try:
	file_with_text = open(path_to_input, 'r', encoding = 'utf-8')
except FileNotFoundError:
	print('Error: input file %s not found' % path_to_input)
	sys.exit(1)

# Computing formulaic density and presenting the results

poem = Poem(file_with_text, ALPHABET, STOP_LIST)
file_with_text.close()
print(round(poem.getFormulaicDensity(), 1))
if show_formulas_on_screen:
	print(poem.returnFormulasAsString())
if output_to_html:
	filename = os.path.basename(path_to_input)
	dot_index = filename.rfind('.')
	if dot_index == -1:
		filename += '.html'
	else:
		filename = filename[:dot_index] + '.html'
	poem.highlightFormulas(filename)