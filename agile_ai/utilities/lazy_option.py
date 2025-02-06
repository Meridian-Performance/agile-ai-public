from agile_ai.utilities.option import Option, OptionT


class LazyOption(Option[OptionT]):
    def get(self) -> OptionT:
        return Option.get(self)()