class Statement:
    def __init__(self, args: list = None, env: dict = None):
        self.args = args
        self.env = env


class PrintStatement(Statement):
    def __init__(self, args=None, env=None):
        super().__init__(args, env)
