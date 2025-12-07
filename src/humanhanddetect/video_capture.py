import cv2
import numpy as np
from typing import Optional, Union
from logging_utils import get_logger


class VideoCapture:
    """
    @class VideoCapture
    @brief Thin wrapper around cv2.VideoCapture with logging and source resolution.
    """

    def __init__(self, source: str, fps: int, logger=None) -> None:
        """
        @brief Initialize the video capture interface.
        @param source String representing webcam index or file path.
        @param fps Desired frames per second for processing.
        @param logger Optional logger instance; fallback to module logger.
        """
        self.logger = logger or get_logger(__name__)
        self._source: Union[int, str] = self._resolve_source(source)
        self._fps: int = fps
        self._cap: Optional[cv2.VideoCapture] = None
        self._frame_width: Optional[int] = None
        self._frame_height: Optional[int] = None

    def _resolve_source(self, source: str) -> Union[int, str]:
        """
        @brief Convert input source string into webcam index or file path.
        @param source Input source string provided by user.
        @return Integer webcam index if convertible; otherwise file path.
        """
        try:
            idx = int(source)
            self.logger.info(f"Using webcam index: {idx}")
            return idx
        except ValueError:
            self.logger.info(f"Using video file: {source}")
            return source

    def open(self) -> bool:
        """
        @brief Open the video capture device or file.
        @return True if successfully opened, otherwise False.
        """
        self._cap = cv2.VideoCapture(self._source)
        if not self._cap.isOpened():
            self.logger.error(f"Failed to open video source: {self._source}")
            return False

        self._frame_width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._frame_height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.logger.debug(f"Video source opened: {self._source}")
        self.logger.debug(
            f"Frame dimensions: {self._frame_width}x{self._frame_height}"
        )
        return True

    def read(self) -> Optional[np.ndarray]:
        """
        @brief Read a single frame from the video source.
        @return Frame as a numpy array, or None on failure.
        """
        if self._cap is None:
            self.logger.error("read() called before open().")
            return None

        ret, frame = self._cap.read()
        if not ret:
            self.logger.warning("Failed to read frame.")
            return None

        return frame

    def close(self) -> None:
        """
        @brief Release the video capture resource.
        """
        if self._cap is not None:
            self._cap.release()
            self.logger.debug("Video source released.")
