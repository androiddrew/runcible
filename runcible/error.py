from molten.errors import MoltenError


class EntityNotFound(MoltenError):
    """Raised when an entity is not found using an `exists` check in sqlalchemy."""


class ConfigurationError(MoltenError):
    """Raised when an a configuration parameter is not found or is invalid."""
