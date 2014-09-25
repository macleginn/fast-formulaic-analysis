import re

# Supplementary data used in the testing code.

RUSSIAN_ALPHABET      = {'ё', 'я', 'ю', 'э', 'ь', 'ы', 'ъ', 'щ', 'ш', 'ч', 'ц', 'х', 'ф', 'у', 'т', 'с', 'р', 'п', 'о', 'н', 'м', 'л', 'к', 'й', 'и', 'з', 'ж', 'е', 'д', 'г', 'в', 'б', 'а', 'Я', 'Ю', 'Э', 'Ь', 'Ы', 'Ъ', 'Щ', 'Ш', 'Ч', 'Ц', 'Х', 'Ф', 'У', 'Т', 'С', 'Р', 'П', 'О', 'Н', 'М', 'Л', 'К', 'Й', 'И', 'З', 'Ж', 'Е', 'Д', 'Г', 'В', 'Б', 'А', 'Ё'}
RUSSIAN_STOP_LIST     = {'а', 'б', 'бы', 'в', 'вас', 'во', 'все', 'всё', 'вы', 'где', 'да', 'дак', 'для', 'до', 'его', 'ей', 'ему', 'если', 'ж', 'же', 'за', 'и', 'из', 'им', 'их', 'ише', 'к', 'как', 'ко', 'когда', 'кого', 'кому', 'ли', 'меж', 'между', 'меня', 'мне', 'мной', 'мня', 'моей', 'мой', 'моя', 'мы', 'на', 'надо', 'нас', 'наш' , 'не', 'ней', 'нем', 'ни', 'ним', 'но', 'о', 'об', 'обо' , 'он', 'она', 'они', 'от', 'перед', 'передо' , 'по', 'под', 'при', 'про', 'с', 'сам', 'со' , 'тебе', 'тебя', 'тем', 'тех', 'то', 'тогда', 'той', 'тот', 'тут' , 'ты', 'тя', 'у' 'уж', 'чем', 'что', 'я'}
ANGLO_SAXON_ALPHABET  = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'L', 'M', 'N', 'O', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'w', 'x', 'y', 'æ', 'ð', 'þ'}
ANGLO_SAXON_STOP_LIST = {'on', 'þæt', 'ond', 'he', 'wæs', 'þa', 'him', 'to', 'se', 'ne', 'ic', 'ða', 'þe', 'swa', 'þær', 'his', 'ðe', 'mid', 'æfter', 'ofer', 'ær', 'æt', 'under', 'wið', 'þonne', 'in', 'hie', 'ac', 'þone', 'þæs', 'Ic', 'þu', 'for', 'hine', 'me'}
HOMERIC_GREEK_ALPHABET = {'Α', 'Δ', 'Ε', 'Ζ', 'Η', 'Θ', 'Ι', 'Κ', 'Λ', 'Μ', 'Ν', 'Ο', 'Π', 'Ρ', 'Σ', 'Τ', 'Υ', 'Φ', 'Ω', 'α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'ς', 'σ', 'τ', 'υ', 'χ', 'ψ', 'ω', 'ϑ', 'ϕ', 'ϱ', 'ἀ', 'ἁ', 'ἂ', 'ἄ', 'ἅ', 'ἐ', 'ἑ', 'ἔ', 'ἕ', 'ἠ', 'ἡ', 'ἢ', 'ἣ', 'ἤ', 'ἥ', 'ἦ', 'ἧ', 'ἰ', 'ἱ', 'ἳ', 'ἴ', 'ἵ', 'ἶ', 'ἷ', 'ὀ', 'ὁ', 'ὃ', 'ὄ', 'ὅ', 'ὐ', 'ὑ', 'ὔ', 'ὕ', 'ὖ', 'ὗ', 'ὠ', 'ὡ', 'ὢ', 'ὣ', 'ὤ', 'ὥ', 'ὦ', 'ὧ', 'ὰ', 'ά', 'ὲ', 'έ', 'ὴ', 'ή', 'ὶ', 'ί', 'ὸ', 'ό', 'ὺ', 'ύ', 'ὼ', 'ώ', 'ᾗ', 'ᾤ', 'ᾧ', 'ᾶ', 'ᾷ', '᾽', 'ῂ', 'ῃ', 'ῆ', 'ῇ', '῎', 'ῖ', '῞', 'ῦ', 'ῳ', 'ῴ', 'ῶ', 'ῷ', '῾'}
HOMERIC_GREEK_STOPLIST = {'δ', 'καὶ', 'δὲ', 'τε', 'μὲν', 'οἱ', 'ἐν', 'δέ', 'ὣς', 'τ', 'ἀλλ', 'γὰρ', 'μοι', 'αὐτὰρ', 'ἐπὶ', 'τὸν', 'δὴ', 'τοι', 'ἐπεὶ', 'ἐς', 'ἐνὶ', 'μιν', 'οὐ', 'ὁ', 'κατὰ', 'ἄρα', 'ἄρ', 'τις', 'νῦν', 'ἐκ', 'καί', 'ὡς', 'γε', 'ἦ', 'γάρ', 'οὔ', 'ἐγὼ', 'τι', 'περ', 'ἠδὲ', 'κεν', 'ἐπ', 'οὐκ'}
EMPTY_STOPLIST         = {}

# Helper functions.

def clearWord(word, alphabet):
    buff = []
    for char in word:
        if char == "ё":
            buff.append("е")
        elif char in alphabet or (char == "-" and len(buff) > 0):
            buff.append(char)
    return "".join(buff)

def extractPWords(line, alphabet):
    pWordArr = []
    line = line.split()
    for word in line:
        word = clearWord(word, alphabet)
        if len(word) > 0:
            pWordArr.append(PoeticWord(word))
    return pWordArr

def makeKey(nGram, keylength):
    key = []
    if keylength <= 0:
        for word in nGram.pwords:
            key.append(word.word.lower())
    else:
        for word in nGram.pwords:
            key.append(word.word.lower()[0:keylength])
    return "".join(key)

def makeNGrams(lineArr, min, max, alphabet, stoplist):
    for length in reversed(range(min, max + 1)):
        for i in range(len(lineArr) - length + 1):
            nGram = lineArr[ i : i + length ]
            stopWords = 0
            for word in nGram:
                if clearWord(word.word.lower(), alphabet) in stoplist:
                    stopWords += 1
            if len(nGram) == 2:
                if stopWords == 0:
                    yield NGram(nGram)
            else:
                if stopWords <= len(nGram) / 2:
                    yield NGram(nGram)

# DataStructures

class PoeticWord:
    """A pword consisting of a string and a used-not-used marker. When used notifies its N-gram observers."""
    def __init__(self, word):
        self.word      = word
        self.blocked   = False
        self.observers = []

    def block(self):
        self.blocked = True
        for obs in self.observers:
            obs.blockOneWord(self)

    def unblock(self):
        self.blocked = False
        for obs in self.observers:
            obs.unblockOneWord(self)

    def isBlocked(self):
        return self.blocked

    def addObserver(self, obs):
        self.observers.append(obs)

    def __str__(self):
        return self.word

    __repr__ = __str__


class NGram:
    """An N-gram consisting of a PoeticWord array. It observes all the pwords it contains."""
    def __init__(self, pWordArr):
        self.pwords = pWordArr
        for pword in self.pwords:
            pword.addObserver(self)
        self.blockedWords = {}
        for pword in self.pwords:
            self.blockedWords[id(pword)] = False
        self.blocked = False

    def __len__(self):
        return len(self.pwords)

    def __str__(self):
        return(" ".join(str(el) for el in self.pwords))

    __repr__ = __str__

    def isBlocked(self):
        return self.blocked

    def blockOneWord(self, word):
        assert self.blockedWords[id(word)] == False
        self.blockedWords[id(word)] = True
        self.blocked                = True

    def unblockOneWord(self, word):
        assert self.blockedWords[id(word)] == True
        self.blockedWords[id(word)] = False
        for isBlocked in self.blockedWords.values():
            if isBlocked:
                self.blocked = True
                break
        else:
            self.blocked = False
    
    def block(self):
        for pword in self.pwords:
            pword.block()

    def unblock(self):
        for pword in self.pwords:
            pword.unblock()

class Poem:
    """A 2-dim array of PWords performing formulaic analysis on initialisation."""
    def __init__(self, fileObj, alphabet, stoplist, keylength, nRepetitions):
        self.alphabet = alphabet
        self.stoplist = stoplist
        self.keylength = keylength
        self.nRepetitions = nRepetitions
        self.pWordArr = []
        self.allKeys  = []
        self.allKeysSet = set()
        self.nGramMap = {}
        self.populate(fileObj)
        self.formulas  = {}
        self.firstWords = set()
        self.lastWords  = set()
        self.extractFormulas()
        self.formulaicDensity = 0
        self.computeFormulaicDensity()

    def populate(self, fileObj):
        """Populates the pword array and the nGram dictionary."""
        nGramsByLength = {}
        for line in fileObj:
            lineArr = extractPWords(line, self.alphabet)
            self.pWordArr.append(lineArr)
            for nGram in makeNGrams(lineArr, 2, 14, self.alphabet, self.stoplist):
                numericKey = len(nGram)
                key = makeKey(nGram, self.keylength)
                if numericKey not in nGramsByLength:
                    nGramsByLength[numericKey] = []
                if key not in self.allKeysSet:
                    nGramsByLength[numericKey].append(key)
                    self.allKeysSet.add(key)
                    self.nGramMap[key] = []
                    self.nGramMap[key].append(nGram)
                else:
                    self.nGramMap[key].append(nGram)
        for numKey in sorted(nGramsByLength, reverse = True):
            self.allKeys.extend(nGramsByLength[numKey])

    def extractFormulas(self):
        """Extract formulas from the dictionary."""
        for key in self.allKeys:
            if len(self.nGramMap[key]) < self.nRepetitions:
                continue
            candidates = self.nGramMap[key]
            temp       = []
            start      = 0
            for j in range(len(candidates) - 1):
                if not candidates[j].isBlocked():
                    temp.append(candidates[j])
                    candidates[j].block()
                    start = j + 1
                    break    
            for i in range(start, len(candidates)):
                if not candidates[i].isBlocked():
                    temp.append(candidates[i])
                    candidates[i].block()
            if len(temp) >= self.nRepetitions:
                self.formulas[key] = []
                self.formulas[key].extend(temp)
                for nGram in temp:
                    self.firstWords.add(
                        id(nGram.pwords[0]
                            )
                        )
                    self.lastWords.add(
                        id(nGram.pwords[-1]
                            )
                        )
            elif len(temp) > 0:
                for nGram in temp:
                    nGram.unblock()

    def computeFormulaicDensity(self):
        allWordsN  = 0
        usedWordsN = 0
        for line in self.pWordArr:
            for pword in line:
                if pword.isBlocked():
                    usedWordsN += 1
                allWordsN += 1
        self.formulaicDensity = usedWordsN / allWordsN * 100

    def getFormulaicDensity(self):
        return self.formulaicDensity

    def returnFormulasAsString(self):
        out = []
        for key in self.allKeys:
            if key in self.formulas:
                formulas = "; ".join(
                    " ".join(str(el) for el in nGram.pwords) for nGram in self.formulas[key]
                    )
                out.append(formulas)
        return("\n".join(out))

    def highlightFormulas(self, filename):
        """Prints formulas to an html file."""
        def _make_key(formula):
            formula = formula[1:-1].split()
            key = []
            for word in formula:
                key.append(word.lower()[:4])
            return ''.join(key)
        lines = []
        for line in self.pWordArr:
            temp = []
            for i in range(len(line)):
                if id(line[i]) in self.firstWords:
                    temp.append("[" + line[i].word)
                elif id(line[i]) in self.lastWords:
                    temp.append(line[i].word + "] ")
                else:
                    temp.append(line[i].word)
            lines.append(' '.join(temp))
        f_p = re.compile(r'\[[^\[\]]+?\]')
        lines_n = list(enumerate(lines, start = 1))
        formula_lines = {}
        for pair in lines_n:
            line = pair[1]
            for mobj in f_p.finditer(line):
                key = _make_key(mobj.group(0))
                if key not in formula_lines:
                    formula_lines[key] = []
                formula_lines[key].append(pair[0])
        with open(filename, "w", encoding = "utf-8") as out:
            out.write('<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body><table border=0>\n')
            for pair in lines_n:
                out.write('<tr>')
                out.write('<td>%s</td>' % str(pair[0]))
                out.write('<td>%s</td>' % str(pair[1]))
                refs = []
                for mobj in f_p.finditer(pair[1]):
                    key = _make_key(mobj.group(0))
                    if key in formula_lines:
                        refs.append(', '.join([str(el) for el in formula_lines[key] if el != pair[0]]))
                out.write('<td>%s</td>' % '; '.join(refs))
                out.write('</tr>')
            out.write("</table></body></html>\n")

# Client code.

def main():
    with open("texts/Iliad.txt", "r", encoding = "utf-8") as inp:
        poem = Poem(inp, HOMERIC_GREEK_ALPHABET, EMPTY_STOPLIST)
        print(round(poem.getFormulaicDensity(), 1))

if __name__ == '__main__':
    main()
    sys.exit(0)