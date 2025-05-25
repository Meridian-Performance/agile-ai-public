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
            self.inject(instance, cls)
        return self.instance_by_cls[cls]

    def inject(self, instance, for_cls=None):
        if for_cls is None:
            for_cls = instance.__class__
        self.instance_by_cls[for_cls] = instance
