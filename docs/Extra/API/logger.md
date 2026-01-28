## Logger Setup - Docker Python Log Tool
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Usage Example
```python
logger.info("This is an info message")
logger.error("This is an error message")
logger.debug("This is a debug message")
logger.warning("This is a warning message")
logger.critical("This is a critical message")
logger.exception("This is an exception message")
```