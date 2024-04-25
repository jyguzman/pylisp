from Token import TokenType, Token
from typing import Union


class Lexer:
    def __init__(self, source: str = None):
        self.source = source
        self.pos = 0
        self.tokens = []
        self.specialForms = {
            'if': (TokenType.IF, 'if'),
            'define': (TokenType.DEFINE, 'define'),
            'lambda': (TokenType.LAMBDA, 'lambda'),
            'defun': (TokenType.DEFUN, 'defun'),
            'list': (TokenType.LIST, 'list')
        }

    def is_eof(self) -> bool:
        return self.pos >= len(self.source)

    def advance(self) -> str:
        self.pos += 1
        if self.pos >= len(self.source):
            return '\0'
        return self.source[self.pos]

    def peek(self, n: int = 0) -> str:
        if self.pos + n >= len(self.source):
            return '\0'
        return self.source[self.pos + n]

    def lex_string(self) -> Token:
        start_pos = self.pos
        string = []
        self.advance()

        while self.peek() != '"':
            string.append(self.peek())
            self.advance()

        self.advance()
        return Token(TokenType.STRING, start_pos, ''.join(string))

    def lex_num(self) -> Token:
        start_pos = self.pos
        numStr = []
        isNegative, isFloat = False, False
        if self.peek() == '-':
            isNegative = True
            self.advance()

        while self.peek().isdigit() or self.peek() == '.':
            if self.peek() == '.':
                isFloat = True
            numStr.append(self.peek())
            self.advance()

        numStr = ''.join(numStr)
        token_type = TokenType.FLOAT if isFloat else TokenType.INTEGER
        literal = float(numStr) if isFloat else int(numStr)
        if isNegative:
            literal = -literal
        return Token(token_type, start_pos, literal)

    def lex_ident(self) -> Token:
        start_pos = self.pos
        ident = []

        while self.peek().isalpha() or self.peek() == '-':
            ident.append(self.peek())
            self.advance()

        ident = ''.join(ident)
        if ident not in self.specialForms:
            return Token(TokenType.STRING, start_pos, ident)
        token_type, literal = self.specialForms[ident]
        return Token(token_type, start_pos, literal)

    def match(self) -> Token:
        c = self.peek()
        while c in (' ', '\n', '\r'):
            c = self.advance()
        token = None
        if c == '(':
            token = Token(TokenType.LPAREN, self.pos, c)
        elif c == ')':
            token = Token(TokenType.RPAREN, self.pos, c)
        elif c == ';':
            token = Token(TokenType.SEMI, self.pos, c)
        elif c == '=':
            token = Token(TokenType.EQUALS, self.pos, c)
        elif c == '<':
            if self.peek(1) == '=':
                token = Token(TokenType.GEQ, self.pos, '<=')
                self.advance()
            else:
                token = Token(TokenType.GREATER, self.pos, c)
        elif c == '>':
            if self.peek(1) == '=':
                token = Token(TokenType.LEQ, self.pos, '>=')
                self.advance()
            else:
                token = Token(TokenType.LESS, self.pos, c)
        elif c == '+':
            token = Token(TokenType.PLUS, self.pos, c)
        elif c == '*':
            token = Token(TokenType.MULTIPLY, self.pos, c)
        elif c == '-':
            if self.peek(1).isdigit():
                return self.lex_num()
            token = Token(TokenType.MINUS, self.pos, c)
        elif c == '/':
            token = Token(TokenType.DIVIDE, self.pos, c)
        elif c.isalpha():
            return self.lex_ident()
        elif c == '"':
            return self.lex_string()
        elif c.isdigit():
            return self.lex_num()
        else:
            token = Token(TokenType.EOF, self.pos, "")
        self.advance()
        return token

    def addToken(self, token: Token):
        self.tokens.append(token)

    def print(self):
        print('\n'.join([str(t) for t in self.tokens]))


    def lex(self, source: str = None):
        while not self.is_eof():
            token = self.match()
            self.addToken(token)
        return self.tokens
