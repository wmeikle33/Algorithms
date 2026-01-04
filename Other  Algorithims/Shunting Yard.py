from typing import List

def tokenize(expr: str) -> List[str]:
    tokens = []
    i, n = 0, len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
        elif c.isdigit():
            j = i
            while j < n and expr[j].isdigit():
                j += 1
            tokens.append(expr[i:j])
            i = j
        elif c in "+-*/()":
            tokens.append(c)
            i += 1
        else:
            raise ValueError(f"Unexpected character: {c}")
    return tokens


def to_rpn(tokens: List[str]) -> List[str]:
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    output = []
    ops = []

    for t in tokens:
        if t.isdigit():
            output.append(t)
        elif t in prec:
            # pop while top has higher or equal precedence
            while ops and ops[-1] in prec and prec[ops[-1]] >= prec[t]:
                output.append(ops.pop())
            ops.append(t)
        elif t == "(":
            ops.append(t)
        elif t == ")":
            while ops and ops[-1] != "(":
                output.append(ops.pop())
            if not ops or ops[-1] != "(":
                raise ValueError("Mismatched parentheses")
            ops.pop()  # discard "("
        else:
            raise ValueError(f"Bad token: {t}")

    while ops:
        if ops[-1] in ("(", ")"):
            raise ValueError("Mismatched parentheses")
        output.append(ops.pop())

    return output


def eval_rpn(rpn: List[str]) -> int:
    st = []
    for t in rpn:
        if t.isdigit():
            st.append(int(t))
        else:
            b = st.pop()
            a = st.pop()
            if t == "+":
                st.append(a + b)
            elif t == "-":
                st.append(a - b)
            elif t == "*":
                st.append(a * b)
            elif t == "/":
                st.append(int(a / b))  # trunc toward 0
            else:
                raise ValueError(f"Unknown op: {t}")
    if len(st) != 1:
        raise ValueError("Invalid RPN expression")
    return st[0]
