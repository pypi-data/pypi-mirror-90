class ZAPIError(Exception):
    def __init__(self, response_object):
        self.message = "ZAPI returned " + str(response_object.status_code) + "\nResponse:\n" + response_object.text
        self.status_code = response_object.status_code
        self.error_message = response_object.text
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
