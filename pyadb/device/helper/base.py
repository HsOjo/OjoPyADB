class BaseHelper:
    def __init__(self, device):
        self.device = device

    def params(self, locals_: dict):
        params = locals_.copy()
        params.pop('self')
        return params
