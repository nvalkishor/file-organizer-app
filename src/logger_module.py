import logging
import os


def setup_logger(log_file='app.log'):
    """
    Sets up the logging configuration.

    Parameters:
    log_file (str): The log file where logs are saved.
    """
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def log_operation(operation):
    """
    Logs an operation performed by the application.

    Parameters:
    operation (str): Description of the operation.
    """
    logging.info(f'Operation performed: {operation}')


# Example usage
if __name__ == '__main__':
    setup_logger()
    log_operation('Application started')
    log_operation('Sample operation executed')
