from argparse import ArgumentParser
from pathlib import Path
from humanhanddetect.logging_utils import get_logger, setup_logging
from humanhanddetect.config_parser import ConfigParser
from humanhanddetect.video_capture import VideoCapture

def main():
    parser = ArgumentParser(description="Human and Hand Detection CLI")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the configuration file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )
    args = parser.parse_args()
    setup_logging(verbose=args.verbose)
    logger = get_logger(__name__)
    if not args.config.exists():
        logger.error(f"Configuration file {args.config} does not exist.")
        return

    config = ConfigParser(config_path = args.config)

    cap = VideoCapture(
        source=config.video_source,
        fps=config.video_fps,
        logger=logger,
    )

    if not cap.open():
        logger.error("Failed to open video source.")
        return
    try:
        while True:
            frame = cap.read()
            if frame is None:
                break
            # TODO: Add processing logic here
    except KeyboardInterrupt:
        logger.info("Interrupted by user (KeyboardInterrupt).")
    finally:
        cap.close()
        logger.info("Cleaned up. Bye!")




if __name__ == "__main__":
    main()