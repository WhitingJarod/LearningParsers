from tokenizer import Tokenizer

class Parser:

    def parse(self, input: str):
        self._string = input
        self._tokenizer = Tokenizer(input)
        self._lookahead = self._tokenizer.getNextToken()
        return self.Program()

    
    # Main entry point.
    # Program
    #   : StatementList
    #   ;
    def Program(self):
        return {
            "type": "Program",
            "body": self.StatementList()
        }

    # StatementList
    #   : Statement
    #   | StatementList Statement -> Statement Statement Statement Statement
    #   ;
    def StatementList(self):
        statementList = [self.Statement()]
        while self._lookahead:
            statementList.append(self.Statement())
        return statementList
    
    # Statement
    #   : ExpressionStatement
    #   ;
    def Statement(self):
        return self.ExpressionStatement()
    
    # ExpressionStatement
    #   : Expression ";"
    #   ;
    def ExpressionStatement(self):
        expression = self.Expression()
        self._eat(';')
        return {
            "type": "ExpressionStatement",
            "expression": expression
        }
    
    # Expression
    #   : Literal
    #   ;
    def Expression(self):
        return self.Literal()

    # Literal
    #   : NumericLiteral
    #   | StringLiteral
    #   ;
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
    ";yeah 42";
    32;
    """))