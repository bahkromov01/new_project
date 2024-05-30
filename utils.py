class ResponseData:
    def __init__(self,
                 data,
                 status_code=200,
                 success=True):
        self.data = data
        self.status_code = status_code
        self.success = success


class BadRequest:
    def __init__(self, data, status_code=400):
        self.data = data
        self.status_code = status_code
