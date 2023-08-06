class WimsAPIError(Exception):
    """Base exception for WimsAPI."""
    pass



class InvalidResponseError(WimsAPIError):  # pragma: no cover
    """Raised when WIMS send a badly formatted response."""
    
    
    def __init__(self, message, response):
        self.message = message
        self.response = response
    
    
    def __str__(self):
        return self.message



class AdmRawError(WimsAPIError):
    """Raised when an error occurs while communicating with the WIMS server."""
    
    
    def __init__(self, message):
        self.message = message
    
    
    def __str__(self):
        return "WIMS' server responded with an ERROR: " + self.message



class NotSavedError(WimsAPIError):
    """Raised trying to use a method needing an object to be saved, without the object being
    actually saved (eg. deleting an unsaved class)."""
    pass



class InvalidItemTypeError(WimsAPIError):
    """Raised when trying to add/get/delete an invalide type from a WIMS class."""
    pass


class InvalidIdentifier(WimsAPIError):
    """Raised when an identifier containing invalid character is sent to WIMS."""
    pass
