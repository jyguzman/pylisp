(def square (lambda (x) (* x x)))
(def just-a-random-function (lambda (x) (+ 5 x)))
(print (square 5))
(print (just-a-random-function 5))
(print (square (just-a-random-function 10)))
(def compose
    (lambda (x)
        (square
            (just-a-random-function x))) )
(print compose)
(def print-hello (lambda () (print "Hello!")))
(print-hello)
