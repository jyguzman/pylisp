from dataclasses import dataclass
from env import Env

MATH_OPS = {'+', '-', '*', '/'}
COMPARISON_OPS = {'=', '>', '>=', '<', '<='}
BINARY_OPS = MATH_OPS.union(COMPARISON_OPS)
SPECIAL = {'lambda', 'def', 'if', 'list', 'defun'}
BUILT_INS = {'read', 'format'}

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


class Eval:
    def __init__(self, lists: list = None, global_env: dict = None):
        self.lists = lists
        self.global_env = global_env

    def evaluate(self, lisp_list, env=None):
        if not isinstance(lisp_list, list):
            return lisp_list
        first_val = lisp_list[0]
        if isinstance(first_val, list):
            first_val = self.evaluate(first_val, env)
            env[first_val] = first_val
        if isinstance(first_val, Function):
            return self.eval_fn(first_val, lisp_list[1:], env)
        if first_val == 'lambda':
            fn = Function(lisp_list[1], lisp_list[2])
            if len(lisp_list) < 4:
                return fn
            return self.eval_fn(fn, lisp_list[3:], env)
        if first_val == 'defun':
            ident, args, body = lisp_list[1], lisp_list[2], lisp_list[3]
            return Function(args, body, env=env, name=ident)
        if first_val == 'if':
            return self.eval_if(lisp_list[1:], env)
        if first_val in BINARY_OPS:
            return self.binary(first_val, cons(lisp_list), env)
        if first_val == 'print':
            return self.print(lisp_list[1], env)
        if first_val == 'define':
            return self.define(lisp_list[1:], env)
        env_val = env.get(first_val, None)
        if env_val and isinstance(env_val, Function):
            return self.eval_fn(env_val, lisp_list[1:], env)
        return lisp_list

    def eval_special_form(self, sf: str, lisp_list: list):
        pass

    def bind_function_vars(self, fn_scope: dict, fn_body: list, env=None):
        for i, elem in enumerate(fn_body):
            if isinstance(elem, list):
                self.bind_function_vars(fn_scope, elem, env)
            else:
                if fn_body[i] in fn_scope:
                    fn_body[i] = fn_scope[fn_body[i]]

    def eval_fn(self, fn: Function, args: list, env=None):
        params, body = fn.params, fn.body[0:]
        fn_scope = {}
        for i in range(len(params)):
            fn_scope[params[i]] = self.evaluate(args[i], env)

        self.bind_function_vars(fn_scope, body, env)
        return self.evaluate(body, env)

    def binary(self, op: str, lisp_list: list, env=None):
        if op in MATH_OPS:
            return self.math_op(op, lisp_list, env)
        if op in COMPARISON_OPS:
            return self.comparison(op, lisp_list, env)
        print(f"Invalid operator {op}")
        exit(1)

    def comparison(self, op: str, lisp_list: list, env: dict = None):
        val = env.get(lisp_list[0], lisp_list[0])
        for elem in lisp_list[1:]:
            other_val = self.evaluate(elem, env)
            other_val = env.get(other_val, other_val)
            if (
                op == '=' and val != other_val or
                op == '>' and val <= other_val or
                op == '<' and val > other_val or
                op == '>=' and val < other_val or
                op == '<=' and val > other_val
            ):
                return None
        return True

    def math_op(self, op: str, lisp_list: list, env: dict = None):
        acc = env.get(lisp_list[0], lisp_list[0])
        for elem in lisp_list[1:]:
            val = self.evaluate(elem, env)
            val = env.get(val, val)
            check_is_number(val)
            if op == '+':
                acc += val
            elif op == '-':
                acc -= val
            elif op == '*':
                acc *= val
            else:
                acc /= val
        return acc

    def bind_cond_vars(self, cond: list, vars: list, env: dict = None):
        pass

    def eval_if(self, args: list=None, env=None):
        cond = args[0]
        val = args[1]
        true_branch = args[2]
        false_branch = args[3]

        val = self.evaluate(val, env)

        pass

    def define(self, lisp_list: list, env=None):
        ident = self.evaluate(lisp_list[0], env)
        val = self.evaluate(lisp_list[1], env)
        env[ident] = val
        return val

    def print(self, args: list, env=None):
        val = self.evaluate(args, env)
        print(env.get(val, val))
        return val


