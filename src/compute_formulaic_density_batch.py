#! /usr/bin/env python3

# This script computes formulaic densities of all files in a directory
# (and its subdirectories, which it traverses recursively) and prints
# the average, standard deviation, and quantiles to the console.
# Files should be in UTF-8, and their names should not start with .
# Full results are put into report.csv which can be viewed in any
# decent spreadsheet editor or data-handling software package to enable all
# kinds of sorting and additional analysis.

from FormulaicAnalysisLib import *
import sys
import ast
import re
import os.path
import math

# We provide our versions of statistical functions
# to ensure compatibility with pre-3.4 versions
# of Python 3.

def mean(vals):
    return round(sum(vals) / len(vals), 1)


def sd(vals, xbar=None):
    """Sample standard deviation."""
    if xbar == None:
        xbar = mean(vals)
    N = len(vals)
    return round(math.sqrt(sum([(x - xbar) ** 2 for x in vals]) / (N - 1)), 1)


def percentile(p, vals):
    """Calculates percentiles using method #4 from
    ‘Quartiles in Elementary Statistics’ by Eric Langford,
    Journal of Statistics Education Volume 14, Number 3 (2006),
    www.amstat.org/publications/jse/v14n3/langford.html"""

    if p >= 1:
        return vals[-1]
    elif p <= 0:
        return vals[0]
    np = p * 1.0 * len(vals)
    if np.is_integer():
        return (vals[int(np)] + vals[int(np + 1)]) / 2
    else:
        return vals[math.ceil(np)]


def count_lines_and_words(file_obj):
    n_lines = 0
    n_words = 0
    for line in file_obj:
        for char in line:
            if char in ALPHABET:
                n_lines += 1
                break
        candidate_words = line.split()
        for c_word in candidate_words:
            for char in c_word:
                if char in ALPHABET:
                    n_words += 1
                    break
    return n_lines, n_words


if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help', 'help'}:
    print('Usage: python3 %s path_to_directory_with_texts' % sys.argv[0])
    sys.exit(0)

path_to_input = sys.argv[-1]

if not os.path.exists(path_to_input):
    print('Error: %s not found' % path_to_input)
    sys.exit(1)
elif not os.path.isdir(path_to_input):
    print('Error: %s is not a directory')
    sys.exit(1)

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
if not STOP_LIST:
    print('Error: unable to recover stop-list from the configuration file')
    sys.exit(1)
if KEY_LENGTH == None:
    print('Error: unable to recover key length from the configuration file')
    sys.exit(1)
if OCCURRENCES == None:
    print('Error: unable to recover required number of occurrences from the configuration file')
    sys.exit(1)

# Processing

n_lines = 0
n_words = 0

print('Processing texts from %s' % path_to_input)
results = {}
result_pairs = []
for root, dirs, files in os.walk(path_to_input):
    for filename in files:
        if filename.startswith('.'):
            continue
        next_file = os.path.join(root, filename)
        try:
            file_obj = open(next_file, 'r', encoding='utf-8')
        except IOError:
            print('Could not read %s, skipping' % next_file)
            break
        poem = Poem(file_obj, ALPHABET, STOP_LIST, KEY_LENGTH, OCCURRENCES)
        file_obj.seek(0)
        _n_lines, _n_words = count_lines_and_words(file_obj)
        n_lines += _n_lines
        n_words += _n_words
        results[next_file] = round(poem.getFormulaicDensity(), 1)
        result_pairs.append((os.path.basename(filename), round(poem.getFormulaicDensity(), 1)))
        file_obj.close()

# Computing statistics

res_vals = list(results.values())
res_vals.sort()
xbar = mean(res_vals)
stdev = sd(res_vals, xbar)
min_val = res_vals[0]
first_quartile = percentile(0.25, res_vals)
median = percentile(0.5, res_vals)
third_quartile = percentile(0.75, res_vals)
max_val = res_vals[-1]

# Printing the results

col_width = 30
print()
print('%d texts in %s' % (len(res_vals), path_to_input))
print('%d lines and %d words in total' % (n_lines, n_words))
print('Mean formulaic density:'.ljust(col_width), end='')
print(xbar)
print('Sample standard deviation:'.ljust(col_width), end='')
print(stdev)
print('Min:'.ljust(col_width), end='')
print(min_val)
print('First quartile:'.ljust(col_width), end='')
print(first_quartile)
print('Median:'.ljust(col_width), end='')
print(median)
print('Third quartile:'.ljust(col_width), end='')
print(third_quartile)
print('Max:'.ljust(col_width), end='')
print(max_val)
print()
with open('report.csv', 'w', encoding='utf-8') as out:
    for pair in result_pairs:
        out.write('%s,%.1f\n' % (pair[0], pair[1]))
print('Full report was written to report.csv')