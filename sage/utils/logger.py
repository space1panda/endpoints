import logging


def set_logger(
        level: int = 10
        ):
    levels = [10, 20, 30, 40, 50]
    assert level in levels, f'{level} is not in {levels}'
    # Configure the logger
    logging.basicConfig(
        level=level,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
        handlers=[
            logging.FileHandler('app.log'),  # Log to a file
            logging.StreamHandler()  # Log to the console
        ]
    )