from tokenizer import Lexer
from parser import Parser
from eval import Eval


def load_source_file(file_path: str):
    source = ""
    with open(file_path) as f:
        source = f.read()
    return source


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lexer = Lexer("""
    ;(defun square (x) (* x x))
    ;(print (square 10))
    (defun fib-helper (n a b) 
        (if (= n 0) 
            a 
            (if (= n 1) 
                b 
                (fib-helper (- n 1) b (+ a b)))))
    (defun fib (n) (fib-helper n 0 1))
    (print (fib 100))
    """)
    lexer.lex()
    parser = Parser(lexer.tokens)
    lists = parser.parse()
    evaluator = Eval(lists, {})
    for i, list_ in enumerate(lists):
        if list_:
            evaluator.evaluate(lists[i])
    print("global env", evaluator.env)
