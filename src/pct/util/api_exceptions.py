


class BaseOptimizerError(Exception):
    status_code = 400

    def __init__(self, message, http_status_code, application_error_code=None):
        Exception.__init__(self)

        self.message = message

        if http_status_code is not None:
            self.status_code = http_status_code

        self.application_error_code = application_error_code

        def to_dict(self):
            rv = {"status": {"status": self.status_code, "message": self.message, "app_code": self.application_error_code}}

            return rv

    class ValidationError(BaseModelError):

        def __init__(self, message, http_status_code, application_error_code=None):
            super().__init__(message, http_status_code, application_error_code)



