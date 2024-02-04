from agile_ai.memoization.warehouse_service import register_object_class
from agile_ai.processing.stream_object import StreamObject, StreamElementT


class FrameStreamObject(StreamObject):
    @classmethod
    def get_extension(cls):
        raise NotImplementedError

    def make_even(self, frame):
        if frame.shape[0] % 2:
            frame = frame[:-1]
        if frame.shape[1] % 2:
            frame = frame[:, :-1]
        return frame

    def put_element(self, index: int, element: StreamElementT) -> StreamElementT:
        self.get_element_path(index).put(self.make_even(element))
        return element

    def get_input_path(self):
        if self.generator:
            self.consume()
        return self.get_object_path() // f"element_%06d.{self.get_extension()}"



class JpgFrameStreamObject(FrameStreamObject):
    @classmethod
    def get_extension(cls):
        return "jpg"


class PngFrameStreamObject(FrameStreamObject):
    @classmethod
    def get_extension(cls):
        return "png"

register_object_class(JpgFrameStreamObject)
register_object_class(PngFrameStreamObject)
