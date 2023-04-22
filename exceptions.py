"""Scraper APP Exceptions"""


class OrderAPPException(Exception):
    customer_message = "Something went wrong. Please try again later."

    def __init__(self, *args):
        if args:
            self.customer_message = args[0]
        super().__init__(self.customer_message)


# File Exceptions
class InitializeFileError(OrderAPPException):
    customer_message = "Files not initialized. Run initialize_file.py."
