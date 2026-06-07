"""Modul interpretace zodpovědný za vykonání zpracovaného AST."""

from typing import Dict, Any, List
from .exceptions import VertexRuntimeError
from .lexer import Token
from .parser import (
    Parser, ASTNode, NumberNode, StringNode, IdentifierNode, ListNode, IndexNode, BinOpNode,
    UnaryOpNode, AssignNode, ListAssignNode, PrintNode, IfNode, WhileNode, ForNode, BlockNode
)

class Environment:
    """Ukládá proměnné a jejich stav během běhu programu."""

    def __init__(self) -> None:
        """Inicializuje prázdné prostředí."""
        self.variables: Dict[str, Any] = {}

    def set(self, name: str, value: Any) -> None:
        """Nastaví hodnotu proměnné v prostředí."""
        self.variables[name] = value

    def get(self, name: str) -> Any:
        """Vrátí hodnotu proměnné z prostředí.

        Vyvolá:
            VertexRuntimeError: pokud proměnná není definovaná.
        """
        if name in self.variables:
            return self.variables[name]
        raise VertexRuntimeError(f"Nedefinovaná proměnná '{name}'")

class Interpreter:
    """Vykonává AST vytvořené parserem."""

    def __init__(self, env: Environment, output_widget: Any) -> None:
        """Inicializuje interpret s prostředím a výstupním widgetem."""
        self.env: Environment = env
        self.output_widget: Any = output_widget

    def execute(self, tokens: List[Token]) -> None:
        """Parsuje tokeny a vyhodnotí vzniklé AST.

        Args:
            tokens (List[Token]): Lexikální tokeny k vykonání.
        """
        parser = Parser(tokens)
        ast = parser.parse()
        self.evaluate(ast)

    def evaluate(self, node: ASTNode) -> Any:
        """Rekurzivně vyhodnotí uzel AST a vrátí jeho hodnotu.

        Args:
            node (ASTNode): Uzel, který se má vyhodnotit.

        Vrací:
            Any: Výsledek vyhodnocení podle typu uzlu.
        """
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode):
            return node.value
        elif isinstance(node, UnaryOpNode):
            operand = self.evaluate(node.operand)
            if node.op == "+":
                return +operand
            if node.op == "-":
                if not isinstance(operand, int):
                    raise VertexRuntimeError("Arithmetický operand musí být celé číslo")
                return -operand
            if node.op == "not":
                return 1 if not operand else 0
            raise VertexRuntimeError(f"Neznámý unární operátor: {node.op}")
        elif isinstance(node, IdentifierNode):
            return self.env.get(node.name)
        elif isinstance(node, ListNode):
            return [self.evaluate(el) for el in node.elements]
        elif isinstance(node, IndexNode):
            lst = self.evaluate(node.left)
            idx = self.evaluate(node.index)
            if not isinstance(lst, list) or not isinstance(idx, int):
                raise VertexRuntimeError("Neplatný přístup k indexu")
            try:
                return lst[idx]
            except IndexError:
                raise VertexRuntimeError("Index mimo rozsah")
        elif isinstance(node, BinOpNode):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            op = node.op
            if op == "+":
                if isinstance(left_val, str) and isinstance(right_val, str):
                    return left_val + right_val
                if isinstance(left_val, int) and isinstance(right_val, int):
                    return left_val + right_val
                if isinstance(left_val, list) and isinstance(right_val, list):
                    return left_val + right_val
                raise VertexRuntimeError("Neplatné operandy pro +")
            if op == "and":
                return 1 if left_val and right_val else 0
            if op == "or":
                return 1 if left_val or right_val else 0
            if op in ("-", "*", "/"):
                if not isinstance(left_val, int) or not isinstance(right_val, int):
                    raise VertexRuntimeError("Arithmetický operand musí být celé číslo")
                if op == "-":
                    return left_val - right_val
                if op == "*":
                    return left_val * right_val
                if op == "/":
                    if right_val == 0:
                        raise VertexRuntimeError("Dělení nulou!")
                    return left_val // right_val
            elif op == "==":
                return 1 if left_val == right_val else 0
            elif op == "!=":
                return 1 if left_val != right_val else 0
            elif op == "<":
                return 1 if left_val < right_val else 0
            elif op == ">":
                return 1 if left_val > right_val else 0
            elif op == "<=":
                return 1 if left_val <= right_val else 0
            elif op == ">=":
                return 1 if left_val >= right_val else 0
        elif isinstance(node, AssignNode):
            val = self.evaluate(node.value)
            self.env.set(node.name, val)
            return val
        elif isinstance(node, ListAssignNode):
            lst = self.evaluate(node.left.left)
            idx = self.evaluate(node.left.index)
            val = self.evaluate(node.value)
            if not isinstance(lst, list) or not isinstance(idx, int):
                raise VertexRuntimeError("Neplatné přiřazení do indexu")
            try:
                lst[idx] = val
            except IndexError:
                raise VertexRuntimeError("Index mimo rozsah")
            return val
        elif isinstance(node, PrintNode):
            val = self.evaluate(node.expression)
            self.output_widget.insert("end", f"> {val}\n")
            try:
                self.output_widget.see("end")
            except Exception:
                pass
            return None
        elif isinstance(node, IfNode):
            cond = self.evaluate(node.condition)
            if cond:
                self.evaluate(node.then_branch)
            elif node.else_branch:
                self.evaluate(node.else_branch)
            return None
        elif isinstance(node, WhileNode):
            while self.evaluate(node.condition):
                self.evaluate(node.body)
            return None
        elif isinstance(node, ForNode):
            if node.init:
                self.evaluate(node.init)
            while node.condition is None or self.evaluate(node.condition):
                self.evaluate(node.body)
                if node.update:
                    self.evaluate(node.update)
            return None
        elif isinstance(node, BlockNode):
            for stmt in node.statements:
                self.evaluate(stmt)
            return None
        raise VertexRuntimeError("Neznámý typ AST uzlu")