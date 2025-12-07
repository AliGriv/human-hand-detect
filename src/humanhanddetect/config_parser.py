from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Tuple, Any, Dict

from logging_utils import get_logger

logger = get_logger(__name__)


class ConfigParser:
    """
    @brief Configuration parser for the human-hand-detect application.

    The configuration is expected to be a JSON file with (at least) the following keys:
      - "yolo_onnx_path" : str (path to YOLO ONNX model)
      - "yolo_threshold" : float in [0, 1] (optional; default 0.25)
      - "yolo_input_size": [int, int] (width, height)
      - "video_source"   : str (e.g., "0" for webcam or a path/URL)
      - "video_fps"      : int
      - "classifier_model_path"   : str
      - "embedder_model_path"     : str
      - "hand_landmark_model_path": str
      - "hand_detection_model_path": str
      - "hand_detection_threshold": float in [0, 1] (optional; default 0.5)
      - "maximum_hands"           : int
      - "hands_nms_threshold"     : float in [0, 1] (optional; default 0.3)
    """

    # Default thresholds if not provided in config
    _DEFAULT_YOLO_THRESHOLD: float = 0.5
    _DEFAULT_HAND_DETECTION_THRESHOLD: float = 0.5
    _DEFAULT_HANDS_NMS_THRESHOLD: float = 0.3

    def __init__(self, config_path: Path) -> None:
        """
        @brief Initialize the configuration parser.

        @param config_path Path to the JSON configuration file.
        """
        self._config_path: Path = config_path

        self._yolo_onnx_path: Path
        self._yolo_threshold: float
        self._yolo_input_size: Tuple[int, int]
        self._video_source: str
        self._video_fps: int
        self._classifier_model_path: Path
        self._embedder_model_path: Path
        self._hand_landmark_model_path: Path
        self._hand_detection_model_path: Path
        self._hand_detection_threshold: float
        self._maximum_hands: int
        self._hands_nms_threshold: float

        self._load_config()

    # --- Properties ---------------------------------------------------------

    @property
    def yolo_onnx_path(self) -> Path:
        """@brief Path to YOLO ONNX model."""
        return self._yolo_onnx_path

    @property
    def yolo_threshold(self) -> float:
        """@brief Confidence threshold for YOLO detections."""
        return self._yolo_threshold

    @property
    def yolo_input_size(self) -> Tuple[int, int]:
        """@brief YOLO input size as (width, height)."""
        return self._yolo_input_size

    @property
    def video_source(self) -> str:
        """@brief Video source (e.g. '0' for webcam, file path, or URL)."""
        return self._video_source

    @property
    def video_fps(self) -> int:
        """@brief Target frames per second for video capture."""
        return self._video_fps

    @property
    def classifier_model_path(self) -> Path:
        """@brief Path to gesture classifier model."""
        return self._classifier_model_path

    @property
    def embedder_model_path(self) -> Path:
        """@brief Path to hand embedder model."""
        return self._embedder_model_path

    @property
    def hand_landmark_model_path(self) -> Path:
        """@brief Path to hand landmark model."""
        return self._hand_landmark_model_path

    @property
    def hand_detection_model_path(self) -> Path:
        """@brief Path to hand detection model."""
        return self._hand_detection_model_path

    @property
    def hand_detection_threshold(self) -> float:
        """@brief Detection threshold for hand detector."""
        return self._hand_detection_threshold

    @property
    def maximum_hands(self) -> int:
        """@brief Maximum number of hands to detect."""
        return self._maximum_hands

    @property
    def hands_nms_threshold(self) -> float:
        """@brief NMS (non-maximum suppression) threshold for hand detections."""
        return self._hands_nms_threshold

    # --- Internal helpers ---------------------------------------------------

    def _load_config(self) -> None:
        """
        @brief Load and validate configuration from the JSON file.

        @throws FileNotFoundError if the configuration file does not exist.
        @throws ValueError if the configuration content is invalid.
        """
        if not self._config_path.is_file():
            raise FileNotFoundError(f"Config file does not exist: {self._config_path}")

        logger.info(f"Loading configuration from '{self._config_path}'")

        try:
            with self._config_path.open("r", encoding="utf-8") as f:
                raw: Dict[str, Any] = json.load(f)
        except JSONDecodeError as exc:
            raise ValueError(f"Failed to parse JSON config: {exc}") from exc

        base_dir = self._config_path.parent

        def _require(key: str) -> Any:
            """
            @brief Retrieve a required key from the configuration.

            @param key Name of the configuration key.
            @return Value associated with the key.
            @throws ValueError if the key is missing.
            """
            if key not in raw:
                raise ValueError(f"Missing required configuration key: '{key}'")
            return raw[key]

        def _resolve_path(path_value: Any, key: str) -> Path:
            """
            @brief Resolve a path value from configuration.

            Relative paths are resolved with respect to the configuration file directory.

            @param path_value Raw path value from JSON (expected str).
            @param key Name of the configuration key (for error reporting).
            @return Resolved Path object.
            @throws ValueError if the value is not a string.
            """
            if not isinstance(path_value, str):
                raise ValueError(f"Configuration key '{key}' must be a string path.")
            path = Path(path_value)
            if not path.is_absolute():
                path = (base_dir / path).resolve()
            if not path.exists():
                raise ValueError(f"Path for key '{key}' does not exist: {path}")
            return path

        # --- Required path fields ---
        self._yolo_onnx_path = _resolve_path(_require("yolo_onnx_path"), "yolo_onnx_path")
        self._classifier_model_path = _resolve_path(
            _require("classifier_model_path"), "classifier_model_path"
        )
        self._embedder_model_path = _resolve_path(
            _require("embedder_model_path"), "embedder_model_path"
        )
        self._hand_landmark_model_path = _resolve_path(
            _require("hand_landmark_model_path"), "hand_landmark_model_path"
        )
        self._hand_detection_model_path = _resolve_path(
            _require("hand_detection_model_path"), "hand_detection_model_path"
        )

        # --- Thresholds with defaults ---
        yolo_thr_raw = raw.get("yolo_threshold", self._DEFAULT_YOLO_THRESHOLD)
        self._yolo_threshold = float(yolo_thr_raw)

        hand_det_thr_raw = raw.get(
            "hand_detection_threshold", self._DEFAULT_HAND_DETECTION_THRESHOLD
        )
        self._hand_detection_threshold = float(hand_det_thr_raw)

        hands_nms_thr_raw = raw.get(
            "hands_nms_threshold", self._DEFAULT_HANDS_NMS_THRESHOLD
        )
        self._hands_nms_threshold = float(hands_nms_thr_raw)

        # Basic sanity check on thresholds
        for name, value in (
            ("yolo_threshold", self._yolo_threshold),
            ("hand_detection_threshold", self._hand_detection_threshold),
            ("hands_nms_threshold", self._hands_nms_threshold),
        ):
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"Configuration '{name}' must be in [0, 1], got {value}.")

        # --- YOLO input size ---
        yolo_input_raw = _require("yolo_input_size")
        if (
            not isinstance(yolo_input_raw, (list, tuple))
            or len(yolo_input_raw) != 2
        ):
            raise ValueError(
                "Configuration 'yolo_input_size' must be a list/tuple of two integers [width, height]."
            )
        try:
            width = int(yolo_input_raw[0])
            height = int(yolo_input_raw[1])
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "Configuration 'yolo_input_size' must contain integer values."
            ) from exc
        self._yolo_input_size = (width, height)

        # --- Video source and FPS ---
        video_source_raw = _require("video_source")
        if not isinstance(video_source_raw, str):
            raise ValueError("Configuration 'video_source' must be a string.")
        self._video_source = video_source_raw

        video_fps_raw = _require("video_fps")
        try:
            self._video_fps = int(video_fps_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("Configuration 'video_fps' must be an integer.") from exc

        # --- Maximum hands ---
        max_hands_raw = _require("maximum_hands")
        try:
            self._maximum_hands = int(max_hands_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("Configuration 'maximum_hands' must be an integer.") from exc

        logger.info("Configuration successfully loaded and validated.")
        logger.debug(
            "Parsed config: \n\tyolo_onnx_path='{}', \n\tyolo_threshold={}, "
            "\n\tyolo_input_size={}, \n\tvideo_source='{}', \n\tvideo_fps={}, "
            "\n\tclassifier_model_path='{}', \n\tembedder_model_path='{}', "
            "\n\thand_landmark_model_path='{}', \n\thand_detection_model_path='{}', "
            "\n\thand_detection_threshold={}, \n\tmaximum_hands={}, \n\thands_nms_threshold={}",
            self._yolo_onnx_path,
            self._yolo_threshold,
            self._yolo_input_size,
            self._video_source,
            self._video_fps,
            self._classifier_model_path,
            self._embedder_model_path,
            self._hand_landmark_model_path,
            self._hand_detection_model_path,
            self._hand_detection_threshold,
            self._maximum_hands,
            self._hands_nms_threshold,
        )
