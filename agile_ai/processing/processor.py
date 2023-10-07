from agile_ai.processing.processor_io import IO


class Processor:
    def perform_super(self, inputs: IO):
        key_part = inputs.get_key()
        outputs: IO = self.get_outputs_cls()()
        outputs.init_options(key_part)
        self.perform(inputs, outputs)
        outputs.store_options()
        return outputs

    def perform(self, inputs, outputs):
        raise NotImplementedError

    @classmethod
    def get_outputs_cls(cls) -> IO:
        return cls.Outputs