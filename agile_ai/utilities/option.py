class Option:
    @staticmethod
    def empty():
        option = Option(None)
        option._has_value = False
        return option
    def __init__(self, value):
        self.value = value
        self._has_value = True

    def get(self):
        if not self._has_value:
            raise ValueError("Unable to call get on an empty Option")
        return self.value

    def is_present(self):
        return self._has_value

    def is_empty(self):
        return not self.is_present()
