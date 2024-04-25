class Env:
    def __init__(self, env: dict):
        self.env = env

    def add(self, var: str, val):
        self.env[var] = val
