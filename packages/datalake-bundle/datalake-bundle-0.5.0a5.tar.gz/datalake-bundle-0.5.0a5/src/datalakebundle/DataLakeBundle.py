from typing import List
from box import Box
from consolebundle.detector import isRunningInConsole
from injecta.compiler.CompilerPassInterface import CompilerPassInterface
from pyfonybundles.Bundle import Bundle
from datalakebundle.table.config.TablesConfigCompilerPass import TablesConfigCompilerPass
from datalakebundle.table.identifier.Expression import Expression

Expression.yaml_loader.add_constructor(Expression.yaml_tag, Expression.from_yaml)

class DataLakeBundle(Bundle):

    SCOPE_NOTEBOOK = 'notebook_scope.yaml'
    SCOPE_CONSOLE = 'console_scope.yaml'

    @classmethod
    def autodetect(cls):
        if isRunningInConsole():
            return DataLakeBundle(DataLakeBundle.SCOPE_CONSOLE)

        return DataLakeBundle(DataLakeBundle.SCOPE_NOTEBOOK)

    @staticmethod
    def createForConsole():
        return DataLakeBundle(DataLakeBundle.SCOPE_CONSOLE)

    @staticmethod
    def createForNotebook():
        return DataLakeBundle(DataLakeBundle.SCOPE_NOTEBOOK)

    def __init__(self, notebookScopeConfig: str):
        self.__notebookScopeConfig = notebookScopeConfig

    def getConfigFiles(self):
        return ['config.yaml', 'scope/' + self.__notebookScopeConfig]

    def getCompilerPasses(self) -> List[CompilerPassInterface]:
        return [
            TablesConfigCompilerPass()
        ]

    def modifyParameters(self, parameters: Box) -> Box:
        if parameters.databricksbundle.notebook.logger == 'default':
            # changing databricksbundle's logger for datalakebundle's logger
            parameters.databricksbundle.notebook.logger = 'datalake_table'

        return parameters
