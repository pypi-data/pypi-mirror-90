from logging import Logger, Filter
from loggerbundle.LoggerFactory import LoggerFactory
from datalakebundle.table.config.TableConfig import TableConfig

class TableLoggerFactory:

    def __init__(
        self,
        loggerFactory: LoggerFactory,
    ):
        self.__loggerFactory = loggerFactory

    def create(self, tableConfig: TableConfig) -> Logger:
        class DefaultExtraFieldsFilter(Filter):
            def filter(self, record):
                if not hasattr(record, 'dbIdentifier'):
                    record.dbIdentifier = tableConfig.dbIdentifier
                if not hasattr(record, 'dbName'):
                    record.dbName = tableConfig.dbName
                if not hasattr(record, 'tableIdentifier'):
                    record.tableIdentifier = tableConfig.tableIdentifier
                if not hasattr(record, 'tableName'):
                    record.tableName = tableConfig.tableName
                return True

        logger = self.__loggerFactory.create(tableConfig.identifier)
        logger.addFilter(DefaultExtraFieldsFilter())

        return logger
