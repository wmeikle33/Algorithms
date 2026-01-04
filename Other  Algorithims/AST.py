from dataclasses import dataclass
from typing import List, Optional, Union

# ---------- AST node definitions ----------
@dataclass
class Num:
    value: int

@dataclass
class Unary:
    op: str          # '-'
    expr: "Node"

@dataclass
class Bin:
    left: "Node"
    op: str          # '+', '-', '*', '/'
    right: "Node"

Node = Union[Num, Unary, Bin]


# ---------- Tokenizer ----------
def tokenize(s: str) -> List[str]:
    tokens = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            j = i
            while j < n and s[j].isdigit():
                j += 1
            tokens.append(s[i:j])
            i = j
        elif c in "+-*/()":
            tokens.append(c)
            i += 1
        else:
            raise ValueError(f"Unexpected char: {c}")
    return tokens


# ---------- Recursive descent parser ----------
# Grammar:
# expr   := term (('+'|'-') term)*
# term   := factor (('*'|'/') factor)*
# factor := '-' factor | number | '(' expr ')'

class Parser:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.i = 0

    def peek(self) -> Optional[str]:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self) -> str:
        t = self.tokens[self.i]
        self.i += 1
        return t

    def parse(self) -> Node:
        node = self.parse_expr()
        if self.peek() is not None:
            raise ValueError("Extra tokens at end")
        return node

    def parse_expr(self) -> Node:
        node = self.parse_term()
        while self.peek() in ("+", "-"):
            op = self.take()
            rhs = self.parse_term()
            node = Bin(node, op, rhs)
        return node

    def parse_term(self) -> Node:
        node = self.parse_factor()
        while self.peek() in ("*", "/"):
            op = self.take()
            rhs = self.parse_factor()
            node = Bin(node, op, rhs)
        return node

    def parse_factor(self) -> Node:
        t = self.peek()
        if t == "-":  # unary minus
            self.take()
            return Unary("-", self.parse_factor())

        if t == "(":
            self.take()  # '('
            node = self.parse_expr()
            if self.peek() != ")":
                raise ValueError("Expected ')'")
            self.take()  # ')'
            return node

        if t is None:
            raise ValueError("Unexpected end of input")

        # number
        if t.isdigit():
            return Num(int(self.take()))

        raise ValueError(f"Unexpected token: {t}")


# ---------- AST evaluator ----------
def eval_ast(node: Node) -> int:
    if isinstance(node, Num):
        return node.value
    if isinstance(node, Unary):
        v = eval_ast(node.expr)
        if node.op == "-":
            return -v
        raise ValueError(f"Unknown unary op {node.op}")
    if isinstance(node, Bin):
        a = eval_ast(node.left)
        b = eval_ast(node.right)
        if node.op == "+":
            return a + b
        if node.op == "-":
            return a - b
        if node.op == "*":
            return a * b
        if node.op == "/":
            # match typical "trunc toward 0" behavior
            return int(a / b)
        raise ValueError(f"Unknown binary op {node.op}")
    raise TypeError("Unknown node type")
