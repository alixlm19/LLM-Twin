class CrawlerError(Exception):
    pass


class InvalidDriverSettingsSchemaError(CrawlerError):
    pass


class EmptyDriverSettingsError(CrawlerError):
    pass


class UnsupportedDriverError(CrawlerError):
    pass


class DriverBuildError(CrawlerError):
    pass


class InvalidDriverOptionError(CrawlerError):
    pass


class UnsupportedTagError(CrawlerError):
    pass
