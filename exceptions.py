"""Scraper APP Exceptions"""


class APPException(Exception):
    message = "Something went wrong. Please try again later."

    def __init__(self, *args):
        if args:
            self.message = args[0]
        super().__init__(self.message)


class InitializeFileError(APPException):
    message = "Files not initialized. Run initialize_file.py."


class EndOfAdsException(APPException):
    message = "End of ads queue."


class SkippedAdError(APPException):
    message = "Ad skipped."


class NetworkException(APPException):
    message = "Network problem or unknown link."
