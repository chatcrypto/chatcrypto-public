"""
Define some basic exceptions
"""


class ExceptionRequestAPIError(Exception):
    message = "Request API error"

    def __init__(self, message="Request API error"):
        self.message = message
        super().__init__(self.message)


class ExceptionParamsForFuncError(Exception):
    message = "Params for func are invalid"


class ExceptionNeedShowMessage(Exception):
    """
    This exception will be used in case return error message for user
    """
    pass


class ExceptionNoExecutorToPick(Exception):
    """
    This exception will be used in case no executor thats picked to answer questions of user
    """
    pass


class NoAvailabelTools(Exception):
    """
    This exception will be used in case there is no available tools that will be picked to answer question
    """
    pass
