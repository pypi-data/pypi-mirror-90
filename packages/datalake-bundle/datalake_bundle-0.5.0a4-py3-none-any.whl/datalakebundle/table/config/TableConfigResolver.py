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

        replacements = self.__prepareReplacements(pathForwardSlashes)

        return self.__createMatchingConfigs(replacements, pathForwardSlashes)

    def __prepareReplacements(self, pathForwardSlashes: str):
        pathParts = self.__parsePath(pathForwardSlashes)
        templateParts = self.__prepareTemplateParts()

        lenDiff = len(pathParts) - len(templateParts)

        if lenDiff < 0:
            raise Exception('datalakebundle.notebook.scriptPathTemplate doesn\'t match real notebook path')

        replacements = dict()

        for index, templatePart in reverseEnum(templateParts):
            if templatePart[0] == '{' and templatePart[-1] == '}':
                placeholderName = templatePart[1:-1]
                pathIndex = lenDiff + index
                replacement = pathParts[pathIndex]

                if placeholderName in replacements and replacements[placeholderName] != replacement:
                    raise Exception('Placeholder {' + placeholderName + '} matches different values from the real notebook path')

                replacements[placeholderName] = replacement

        return replacements

    def __createMatchingConfigs(self, replacements: dict, pathForwardSlashes: str) -> TableConfig:
        outputKeys = replacements.keys()
        matchingConfigs = []

        for identifier, rawTableConfig in self.__rawTableConfigs.items():
            primaryKeyAttributes = {key: val for key, val in rawTableConfig.items() if key in outputKeys}

            if primaryKeyAttributes == replacements:
                matchingConfigs.append(TableConfig.fromBox(identifier, rawTableConfig))

        if not matchingConfigs:
            raise Exception(f'No config found for {pathForwardSlashes} in datalakebundle.tables')

        if len(matchingConfigs) > 1:
            raise Exception(f'Multiple configurations found for keys: {outputKeys}')

        return matchingConfigs[0]

    def __prepareTemplateParts(self):
        templateParts = self.__parsePath(self.__notebookPathTemplate)

        if templateParts[0] == '{rootModulePath}':
            templateParts = templateParts[1:]

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
