from dataclasses import dataclass
import functools
from copy import deepcopy

MATH_OPS = {'+', '-', '*', '/'}
COMPARISON_OPS = {'=', '>', '>=', '<', '<='}
BINARY_OPS = MATH_OPS.union(COMPARISON_OPS)
SPECIAL = {'lambda', 'define', 'if', 'list', 'defun'}
BUILT_INS = {'read', 'format', 'print'}
FUNCTIONS = BINARY_OPS.union(SPECIAL, BUILT_INS)


@dataclass
class Function:
    params: list[str]
    body: list
    name: str = None
    env: dict = None


def check_is_number(val):
    if not isinstance(val, (float, int)):
        print(f"{val} is not a number.")
        exit(1)


def car(lisp_list: list):
    return lisp_list[0]


def cons(lisp_list: list):
    return lisp_list[1:]


def math_binary(op: str, a, b):
    if not isinstance(a, (int, float)):
        print(f'{a} is not a number.')
        exit(1)
    if not isinstance(b, (int, float)):
        print(f'{b} is not a number.')
        exit(1)

    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else:
        return a / b


class Eval:
    def __init__(self, lists: list = None, env: dict = None):
        self.lists = lists
        self.env = env

    def evaluate(self, lisp_value):
        if not isinstance(lisp_value, list):
            if isinstance(lisp_value, (str, Function)) and lisp_value in self.env:
                return self.env[lisp_value]
            return lisp_value
        if isinstance(lisp_value[0], list):
            lisp_value[0] = self.evaluate(lisp_value[0])
        first_val = self.evaluate(lisp_value[0])
        if not isinstance(first_val, Function) and first_val not in FUNCTIONS:
            print("First element must be a function, operator, or special form.")
            exit(1)
        if isinstance(first_val, Function):
            return self.eval_fn(first_val, lisp_value[1:])
        if first_val == 'lambda':
            fn = Function(lisp_value[1], lisp_value[2])
            if len(lisp_value) < 4:
                return fn
            return self.eval_fn(fn, lisp_value[3:])
        if first_val == 'defun':
            name, args, body = lisp_value[1], lisp_value[2], lisp_value[3]
            fn = Function(args, body, name=name)
            self.env[name] = fn
            return fn
        if first_val == 'if':
            return self.eval_if(lisp_value[1:])
        if first_val == 'print':
            return self.print(lisp_value[1])
        if first_val == 'define':
            return self.define(lisp_value[1:])
        if first_val in BINARY_OPS:
            return self.binary(first_val, cons(lisp_value))
        print(f"Operator or function {first_val} not available.")
        exit(1)

    def bind_function_vars(self, fn_scope: dict, fn_body: list):
        for i, elem in enumerate(fn_body):
            if isinstance(elem, list):
                self.bind_function_vars(fn_scope, elem)
            else:
                if fn_body[i] in fn_scope:
                    fn_body[i] = fn_scope[fn_body[i]]

    def eval_fn(self, fn: Function, args: list):
        params, body = fn.params, deepcopy(fn.body)
        fn_scope = {params[i]: self.evaluate(args[i]) for i in range(len(params))}
        self.bind_function_vars(fn_scope, body)
        return self.evaluate(body)

    def binary(self, op: str, lisp_list: list):
        if op in MATH_OPS:
            return self.math_op(op, lisp_list)
        if op in COMPARISON_OPS:
            return self.comparison(op, lisp_list)
        print(f"Invalid operator {op}.")
        exit(1)

    def comparison(self, op: str, lisp_list: list):
        new_list = [self.evaluate(item) for item in lisp_list]
        val = new_list[0]
        for other_val in new_list[1:]:
            if (
                    op == '=' and val != other_val or
                    op == '>' and val <= other_val or
                    op == '<' and val >= other_val or
                    op == '>=' and val < other_val or
                    op == '<=' and val > other_val
            ):
                return False
        return True

    def math_op(self, op: str, lisp_list: list):
        new_list = [self.evaluate(item) for item in lisp_list]
        return functools.reduce(lambda a, b: math_binary(op, a, b), new_list)

    def eval_if(self, args: list = None):
        if self.evaluate(args[0]):
            return self.evaluate(self.evaluate(args[1]))
        return self.evaluate(self.evaluate(args[2]))

    def define(self, lisp_list: list):
        ident = self.evaluate(lisp_list[0])
        val = self.evaluate(lisp_list[1])
        self.env[ident] = val
        return val

    def print(self, args: list):
        val = self.evaluate(args)
        print(val)
        return None
