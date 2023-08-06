class ZAPIError(Exception):
    def __init__(self, status_code, error_response):
        self.message = "ZAPI returned " + str(status_code) + ": " + error_response['errorMsg']
        self.status_code = status_code
        self.error_message = error_response['errorMsg']
        super().__init__(self.message)

    pass


class ResourceNotFoundError(Exception):
    def __init__(self, resource_type, resource_name):
        self.message = resource_type + " '" + resource_name + "' was not found."
        self.resource_type = resource_type
        self.resource_name = resource_name
        super().__init__(self.message)

    pass


class InsufficientContextError(Exception):
    def __init__(self, context_resource):
        self.message = "There was insufficient context: " + context_resource + " has not been set."
        self.missing_context = context_resource
        super().__init__(self.message)

    pass


class MissingParametersError(Exception):
    def __init__(self, parameters):
        self.message = "The following parameters were missing from the caller: " + ", ".join(parameters)
        self.missing_parameters = parameters
        super().__init__(self.message)

    pass


class MethodNotImplementedError(Exception):
    def __init__(self, message):
        self.message = "This method has not fully been implemented yet: " + message
        super().__init__(self.message)

    pass
