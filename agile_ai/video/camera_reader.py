from typing import Union

import cv2

from agile_ai.video.video_reader import ColorType


class CameraReader:
    video_source: Union[int, str]
    source_color: ColorType
    output_color: ColorType

    def __init__(self, video_source: Union[int, str] = 0, source_color=ColorType.BGR, output_color=ColorType.RGB):
        self.video_source = video_source
        self.source_color = source_color
        self.output_color = output_color

    def get_frames(self):
        capture = cv2.VideoCapture(self.video_source)
        while True:
            success, frame = capture.read()
            if not success:
                break
            if cv2.waitKey(1) == ord('q'):
                break
            yield ColorType.convert(frame, self.source_color, self.output_color)
        capture.release()
