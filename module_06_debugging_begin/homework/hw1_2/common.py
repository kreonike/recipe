import logging

def configure_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='[%(asctime)s.%(msecs)03d] %(module)s:%(levelname)7s - %(message)s',
        handlers=[
            logging.FileHandler('stderr.txt', mode='w'),
            logging.StreamHandler()
        ]
    )