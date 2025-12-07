from argparse import ArgumentParser
from pathlib import Path
from humanhanddetect.logging_utils import get_logger, setup_logging
from config_parser import ConfigParser

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





if __name__ == "__main__":
    main()