from agile_ai.processing.processor_io import IO


class Processor:
    def perform_super(self, inputs: IO):
        outputs = self._get_outputs(inputs)
        self.perform(inputs, outputs)
        outputs.store_options()
        return outputs

    def _get_outputs(self, inputs: IO):
        key_part = inputs.get_key()
        outputs: IO = self.get_outputs_cls()()
        outputs.init_options(key_part)
        return outputs

    def perform(self, inputs, outputs):
        raise NotImplementedError

    def resolve(self, inputs: IO) -> IO:
        outputs = self._get_outputs(inputs)
        if outputs.all_options_present():
            return outputs
        return self.perform_super(inputs)

    @classmethod
    def get_outputs_cls(cls) -> IO:
        return cls.Outputs