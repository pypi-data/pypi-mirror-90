class Error(Exception):
    """Base Error Class"""

    def __init__(self, message):
        self.message = str(message)

    def __str__(self):
        return f"Something went wrong: {self.message}"


class DownloadError(Error):
    """Exception raised for errors Office365 download errors"""

    def __init__(self, expression):
        self.expression = expression
        self.message = self.expression.message
        self.response = self.expression.response

    def __str__(self):
        return f"Download Error: {self.message}, Request Status: {self.response.status_code}"


class DeleteError(Error):
    """Exception raised for errors Office365 delete errors"""

    def __init__(self, expression):
        self.expression = expression
        self.message = self.expression.message
        self.response = self.expression.response

    def __str__(self):
        return f"Delete Error: {self.message}, Request Status: {self.response.status_code}"
