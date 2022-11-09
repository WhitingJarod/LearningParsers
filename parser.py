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
    
    def BinaryExpression(operator, left, right):
        return {
            "type": "BinaryExpression",
            "operator": operator["value"],
            "left": left,
            "right": right
        }

    def AssignmentExpression(operator, left, right):
        return {
            "type": "AssignmentExpression",
            "operator": operator,
            "left": left,
            "right": right
        }

    def ExpressionStatement(expression):
        return {
            "type": "ExpressionStatement",
            "expression": expression
        }

    def StringLiteral(value):
        return {
            "type": "StringLiteral",
            "value": value
        }

    def NumericLiteral(value):
        return {
            "type": "NumericLiteral",
            "value": value
        }
    
    def Identifier(name):
        return {
            "type": "Identifier",
            "name": name
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
    def StatementList(self, stopLookahead=None):
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
        return factory.EmptyStatement()

    # BlockStatement
    #   : "{" Optional StatementList "}"
    #   ;
    def BlockStatement(self):
        self._eat("{")
        body = self._lookahead["type"] != "}" and self.StatementList("}") or []
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
    #   | AdditiveExpression
    #   ;
    def Expression(self):
        return self.AssignmentExpression()
    
    # AssignmentExpression
    #   : AdditiveExpression
    #   | LeftHandSideExpression AssignmentOperator AssignmentExpression
    def AssignmentExpression(self):
        left = self.AdditiveExpression()
        if not self._isAssignmentOperator(self._lookahead["type"]):
            return left
        return factory.AssignmentExpression(self.AssignmentOperator()["value"], self._checkValidAssignmentTarget(left), self.AssignmentExpression())       

    # AssignmentOperator
    #   : SIMPLE_ASSIGN
    #   | COMPLEX_ASSIGN
    #   ;
    def AssignmentOperator(self):
        if self._lookahead["type"] == "SIMPLE_ASSIGN":
            return self._eat("SIMPLE_ASSIGN")
        else:
            return self._eat("COMPLEX_ASSIGN")
    
    # LeftHandSideExpression
    #   : Identifier
    #   ;
    def LeftHandSideExpression(self):
        return self.Identifier()
    
    # Identifier
    #   : IDENTIFIER
    #   ;
    def Identifier(self):
        return factory.Identifier(self._eat("IDENTIFIER")["value"])

    def _isAssignmentOperator(self, type):
        return type == "SIMPLE_ASSIGN" or type == "COMPLEX_ASSIGN"

    def _checkValidAssignmentTarget(self, node):
        if node["type"] == "Identifier":
            return node
        raise Exception("Invalid identifier: {}", node)

    def _BinaryExpression(self, builder, token):
        left = builder()
        while self._lookahead["type"] == token:
            left = factory.BinaryExpression(self._eat(token), left, builder())
        return left

    # AdditiveExpression
    #   : MultiplicativeExpression MULTIPLICATIVE_OPERATOR Literal
    #   | AdditiveExpression ADDITIVE_OPERATOR Literal
    #   ;
    def AdditiveExpression(self):
        return self._BinaryExpression(self.MultiplicativeExpression, "ADDITIVE_OPERATOR")

    # MultiplicativeExpression
    #   : PrimaryExpression
    #   | MultiplicativeExpression MULTIPLICATIVE_OPERATOR PrimaryExpression
    #   ;
    def MultiplicativeExpression(self):
        return self._BinaryExpression(self.PrimaryExpression, "MULTIPLICATIVE_OPERATOR")
    
    # PrimaryExpression
    #   : Literal
    #   | ParenthesizedExpression
    #   | LeftHandSideExpression
    #   ;
    def PrimaryExpression(self):
        if self._isLiteral(self._lookahead["type"]):
            return self.Literal()
        elif self._lookahead["type"] == "(":
            return self.ParenthesizedExpression()
        else:
            return self.LeftHandSideExpression()
    
    def _isLiteral(self, type):
        return type == "STRING" or type == "NUMBER"

    # ParenthesizedExpression
    #   : "(" Expression ")"
    #   ;
    def ParenthesizedExpression(self):
        self._eat("(")
        expression = self.Expression()
        self._eat(")")
        return expression

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
        a+=1;
    """)
    out = open("parsed.json", "w")
    print(json.dump(parsed, out))
    out.close()
