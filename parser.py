from tokenizer import Tokenizer
import json

AST_MODE = "default"

class DefaultFactory:
    def Program(body):
        return {
            "type": "Program",
            "body": body,
        }
    
    def EmptyStatement():
        return {"type": "EmptyStatement"}
    
    def BlockStatement(body):
        return {
            "type": "BlockStatement",
            "body": body
        }
    
    def ExpressionStatement(expression):
        return {
            "type": "ExpressionStatement",
            "expression": expression
        }
    
    def StringLiteral(value):
        return {
            "type": "StringValue",
            "value": value
        }
    
    def NumericLiteral(value):
        return {
            "type": "NumericLiteral",
            "value": value
        }

class SExpressionFactory:
    def Program(body):
        return ["begin", body]
    
    def EmptyStatement():
        return
    
    def BlockStatement(body):
        return ["begin", body]
    
    def ExpressionStatement(expression):
        return expression
    
    def StringLiteral(value):
        return "\"{}\"".format(value)
    
    def NumericLiteral(value):
        return value
    
factory = AST_MODE == "default" and DefaultFactory or SExpressionFactory
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
        return factory.Program(self.StatementList())
        # return {
        #     "type": "Program",
        #     "body": self.StatementList()
        # }

    # StatementList
    #   : Statement
    #   | StatementList Statement -> Statement Statement Statement Statement
    #   ;
    def StatementList(self, stopLookahead = None):
        statementList = [self.Statement()]
        while self._lookahead and self._lookahead["type"] != stopLookahead:
            statementList.append(self.Statement())
        return statementList
    
    # Statement
    #   : ExpressionStatement
    #   | BlockStatement
    #   | EmptyStatement
    #   ;
    def Statement(self):
        if self._lookahead["type"] == "{":
            return self.BlockStatement()
        elif self._lookahead["type"] == ";":
            return self.EmptyStatement()
        else:
            return self.ExpressionStatement()
    
    # EmptyStatement
    # : ";"
    # ;
    def EmptyStatement(self):
        self._eat(";")
        return {
            "type": "EmptyStatement"
        }    
    # BlockStatement
    #   : "{" Optional StatementList "}"
    #   ;
    def BlockStatement(self):
        self._eat("{")
        body = self._lookahead["type"] != "}" and self.StatementList("}") or [];
        self._eat("}")
        return factory.BlockStatement(body)
    
    # ExpressionStatement
    #   : Expression ";"
    #   ;
    def ExpressionStatement(self):
        expression = self.Expression()
        self._eat(';')
        return factory.ExpressionStatement(expression)
    
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
        return factory.NumericLiteral(float(token["value"]))
    
    def StringLiteral(self):
        token = self._eat("STRING")
        return factory.StringLiteral(token["value"][1:-1])
    
    def _eat(self, tokenType):
        token = self._lookahead
        if token == None:
            raise Exception("Expected {}, got EOF".format(tokenType))
        if token["type"] != tokenType:
            raise Exception("Expected {}, got {}", tokenType, token["type"])
        self._lookahead = self._tokenizer.getNextToken()
        return token


if __name__ == "__main__":
    parsed = Parser().parse("""
        /* This is a
        multiline comment
        Yeah boi
        */
        ";yeah 42";
        32;
        { // New block yeah!
            112;
            {
                "Another block deep!";
            }
        }
    """)
    out = open("parsed.json", "w")
    print(json.dump(parsed, out))
    out.close()
