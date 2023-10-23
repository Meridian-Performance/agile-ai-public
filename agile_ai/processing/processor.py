from typing import Type

from agile_ai.injection.decorators import autowire_services
from agile_ai.processing.processor_io import IO
from agile_ai.utilities.introspection import Introspection


class Processor:
    Inputs: Type[IO]
    Outputs: Type[IO]
    inputs: IO

    def __init__(self):
        self.inputs = self.get_inputs_cls()()
        self.inputs.init_options(None)
        self.initialize_services()

    @classmethod
    def initialize_services(cls):
        autowire_services(cls)

    def perform_super(self, inputs: IO):
        outputs = self._get_outputs(inputs)
        self.perform(inputs, outputs)
        outputs.store_options()
        return outputs

    def _get_outputs(self, inputs: IO):
        outputs: IO = self.get_outputs_cls()()
        key_part = inputs.get_key()
        outputs.init_options(key_part)
        return outputs

    def perform(self, inputs, outputs):
        raise NotImplementedError

    def resolve(self) -> IO:
        outputs = self._get_outputs(self.inputs)
        class_name = Introspection.get_class_name(self.__class__)
        print(f"<{class_name}> Checking outputs")
        if outputs.has_options() and outputs.all_options_present(status_log=True):
            print(f"<{class_name}> Resolved: all options present")
            return outputs
        print(f"<{class_name}> Not resolved: calling perform")
        return self.perform_super(self.inputs)

    @classmethod
    def get_inputs_cls(cls) -> Type[IO]:
        return cls.Inputs

    @classmethod
    def get_outputs_cls(cls) -> Type[IO]:
        return cls.Outputs
