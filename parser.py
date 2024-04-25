from Token import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token] = None):
        self.tokens = tokens
        self.pos = 0

    def is_eof(self):
        return self.pos >= len(self.tokens)

    def peek(self, n: int = 0):
        return self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos + 1 >= len(self.tokens):
            return Token(TokenType.EOF, self.pos, "")
        return self.tokens[self.pos]

    def atom(self):
        return self.peek().literal

    def parse_list(self):
        lisp_list = []
        while self.advance().type not in (TokenType.RPAREN, TokenType.EOF):
            lisp_list.append(self.parse_expression())
        return lisp_list

    def parse_expression(self):
        return self.parse_list() if self.peek().type == TokenType.LPAREN else self.atom()

    def parse(self):
        lists = []
        while not self.is_eof():
            lists.append(self.parse_expression())
            self.advance()
        return lists
