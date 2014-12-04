fast-formulaic-analysis
=======================

A program for finding formulas in poetic texts and calculating formulaic density. Essentially, it is an incomparably faster and more correct version of [this program](http://github.com/macleginn/poetic-formula-extractor-python).
There is a deep seated bug in the old version, but I keep it here since it was used in the presentation.

The program consists of four files, which should reside in the same directory.

```FormulaicAnalysisLib.py``` is a library containing classes and functions implementing the algorithm.

```alpha_stop.conf``` is a configuration file containing the alphabet, the stop list, the formulaic key length, and the number of occurrences, which make a repeated N-gram qualify as a formula. All these parameters, except stop-list, must be non-empty.

```compute_formulaic_density.py``` is a script that computes formulaic density of a single text based on the parameters in the configuration file. The usage is

```python3 compute_formulaic_density.py [options] pathToFileWithText```

Options include ```-s``` (show formulas on the screen) and ```-f``` (create an html file with the text with formulas in square brackets and cross-references). These arguments can be used separately or combined as ```-sf``` or ```-fs```. If the path is a directory, a random file therefrom will be selected.

```compute_formulaic_density_batch.py``` is a script for computing formulaic density of all files in a given directory. The usage is

```python3 compute_formulaic_density_batch.py pathToDirectory```

Text files should be in UTF-8 and their names should not start with ‘.’. The script prints the number of texts (i.e. files), lines, and words on the screen, as well as the mean formulaic density, sample standard deviation, and quartiles. The full report is written to ```report.csv```.
