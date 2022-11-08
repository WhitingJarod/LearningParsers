import re
Spec = [
    [re.compile("^\d+"), "NUMBER"],
    [re.compile("^\"[^\"]*\""), "STRING"],
    [re.compile("^\'[^\']*\'"), "STRING"],
    [re.compile("^\s+"), None],
    [re.compile("^//.*\n"), None],
    [re.compile("/\*[\s\S]*\*/"), None]
]


class Tokenizer:

    def __init__(self, input: str):
        self._string = input
        self._cursor = 0

    def atCursor(self):
        return self._string[self._cursor:self._cursor+1]

    def isEOF(self):
        return self._cursor == len(self._string)

    def hasMoreTokens(self):
        return self._cursor < len(self._string)

    def getNextToken(self):
        if not self.hasMoreTokens():
            print("EOF")
            return None

        string = self._string[self._cursor:]
        for spec in Spec:
            value = self._match(spec[0], string)
            if value == None: continue
            if spec[1] == None: return self.getNextToken()
            return {
                "type": spec[1],
                "value": value
            }

        raise Exception("Unexpected token at position {}: {}".format(self._cursor, string[0:1]))

    def _match(self, exp, string):
        mat = exp.match(string)
        if mat:
            self._cursor += len(mat.group(0))
            return mat.group(0)
