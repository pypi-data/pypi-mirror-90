from box import Box
from datalakebundle.notebook.NotebookParams import NotebookParams
from datalakebundle.table.config.TableConfig import TableConfig

class NotebookParamsResolver:

    def __init__(
        self,
        rawTablesConfig: Box,
    ):
        self.__rawTablesConfig = rawTablesConfig

    def resolve(self, tableConfig: TableConfig) -> NotebookParams:
        if 'params' not in self.__rawTablesConfig[tableConfig.identifier]:
            return NotebookParams({})

        return self.__rawTablesConfig[tableConfig.identifier].params
