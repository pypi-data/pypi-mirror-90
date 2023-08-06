from pathlib import Path
from box import Box
from datalakebundle.table.config.TableConfig import TableConfig

class TableConfigResolver:

    def __init__(
        self,
        notebookPathTemplate: str,
        rawTableConfigs: Box,
    ):
        self.__notebookPathTemplate = notebookPathTemplate
        self.__rawTableConfigs = rawTableConfigs or Box()

    def resolve(self, notebookPath: Path) -> TableConfig:
        pathForwardSlashes = str(notebookPath).replace('\\', '/')
        pathParts = self.__parsePath(pathForwardSlashes)
        templateParts = self.__prepareTemplateParts()

        lenDiff = len(pathParts) - len(templateParts)

        if lenDiff < 0:
            raise Exception('datalakebundle.notebook.scriptPathTemplate doesn\'t match real notebook path')

        output = dict()

        for index, templatePart in reverseEnum(templateParts):
            if templatePart[0] == '{' and templatePart[-1] == '}':
                placeholderName = templatePart[1:-1]
                pathIndex = lenDiff + index
                replacement = pathParts[pathIndex]

                if placeholderName in output and output[placeholderName] != replacement:
                    raise Exception('Placeholder {' + placeholderName + '} matches different values from the real notebook path')

                output[placeholderName] = replacement

        resolvedIdentifier = output['dbIdentifier'] + '.' + output['tableIdentifier']

        for identifier, rawTableConfig in self.__rawTableConfigs.items():
            if identifier == resolvedIdentifier:
                return TableConfig.fromBox(identifier, rawTableConfig)

        raise Exception(f'No config found for {notebookPath} in datalakebundle.tables')

    def __prepareTemplateParts(self):
        templateParts = self.__parsePath(self.__notebookPathTemplate)

        if templateParts[0] == '{rootModulePath}':
            templateParts = templateParts[1:]

        if '{dbIdentifier}' not in templateParts:
            raise Exception('{dbIdentifier} placeholder must be used in datalakebundle.notebook.scriptPathTemplate')

        if '{tableIdentifier}' not in templateParts:
            raise Exception('{tableIdentifier} placeholder must be used in datalakebundle.notebook.scriptPathTemplate')

        return templateParts

    def __parsePath(self, path: str):
        if path[-3:] == '.py':
            path = path[:-3]
        if path[:1] == '/':
            path = path[1:]

        return path.split('/')

def reverseEnum(items):
    for index in reversed(range(len(items))):
        yield index, items[index]
