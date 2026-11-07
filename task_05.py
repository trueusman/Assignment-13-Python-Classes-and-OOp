"""Task 05: Safe arithmetic expression parser. No eval() or exec()."""

class ExpressionError(ValueError):
    pass

class Parser:
    def __init__(self, expression):
        self.tokens = self._tokenize(expression)
        self.position = 0

    @staticmethod
    def _tokenize(expression):
        tokens = []
        i = 0
        while i < len(expression):
            ch = expression[i]
            if ch.isspace():
                i += 1
            elif ch.isdigit():
                j = i
                while j < len(expression) and expression[j].isdigit():
                    j += 1
                tokens.append(int(expression[i:j]))
                i = j
            elif ch in "+-*/()":
                tokens.append(ch)
                i += 1
            else:
                raise ExpressionError(f"Invalid character: {ch!r}")
        return tokens

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def take(self):
        token = self.peek()
        if token is not None:
            self.position += 1
        return token

    def parse(self):
        if not self.tokens:
            raise ExpressionError("Expression is empty")
        value = self.expression()
        if self.peek() is not None:
            raise ExpressionError(f"Unexpected token: {self.peek()!r}")
        return float(value)

    def expression(self):
        value = self.term()
        while self.peek() in ("+", "-"):
            op = self.take()
            right = self.term()
            value = value + right if op == "+" else value - right
        return value

    def term(self):
        value = self.factor()
        while self.peek() in ("*", "/"):
            op = self.take()
            right = self.factor()
            if op == "/" and right == 0:
                raise ZeroDivisionError("Division by zero")
            value = value * right if op == "*" else value / right
        return value

    def factor(self):
        token = self.peek()
        if token == "+":
            self.take()
            return +self.factor()
        if token == "-":
            self.take()
            return -self.factor()
        if token == "(":
            self.take()
            value = self.expression()
            if self.take() != ")":
                raise ExpressionError("Missing closing parenthesis")
            return value
        if isinstance(token, int):
            return self.take()
        raise ExpressionError(f"Expected a number or '(', got {token!r}")


def calculate(expression):
    return Parser(expression).parse()


if __name__ == "__main__":
    print(calculate("-(3 + 2) * 4 + 18 / 3"))  # -14.0
