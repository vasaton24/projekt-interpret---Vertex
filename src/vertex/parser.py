"""Parser module with integrated AST nodes."""

from typing import List, Union
from .exceptions import VertexSyntaxError
from .lexer import Token

class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value: int) -> None:
        self.value: int = value

class IdentifierNode(ASTNode):
    def __init__(self, name: str) -> None:
        self.name: str = name

class ListNode(ASTNode):
    def __init__(self, elements: List[ASTNode]) -> None:
        self.elements: List[ASTNode] = elements

class IndexNode(ASTNode):
    def __init__(self, left: ASTNode, index: ASTNode) -> None:
        self.left: ASTNode = left
        self.index: ASTNode = index

class BinOpNode(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode) -> None:
        self.left: ASTNode = left
        self.op: str = op
        self.right: ASTNode = right

class AssignNode(ASTNode):
    def __init__(self, name: str, value: ASTNode) -> None:
        self.name: str = name
        self.value: ASTNode = value

class ListAssignNode(ASTNode):
    def __init__(self, left: IndexNode, value: ASTNode) -> None:
        self.left: IndexNode = left
        self.value: ASTNode = value

class PrintNode(ASTNode):
    def __init__(self, expression: ASTNode) -> None:
        self.expression: ASTNode = expression

class IfNode(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_branch: Union[ASTNode, None]) -> None:
        self.condition: ASTNode = condition
        self.then_branch: ASTNode = then_branch
        self.else_branch: Union[ASTNode, None] = else_branch

class WhileNode(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode) -> None:
        self.condition: ASTNode = condition
        self.body: ASTNode = body

class ForNode(ASTNode):
    def __init__(self, init: Union[ASTNode, None], condition: Union[ASTNode, None], update: Union[ASTNode, None], body: ASTNode) -> None:
        self.init: Union[ASTNode, None] = init
        self.condition: Union[ASTNode, None] = condition
        self.update: Union[ASTNode, None] = update
        self.body: ASTNode = body

class BlockNode(ASTNode):
    def __init__(self, statements: List[ASTNode]) -> None:
        self.statements: List[ASTNode] = statements

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens: List[Token] = tokens
        self.pos: int = 0

    def current(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token("EOF", "")

    def consume(self, expected_type: str) -> Token:
        tok: Token = self.current()
        if tok.type != expected_type:
            raise VertexSyntaxError(f"Expected {expected_type}, got {tok.type}")
        self.pos += 1
        return tok

    def parse(self) -> BlockNode:
        statements: List[ASTNode] = []
        while self.current().type != "EOF":
            statements.append(self.parse_statement())
        return BlockNode(statements)

    def parse_statement(self) -> ASTNode:
        if self.current().type == "PRINT":
            self.consume("PRINT")
            expr = self.parse_expression()
            self.consume("SEMI")
            return PrintNode(expr)
        elif self.current().type == "IF":
            self.consume("IF")
            self.consume("LPAREN")
            cond = self.parse_expression()
            self.consume("RPAREN")
            then_branch = self.parse_block_or_statement()
            else_branch = None
            if self.current().type == "ELSE":
                self.consume("ELSE")
                else_branch = self.parse_block_or_statement()
            return IfNode(cond, then_branch, else_branch)
        elif self.current().type == "WHILE":
            self.consume("WHILE")
            self.consume("LPAREN")
            cond = self.parse_expression()
            self.consume("RPAREN")
            body = self.parse_block_or_statement()
            return WhileNode(cond, body)
        elif self.current().type == "FOR":
            self.consume("FOR")
            self.consume("LPAREN")
            init = None
            if self.current().type != "SEMI":
                init = self.parse_expression()
            self.consume("SEMI")
            cond = None
            if self.current().type != "SEMI":
                cond = self.parse_expression()
            self.consume("SEMI")
            update = None
            if self.current().type != "RPAREN":
                update = self.parse_expression()
            self.consume("RPAREN")
            body = self.parse_block_or_statement()
            return ForNode(init, cond, update, body)
        elif self.current().type == "LBRACE":
            return self.parse_block_or_statement()
        else:
            expr = self.parse_expression()
            self.consume("SEMI")
            return expr

    def parse_block_or_statement(self) -> ASTNode:
        if self.current().type == "LBRACE":
            self.consume("LBRACE")
            statements: List[ASTNode] = []
            while self.current().type not in ("RBRACE", "EOF"):
                statements.append(self.parse_statement())
            self.consume("RBRACE")
            return BlockNode(statements)
        return self.parse_statement()

    def parse_expression(self) -> ASTNode:
        return self.parse_assignment()

    def parse_assignment(self) -> ASTNode:
        expr = self.parse_comparison()
        if self.current().type == "ASSIGN":
            self.consume("ASSIGN")
            value = self.parse_assignment()
            if isinstance(expr, IdentifierNode):
                return AssignNode(expr.name, value)
            elif isinstance(expr, IndexNode):
                return ListAssignNode(expr, value)
            raise VertexSyntaxError("Invalid assignment target")
        return expr

    def parse_comparison(self) -> ASTNode:
        expr = self.parse_term()
        while self.current().type in ("EQ", "NE", "LT", "GT", "LE", "GE"):
            op_tok = self.current()
            self.pos += 1
            right = self.parse_term()
            expr = BinOpNode(expr, op_tok.value, right)
        return expr

    def parse_term(self) -> ASTNode:
        expr = self.parse_factor()
        while self.current().type in ("PLUS", "MINUS"):
            op_tok = self.current()
            self.pos += 1
            right = self.parse_factor()
            expr = BinOpNode(expr, op_tok.value, right)
        return expr

    def parse_factor(self) -> ASTNode:
        expr = self.parse_primary()
        while self.current().type in ("TIMES", "DIVIDE"):
            op_tok = self.current()
            self.pos += 1
            right = self.parse_primary()
            expr = BinOpNode(expr, op_tok.value, right)
        return expr

    def parse_primary(self) -> ASTNode:
        tok = self.current()
        if tok.type == "NUMBER":
            self.consume("NUMBER")
            expr: ASTNode = NumberNode(int(tok.value))
        elif tok.type == "ID":
            self.consume("ID")
            expr = IdentifierNode(tok.value)
        elif tok.type == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
        elif tok.type == "LBRACKET":
            self.consume("LBRACKET")
            elements: List[ASTNode] = []
            if self.current().type != "RBRACKET":
                elements.append(self.parse_expression())
                while self.current().type == "COMMA":
                    self.consume("COMMA")
                    elements.append(self.parse_expression())
            self.consume("RBRACKET")
            expr = ListNode(elements)
        else:
            raise VertexSyntaxError(f"Unexpected token: {tok.value}")

        while self.current().type == "LBRACKET":
            self.consume("LBRACKET")
            index_expr = self.parse_expression()
            self.consume("RBRACKET")
            expr = IndexNode(expr, index_expr)

        return expr