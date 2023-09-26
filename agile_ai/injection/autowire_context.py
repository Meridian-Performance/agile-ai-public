from functools import partial


class AutowireContext:
    def __init__(self):
        self.instance_by_cls = dict()

    def reset(self):
        self.instance_by_cls = dict()

    def autowire(self, cls):
        return property(lambda *args: self.get_service(cls))

    def get_service(self, cls):
        if cls not in self.instance_by_cls:
            instance = cls()
            self.instance_by_cls[cls] = instance
        return self.instance_by_cls[cls]
