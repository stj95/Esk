import logging

def create_logger(name, path):
    """
    Create logger object

    :return:
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = 0

    file_handler = logging.FileHandler(path)
    stream_handler = logging.StreamHandler()

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger