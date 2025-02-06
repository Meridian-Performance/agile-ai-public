from agile_ai.utilities.option import Option, OptionT


class NoMemo:
    pass


class MemoOption(Option[OptionT]):
    _memo: any

    def __init__(self, value):
        Option.__init__(self, value)
        self._memo = NoMemo

    def get(self) -> OptionT:
        if self._memo == NoMemo:
            self._memo = Option.get(self)()
        return self._memo
