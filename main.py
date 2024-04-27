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
    source_one = """
    (+ (- 3 5) (* 5 -7) (/ 20 10))
    (print (+ (* 3 5) (/ 5 -7.7) (- 6 9)))
    ((lambda (x y) (- x y)) 5 6)
    (( lambda (w x y z) (+ w (- y z) (* z (+ 5 10 (- 5 10 (/ 5 10))) x z) ) ) 5 (- 10 20) 15 20)
    """
    source_two = "(print ( print (+ 3 5)))"
    source_three = """
    (def variable (- 20 10))
    (def new-variable (+ 10 30))
    (print (- variable (+ new-variable 30)))
    (def square (lambda (x) (* x x)))
    """
    long_lambda = "(print(( lambda (w x y z) (+ w (- y z) (* z (+ 5 10 (- 5 10 (/ 5 10))) x z) ) ) 5 (- 10 20) 15 20))"
    test = '(if (> x 0) (print "Positive") (print "Negative"))'
    ex = "(print (lambda (x y z) (- 3 x y z 5)) (+ 10 (- 5 6)) (+ 10 15))"
    string_thing = """
    (print (>= 3 1 1.7 0.8 9))
    (print (+ 5 8 (- 6 7)))
    (define hello (lambda () (print "Hello!")))
    (hello)
    (define outer-var 50)
    (print 
        ( lambda (x) (
            (define thing 50) 
            (+ thing x) ) ) )
    """
    """
    (defun fib (n)
      ; Return the nth Fibonacci number
      (if (< n 2)
          n
          (+ (fib (- n 1))
             (fib (- n 2)))))
    """
    lexer = Lexer("""
    (defun square (x) (* x x))
    (print (square 5))
    (defun fib (n)
      ; Return the nth Fibonacci number
      (if (< n 2)
          n
          (+ (fib (- n 1))
             (fib (- n 2)))))
    (print fib)
    ; (print (fib 2))
    ; (if (> 5 10) (print "true") (print "false"))
    ; (print (fib 5))
    """)
    lexer.lex()
    # lexer.print()
    parser = Parser(lexer.tokens)
    lists = parser.parse()
    evaluator = Eval(lists, {})
    for i, list_ in enumerate(lists):
        if list_:
            evaluator.evaluate(lists[i])

    print("global env", evaluator.env)
