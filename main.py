from tokenizer import Lexer
from parser import Parser

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lexer = Lexer("""
    (+ (+ 3 5) (/ 5 -7.7) (- 6 9))
    (print (+ (* 3 5) (/ 5 -7.7) (- 6 9)))
    (print (lambda (x y) (- x y)) 5 6)
    """)
    lexer.lex()
    lexer.print()
    parser = Parser(lexer.tokens)
    lists = parser.parse()
    parser.print(lists)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
