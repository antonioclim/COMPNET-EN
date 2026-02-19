#!/usr/bin/env python3
"""
[PROJECT_NAME] — [One-line description]

This module implements [brief description of functionality].

Usage:
    python main.py [options]

Example:
    python main.py --config config.yaml --verbose

Author: [Student Name]
Course: Computer Networks — ASE Bucharest
Project: P[XX]
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    import yaml
except ImportError:
    print("[ERROR] PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════
VERSION = "1.0.0"
DEFAULT_CONFIG = Path("config.yaml")
DEFAULT_LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = "app.log"

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR_CONFIG = 1
EXIT_ERROR_NETWORK = 2
EXIT_ERROR_RUNTIME = 3


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGING_SETUP
# ═══════════════════════════════════════════════════════════════════════════════
def setup_logging(
    level: int = DEFAULT_LOG_LEVEL,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    Configure logging with both console and file handlers.
    
    Args:
        level: Logging level (default: INFO)
        log_file: Path to log file (default: app.log)
        
    Returns:
        Configured logger instance
        
    Example:
        >>> logger = setup_logging(logging.DEBUG)
        >>> logger.info("Application started")
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console_handler)
    
    # File handler
    file_path = log_file or Path(LOG_FILE)
    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
    ))
    logger.addHandler(file_handler)
    
    return logger


# Initialise logger
logger = setup_logging()


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════
def load_config(path: Path) -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        path: Path to configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is invalid YAML
        
    Example:
        >>> config = load_config(Path("config.yaml"))
        >>> print(config.get("server", {}).get("port", 8080))
        
    # 💭 PREDICTION: What happens if the file doesn't exist?
    # Answer: FileNotFoundError is raised with descriptive message
    """
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            
        if config is None:
            return {}
            
        logger.info(f"Configuration loaded from {path}")
        return config
        
    except yaml.YAMLError as e:
        logger.error(f"Invalid YAML in {path}: {e}")
        raise


def validate_config(config: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Validate that configuration contains required keys.
    
    Args:
        config: Configuration dictionary
        required_keys: List of required top-level keys
        
    Returns:
        True if all required keys present, False otherwise
        
    # 💭 PREDICTION: What happens with nested required keys?
    # Answer: Only checks top-level; use dot notation for nested
    """
    missing = [key for key in required_keys if key not in config]
    
    if missing:
        logger.error(f"Missing required configuration keys: {missing}")
        return False
        
    return True


# ═══════════════════════════════════════════════════════════════════════════════
# CORE_LOGIC
# ═══════════════════════════════════════════════════════════════════════════════
class NetworkApplication:
    """
    Main application class for [PROJECT_NAME].
    
    This class handles [brief description of what it manages].
    
    Attributes:
        config: Application configuration dictionary
        running: Whether the application is currently running
        
    Example:
        >>> app = NetworkApplication({"server": {"port": 8080}})
        >>> app.start()
        >>> # ... application runs ...
        >>> app.stop()
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialise the network application.
        
        Args:
            config: Configuration dictionary with application settings
        """
        self.config = config
        self.running = False
        self._resources: List[Any] = []
        
        logger.info("Application initialised")
        logger.debug(f"Configuration: {config}")
    
    def start(self) -> None:
        """
        Start the application.
        
        Raises:
            RuntimeError: If application is already running
            
        # 💭 PREDICTION: What should happen if start() is called twice?
        # Answer: RuntimeError to prevent resource conflicts
        """
        if self.running:
            raise RuntimeError("Application is already running")
        
        logger.info("Starting application...")
        
        # TODO: Implement your startup logic here
        # Example:
        # - Initialise network connections
        # - Start background threads/tasks
        # - Set up event handlers
        
        self.running = True
        logger.info("Application started successfully")
    
    def stop(self) -> None:
        """
        Stop the application gracefully.
        
        Ensures all resources are properly released.
        """
        if not self.running:
            logger.warning("Application is not running")
            return
        
        logger.info("Stopping application...")
        
        # TODO: Implement your cleanup logic here
        # Example:
        # - Close network connections
        # - Stop background threads
        # - Flush buffers
        
        # Clean up resources
        for resource in self._resources:
            try:
                if hasattr(resource, "close"):
                    resource.close()
            except Exception as e:
                logger.warning(f"Error closing resource: {e}")
        
        self._resources.clear()
        self.running = False
        logger.info("Application stopped")
    
    def __enter__(self) -> "NetworkApplication":
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.stop()


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER_FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════
def validate_port(port: int) -> bool:
    """
    Check if port number is within valid range.
    
    Args:
        port: Port number to validate
        
    Returns:
        True if port is valid (1-65535), False otherwise
        
    Example:
        >>> validate_port(8080)
        True
        >>> validate_port(70000)
        False
    """
    return 1 <= port <= 65535


def validate_ip_address(ip: str) -> bool:
    """
    Validate IPv4 address format.
    
    Args:
        ip: IP address string to validate
        
    Returns:
        True if valid IPv4 format, False otherwise
        
    Example:
        >>> validate_ip_address("192.168.1.1")
        True
        >>> validate_ip_address("999.999.999.999")
        False
    """
    parts = ip.split(".")
    
    if len(parts) != 4:
        return False
    
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# ARGUMENT_PARSING
# ═══════════════════════════════════════════════════════════════════════════════
def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace
        
    Example:
        >>> args = parse_arguments()
        >>> print(args.config)
        config.yaml
    """
    parser = argparse.ArgumentParser(
        description="[PROJECT_NAME] — [Brief description]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --config config.yaml
    %(prog)s --verbose --port 8080
    %(prog)s --help

For more information, see the project documentation.
        """
    )
    
    parser.add_argument(
        "--config", "-c",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Path to configuration file (default: %(default)s)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose (DEBUG) logging"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Suppress all output except errors"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without starting"
    )
    
    return parser.parse_args()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    """
    Application entry point.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
        
    Exit codes:
        0 - Success
        1 - Configuration error
        2 - Network error
        3 - Runtime error
    """
    args = parse_arguments()
    
    # Configure logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
    elif args.quiet:
        logger.setLevel(logging.ERROR)
        for handler in logger.handlers:
            handler.setLevel(logging.ERROR)
    
    try:
        # Load configuration
        logger.info(f"Loading configuration from {args.config}")
        config = load_config(args.config)
        
        # Validate configuration
        # TODO: Add your required keys
        required_keys = ["server"]  # Example
        if not validate_config(config, required_keys):
            return EXIT_ERROR_CONFIG
        
        # Dry run mode
        if args.dry_run:
            logger.info("Configuration valid. Dry run complete.")
            return EXIT_SUCCESS
        
        # Create and run application
        with NetworkApplication(config) as app:
            logger.info("Application running. Press Ctrl+C to stop.")
            
            # TODO: Implement your main loop here
            # Example:
            # while app.running:
            #     app.process_events()
            
            # For now, just wait for interrupt
            try:
                import time
                while app.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Received interrupt signal")
        
        return EXIT_SUCCESS
        
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        logger.error(f"Usage: python {sys.argv[0]} --config <path>")
        return EXIT_ERROR_CONFIG
        
    except yaml.YAMLError as e:
        logger.error(f"Invalid configuration file: {e}")
        return EXIT_ERROR_CONFIG
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return EXIT_SUCCESS
        
    except OSError as e:
        logger.error(f"Network error: {e}")
        return EXIT_ERROR_NETWORK
        
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return EXIT_ERROR_RUNTIME


if __name__ == "__main__":
    sys.exit(main())
