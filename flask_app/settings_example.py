#QA
STRIPE_API_KEYS = {}
#mirror the logging levels in python - docs here.
#setting the logging levels to 'error' will ignore everything below it
LOGGING_LEVELS = {
    'debug'    : 10, # Detailed information, typically of interest only when diagnosing problems.
    'info'     : 20, # Confirmation that things are working as expected.
    'warning'  : 30, # An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
    'error'    : 40, # Due to a more serious problem, the software has not been able to perform some function.
    'critical' : 50  # A serious error, indicating that the program itself may be unable to continue running.
}

SECRET_KEY = '' #put a randomly generated key here - something like os.urandom(24) from shell.