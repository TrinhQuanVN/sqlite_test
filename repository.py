import data_access

class repository:
    def __init__(self, context:data_access) -> None:
        self.context = context
        self.con