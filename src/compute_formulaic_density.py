#! /usr/bin/env python3

# This is the client code for FormulaicAnalysisLib.py,
# which is presumed to be present in the same directory.
# Usage: python3 compute_formulaic_density.py [options] pathToFileWithText
# If the path is a directory, a random file therefrom will
# be selected (use compute_formulaic_density_batch.py for
# large-scale analyses).
# Options include -s (show formulas on the screen) and -f
# (create an html file with the text with formulas in square
# brackets and cross-references). These arguments can be used separately
# or combined as -sf or -fs.
# The alphabet and stop-list for the analysis are taken from
# alpha_stop.conf. Russian, Anglo-Saxon, and Homeric Greek data
# are already provided there; un-comment relevant lines.

from FormulaicAnalysisLib import *
import sys
import ast
import re
import os
import os.path
import random

if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help', 'help'}:
    print('Usage: python3 %s [-sf] path_to_file_with_text' % sys.argv[0])
    sys.exit(0)

show_formulas_on_screen = False
output_to_html = False

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

# Retrieving configuration

ALPHABET = set()
STOP_LIST = set()
KEY_LENGTH = None
OCCURRENCES = None

try:
    with open('alpha_stop.conf', 'r', encoding='utf-8') as inp:
        for line in inp:
            if line.startswith('ALPHABET'):
                line = line.strip('\n')
                fields = re.split(r'\s*=\s*', line)
                ALPHABET = ast.literal_eval(fields[1])
            elif line.startswith('STOP_LIST'):
                line = line.strip('\n')
                fields = re.split(r'\s*=\s*', line)
                STOP_LIST = ast.literal_eval(fields[1])
            elif line.startswith('KEY_LENGTH'):
                line = line.strip('\n')
                fields = re.split(r'\s*=\s*', line)
                KEY_LENGTH = int(fields[1])
            elif line.startswith('OCCURRENCES'):
                line = line.strip('\n')
                fields = re.split(r'\s*=\s*', line)
                OCCURRENCES = int(fields[1])
except FileNotFoundError:
    print('Error: configuration file alpha_stop.conf not found')
    sys.exit(1)

if not ALPHABET:
    print('Error: unable to recover alphabet from the configuration file')
    sys.exit(1)
if KEY_LENGTH == None:
    print('Error: unable to recover key length from the configuration file')
    sys.exit(1)
if OCCURRENCES == None:
    print('Error: unable to recover number of occurrences from the configuration file')
    sys.exit(1)

# Opening input file for processing

if not os.path.exists(path_to_input):
    print('Error: input file %s not found' % path_to_input)
    sys.exit(1)

if not os.path.isdir(path_to_input):
    final_path = path_to_input
    try:
        file_with_text = open(final_path, 'r', encoding='utf-8')
    except IOError:
        print('Error: unable to read input file %s' % path_to_input)
        sys.exit(1)
else:
    print('Selecting a random file from %s' % path_to_input)
    filenames = []
    for root, dirs, files in os.walk(path_to_input):
        for filename in files:
            if not filename.startswith('.') and filename.endswith('txt'):
                filenames.append(os.path.join(root, filename))
    try:
        final_path = random.choice(filenames)
        file_with_text = open(final_path, 'r', encoding='utf-8')
    except IOError:
        print('Error: unable to read input file %s' % path_to_input)
        sys.exit(1)


# Computing formulaic density and presenting the results

poem = Poem(file_with_text, ALPHABET, STOP_LIST, KEY_LENGTH, OCCURRENCES)
file_with_text.close()
print(final_path)
print(round(poem.getFormulaicDensity(), 1))
if show_formulas_on_screen:
    print(poem.returnFormulasAsString())
if output_to_html:
    filename = 'html_out/' + os.path.basename(final_path)
    dot_index = filename.rfind('.')
    if dot_index == -1:
        filename += '.html'
    else:
        filename = filename[:dot_index] + '.html'
    print('Writing to %s' % filename)
    poem.highlightFormulas(filename)