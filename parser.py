from tokenizer import Tokenizer

class Parser:

    def parse(self, input: str):
        self._string = input
        self._tokenizer = Tokenizer(input)
        self._lookahead = self._tokenizer.getNextToken()
        return self.Program()

    
    # Main entry point.
    #
    # Literal
    #   : NumericLiteral
    #   | StringLiteral
    #   ;
    #
    def Program(self):
        return {
            "type": "Program",
            "body": self.Literal()
        }
    
    def Literal(self):
        if self._lookahead["type"] == "NUMBER":
            return self.NumericLiteral()
        elif self._lookahead["type"] == "STRING":
            return self.StringLiteral()

    def NumericLiteral(self):
        token = self._eat("NUMBER")
        return {
            "type": "NumericLiteral",
            "value": float(token["value"])
        }
    
    def StringLiteral(self):
        token = self._eat("STRING")
        return {
            "type": "StringLiteral",
            "value": token["value"][1:-1]
        }
    
    def _eat(self, tokenType):
        token = self._lookahead
        if token == None:
            raise Exception("Expected {}, got EOF".format(tokenType))
        if token["type"] != tokenType:
            raise Exception("Expected {}, got {}", tokenType, token["type"])
        self._lookahead = self._tokenizer.getNextToken()
        return token

if __name__ == "__main__":
    print(Parser().parse("""
    /* This is a
    multiline comment
    Yeah boi
    */
    "yeah 42"
    """))