import logging
#Configure logging
logging.basicConfig(
    filename='app.log',
    filemode='a',  # Append mode, change to 'w' for write mode
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger object
logger = logging.getLogger('my_logger')

# Log messages at different severity levels
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')