import logging

def get_configured_logger(log_file_name: str = "crawler.log") -> logging:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file_name),
            logging.StreamHandler()
        ]
    )
    return logging