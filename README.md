fast-formulaic-analysis
=======================

A program for finding formulas in poetic texts and calculating formulaic density. Essentially, it an incomparably faster
and more correct version of [this program](github.com/macleginn/poetic-formula-extractor-python).
There is a deep seated bug in the old version, but I keep it here since it was used in the presentation.
The usage is nearly identical except that now the algorithm takes the file object as input:

```python
with open("texts/Iliad.txt", "r", encoding = "utf-8") as inp:
   poem = Poem(inp, HOMERIC_GREEK_ALPHABET, EMPTY_STOPLIST)
print(round(poem.getFormulaicDensity(), 1))
print(poem.returnFormulasAsString()
poem.highlightFormulas("Iliad_highlited.html")
```
