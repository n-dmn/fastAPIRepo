class UnknownConnectorError(KeyError):
    """Raised when an unknown connector is requested."""


class MissingDSNError(ValueError):
    """Raised when a required DSN is missing in configuration."""
