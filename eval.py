from dataclasses import  dataclass

MATH_OPS = {'+', '-', '*', '/'}
COMPARISON_OPS = {'=', '>', '>=', '<', '<='}
SPECIAL = {'lambda', 'def', 'if'}

@dataclass
class Lambda:
    params: list[str]
    body: list


def check_is_number(val):
    if not isinstance(val, (float, int)):
        print(f"{val} is not a number.")
        exit(1)


def car(lisp_list: list):
    return lisp_list[0]


def cons(lisp_list: list):
    return lisp_list[1:]


class Eval:
    def __init__(self, lists: list = None):
        self.lists = lists

    def evaluateList(self, lisp_list):
        return self.evaluate(lisp_list[0])

    def evaluate(self, lisp_val):
        if lisp_val is None or isinstance(lisp_val, (int, float, bool, str)):
            return lisp_val
        if isinstance(lisp_val, list):
            first_val = car(lisp_val)
            if not isinstance(first_val, list):
                if first_val in MATH_OPS:
                    return self.math_op(first_val, cons(lisp_val))
                if first_val in COMPARISON_OPS:
                    return self.comparison(first_val, cons(lisp_val))
                if first_val == 'print':
                    print(self.evaluate(lisp_val[1]))
                    return None
            else:
                first_val_inner = car(first_val)
                if first_val_inner == 'lambda':
                    fn = self.make_lambda(first_val[1], first_val[2])
                    return self.eval_lambda(fn, cons(lisp_val))

        return lisp_val

    def make_lambda(self, params: list[str], body: list) -> Lambda:
        return Lambda(params, body)

    def bind_lambda_vars(self, fn_scope: dict, fn_body: list):
        for i, elem in enumerate(fn_body):
            if isinstance(elem, list):
                self.bind_lambda_vars(fn_scope, elem)
            else:
                if fn_body[i] in fn_scope:
                    fn_body[i] = fn_scope[fn_body[i]]

    def eval_lambda(self, fn: Lambda, args: list):
        # print("lambda:", fn, "\nargs:", args)
        params, body = fn.params, fn.body
        scope = {}
        for i in range(len(params)):
            scope[params[i]] = self.evaluate(args[i])

        # print(scope)
        self.bind_lambda_vars(scope, body)
        # print("body", body)
        #
        # print("body", body)
        # print("evaled", self.evaluate(body))
        return self.evaluate(body)

    def math_op(self, op: str, lisp_list: list):
        match op:
            case '+':
                return self.plus(lisp_list)
            case '-':
                return self.minus(lisp_list)
            case '*':
                return self.multiply(lisp_list)
            case '/':
                return self.divide(lisp_list)

    def comparison(self, op: str, lisp_list: list):
        return None

    def plus(self, lisp_list):
        acc = 0
        for elem in lisp_list:
            val = self.evaluate(elem)
            check_is_number(val)
            acc += val
        return acc

    def multiply(self, lisp_list):
        acc = lisp_list[0]
        for elem in lisp_list[1:]:
            val = self.evaluate(elem)
            check_is_number(val)
            acc *= val
        return acc

    def minus(self, lisp_list):
        acc = lisp_list[0]
        for elem in lisp_list[1:]:
            val = self.evaluate(elem)
            check_is_number(val)
            acc -= val
        return acc

    def divide(self, lisp_list):
        acc = lisp_list[0]
        for elem in lisp_list[1:]:
            val = self.evaluate(elem)
            check_is_number(val)
            acc /= val
        return acc

    def print(self, args: list):
        print("args in print", args)
        val = self.evaluate(args)
        print("val in print", val)
        print(self.evaluate(args))


