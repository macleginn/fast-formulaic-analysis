fast-formulaic-analysis
=======================

A program for finding formulas in poetic texts and calculating formulaic density. Essentially, it is an incomparably faster
and more correct version of [this program](http://github.com/macleginn/poetic-formula-extractor-python).
There is a deep seated bug in the old version, but I keep it here since it was used in the presentation.
The usage is nearly identical except that now the algorithm takes a file object as input:

```python
with open("texts/Iliad.txt", "r", encoding = "utf-8") as inp:
   poem = Poem(inp, HOMERIC_GREEK_ALPHABET, EMPTY_STOPLIST)
print(round(poem.getFormulaicDensity(), 1))
print(poem.returnFormulasAsString()
poem.highlightFormulas("Iliad_highlited.html")
```
