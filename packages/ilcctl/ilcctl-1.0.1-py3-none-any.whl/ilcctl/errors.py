class ResourceNotFound(Exception):
    """
    Common exception base class in case of an invalid UUID
    """
    def __init__(self, uuid):
        self.uuid = uuid


class ServiceNotFound(ResourceNotFound):
    """
    Exception class for invalid service UUID
    """
    def __str__(self):
        return 'Requested service with UUID {} was not found'.format(self.uuid)


class CharacteristicNotFound(ResourceNotFound):
    """
    Exception class for invalid characteristic UUID
    """
    def __str__(self):
        return 'Requested characteristic with UUID {} was not found'.format(self.uuid)
