class InvalidDriverSettingsSchemaError(Exception):
    pass


class EmptyDriverSettingsError(Exception):
    pass


class UnsupportedDriverError(Exception):
    pass


class DriverBuildError(Exception):
    pass


class InvalidDriverOptionError(Exception):
    pass
