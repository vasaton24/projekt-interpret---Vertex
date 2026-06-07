"""Parser modul s definicí AST uzlů pro syntaktickou analýzu."""

from typing import List, Union
from .exceptions import VertexSyntaxError
from .lexer import Token

class ASTNode:
    """Základní třída pro uzly abstraktního syntaktického stromu."""
    pass

class NumberNode(ASTNode):
    """Reprezentuje celočíselnou literál v AST."""

    def __init__(self, value: int) -> None:
        self.value: int = value

class StringNode(ASTNode):
    """Reprezentuje řetězcový literál v AST."""

    def __init__(self, value: str) -> None:
        self.value: str = value

class IdentifierNode(ASTNode):
    """Reprezentuje pojmenovaný odkaz na proměnnou v AST."""

    def __init__(self, name: str) -> None:
        self.name: str = name

class ListNode(ASTNode):
    """Reprezentuje literál seznamu v AST."""

    def __init__(self, elements: List[ASTNode]) -> None:
        self.elements: List[ASTNode] = elements

class IndexNode(ASTNode):
    """Reprezentuje indexování seznamu v AST."""

    def __init__(self, left: ASTNode, index: ASTNode) -> None:
        self.left: ASTNode = left
        self.index: ASTNode = index

class BinOpNode(ASTNode):
    """Reprezentuje binární operaci mezi dvěma výrazy."""

    def __init__(self, left: ASTNode, op: str, right: ASTNode) -> None:
        self.left: ASTNode = left
        self.op: str = op
        self.right: ASTNode = right

class UnaryOpNode(ASTNode):
    """Reprezentuje unární operaci nad jedním výrazem."""

    def __init__(self, op: str, operand: ASTNode) -> None:
        self.op: str = op
        self.operand: ASTNode = operand

class AssignNode(ASTNode):
    """Reprezentuje přiřazení proměnné."""

    def __init__(self, name: str, value: ASTNode) -> None:
        self.name: str = name
        self.value: ASTNode = value

class ListAssignNode(ASTNode):
    """Reprezentuje přiřazení prvku seznamu."""

    def __init__(self, left: IndexNode, value: ASTNode) -> None:
        self.left: IndexNode = left
        self.value: ASTNode = value

class PrintNode(ASTNode):
    """Reprezentuje tiskový příkaz v AST."""

    def __init__(self, expression: ASTNode) -> None:
        self.expression: ASTNode = expression

class IfNode(ASTNode):
    """Reprezentuje podmíněný příkaz s volitelnou větví else."""

    def __init__(self, condition: ASTNode, then_branch: ASTNode, else_branch: Union[ASTNode, None]) -> None:
        self.condition: ASTNode = condition
        self.then_branch: ASTNode = then_branch
        self.else_branch: Union[ASTNode, None] = else_branch

class WhileNode(ASTNode):
    """Reprezentuje while smyčku."""

    def __init__(self, condition: ASTNode, body: ASTNode) -> None:
        self.condition: ASTNode = condition
        self.body: ASTNode = body

class ForNode(ASTNode):
    """Reprezentuje for smyčku s inicializací, podmínkou a aktualizací."""

    def __init__(self, init: Union[ASTNode, None], condition: Union[ASTNode, None], update: Union[ASTNode, None], body: ASTNode) -> None:
        self.init: Union[ASTNode, None] = init
        self.condition: Union[ASTNode, None] = condition
        self.update: Union[ASTNode, None] = update
        self.body: ASTNode = body

class BlockNode(ASTNode):
    """Reprezentuje blok příkazů."""

    def __init__(self, statements: List[ASTNode]) -> None:
        self.statements: List[ASTNode] = statements

class Parser:
    """Parsuje seznam tokenů do abstraktního syntaktického stromu (AST)."""

    def __init__(self, tokens: List[Token]) -> None:
        """Inicializuje parser se seznamem tokenů."""
        self.tokens: List[Token] = tokens
        self.pos: int = 0

    def current(self) -> Token:
        """Vrací právě analyzovaný token."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        if self.tokens:
            last = self.tokens[-1]
            return Token("EOF", "", last.line, last.column)
        return Token("EOF", "", 1, 1)

    def consume(self, expected_type: str) -> Token:
        """Spotřebuje aktuální token pokud odpovídá očekávanému typu, jinak vyhodí chybu."""
        tok: Token = self.current()
        if tok.type != expected_type:
            raise VertexSyntaxError(f"Expected {expected_type}, got {tok.type}", tok.line, tok.column)
        self.pos += 1
        return tok

    def parse(self) -> BlockNode:
        """Parsuje kompletní posloupnost tokenů do kořenového BlockNode."""
        statements: List[ASTNode] = []
        while self.current().type != "EOF":
            statements.append(self.parse_statement())
        return BlockNode(statements)

    def parse_statement(self) -> ASTNode:
        """Parse a single statement or control structure."""
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
        """Parse a block of statements enclosed in braces, or a single statement."""
        if self.current().type == "LBRACE":
            self.consume("LBRACE")
            statements: List[ASTNode] = []
            while self.current().type not in ("RBRACE", "EOF"):
                statements.append(self.parse_statement())
            self.consume("RBRACE")
            return BlockNode(statements)
        return self.parse_statement()

    def parse_expression(self) -> ASTNode:
        """Parse an assignment or lower-precedence expression."""
        return self.parse_assignment()

    def parse_assignment(self) -> ASTNode:
        """Parse variable or list assignment."""
        expr = self.parse_logical_or()
        if self.current().type == "ASSIGN":
            self.consume("ASSIGN")
            value = self.parse_assignment()
            if isinstance(expr, IdentifierNode):
                return AssignNode(expr.name, value)
            elif isinstance(expr, IndexNode):
                return ListAssignNode(expr, value)
            raise VertexSyntaxError("Invalid assignment target", self.current().line, self.current().column)
        return expr

    def parse_logical_or(self) -> ASTNode:
        expr = self.parse_logical_and()
        while self.current().type == "OR":
            op_tok = self.current()
            self.consume("OR")
            right = self.parse_logical_and()
            expr = BinOpNode(expr, op_tok.value, right)
        return expr

    def parse_logical_and(self) -> ASTNode:
        expr = self.parse_comparison()
        while self.current().type == "AND":
            op_tok = self.current()
            self.consume("AND")
            right = self.parse_comparison()
            expr = BinOpNode(expr, op_tok.value, right)
        return expr

    def parse_comparison(self) -> ASTNode:
        """Parse equality and relational comparisons."""
        expr = self.parse_term()
        while self.current().type in ("EQ", "NE", "LT", "GT", "LE", "GE"):
            op_tok = self.current()
            self.pos += 1
            right = self.parse_term()
            expr = BinOpNode(expr, op_tok.value, right)
        return expr

    def parse_term(self) -> ASTNode:
        """Parse addition and subtraction operations."""
        expr = self.parse_factor()
        while self.current().type in ("PLUS", "MINUS"):
            op_tok = self.current()
            self.pos += 1
            right = self.parse_factor()
            expr = BinOpNode(expr, op_tok.value, right)
        return expr

    def parse_factor(self) -> ASTNode:
        """Parse multiplication and division operations."""
        expr = self.parse_unary()
        while self.current().type in ("TIMES", "DIVIDE"):
            op_tok = self.current()
            self.pos += 1
            right = self.parse_unary()
            expr = BinOpNode(expr, op_tok.value, right)
        return expr

    def parse_unary(self) -> ASTNode:
        """Parse unary plus, minus, and logical not expressions."""
        if self.current().type in ("PLUS", "MINUS", "NOT"):
            op_tok = self.current()
            self.pos += 1
            operand = self.parse_unary()
            return UnaryOpNode(op_tok.value, operand)
        return self.parse_primary()

    def parse_primary(self) -> ASTNode:
        """Parse primary elements like numbers, identifiers, and parenthesis."""
        tok = self.current()
        if tok.type == "NUMBER":
            self.consume("NUMBER")
            expr: ASTNode = NumberNode(int(tok.value))
        elif tok.type == "ID":
            self.consume("ID")
            expr = IdentifierNode(tok.value)
        elif tok.type == "STRING":
            self.consume("STRING")
            expr = StringNode(tok.value)
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
            raise VertexSyntaxError(f"Unexpected token: {tok.value}", tok.line, tok.column)

        while self.current().type == "LBRACKET":
            self.consume("LBRACKET")
            index_expr = self.parse_expression()
            self.consume("RBRACKET")
            expr = IndexNode(expr, index_expr)

        return expr