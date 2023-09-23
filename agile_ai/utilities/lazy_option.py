from agile_ai.utilities.option import Option


class LazyOption(Option):
    def get(self):
        return Option.get(self)()