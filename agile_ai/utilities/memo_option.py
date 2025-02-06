from agile_ai.utilities.option import Option

class NoMemo:
    pass

class MemoOption(Option):
    _memo: any

    def __init__(self, value):
        Option.__init__(self, value)
        self._memo = NoMemo

    def get(self):
        if self._memo == NoMemo:
            self._memo = Option.get(self)()
        return self._memo