from tokenizer import Lexer
from parser import Parser
from eval import Eval
from sys import argv


def load_source_file(file_path: str = 'test.pylisp'):
    with open(file_path) as f:
        return f.read()


def repl():
    pass


if __name__ == '__main__':
    if len(argv) == 1:
        repl()
    else:
        lexer = Lexer(load_source_file())
        lexer.lex()
        parser = Parser(lexer.tokens)
        lists = parser.parse()
        evaluator = Eval(lists, {})
        for lisp_list in lists:
            evaluator.evaluate(lisp_list)
