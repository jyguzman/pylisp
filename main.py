from tokenizer import Lexer
from parser import Parser
from eval import Eval


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    source_one = """
    (+ (- 3 5) (* 5 -7) (/ 20 10))
    (print (+ (* 3 5) (/ 5 -7.7) (- 6 9)))
    ((lambda (x y) (- x y)) 5 6)
    (( lambda (w x y z) (+ w (- y z) (* z (+ 5 10 (- 5 10 (/ 5 10))) x z) ) ) 5 (- 10 20) 15 20)
    """
    source_two = "(print ((lambda (x y) (+ (* x x) (* y y) (* 2 x y))) 3 4))"
    source_three = """
    (print (+ 3 5))
    """
    lexer = Lexer(source_two)
    lexer.lex()
    lexer.print()
    parser = Parser(lexer.tokens)
    lists = parser.parse()
    # for i, list_ in enumerate(lists):
    #     print(list_, i)
    evaluator = Eval(lists)
    # print(lists[2])
    print(lists[0])
    evaluator.evaluate(lists[0])
    # print(evaluator.evaluate(lists[0]))
