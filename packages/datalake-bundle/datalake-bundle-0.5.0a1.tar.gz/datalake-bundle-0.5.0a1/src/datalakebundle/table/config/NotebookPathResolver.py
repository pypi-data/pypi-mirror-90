from box import Box
from databricksbundle.container.containerInitResolver import getContainerInit
from injecta.dtype.classLoader import loadClass
from injecta.package.pathResolver import resolvePath
from datalakebundle.table.identifier.ValueResolverInterface import ValueResolverInterface

class NotebookPathResolver(ValueResolverInterface):

    def __init__(
        self,
        notebookPathTemplate: str
    ):
        self.__notebookPathTemplate = notebookPathTemplate

    def resolve(self, rawTableConfig: Box):
        replacements = rawTableConfig
        replacements['rootModulePath'] = self.__getRootModulePath()

        return self.__notebookPathTemplate.format(**replacements)

    def __getRootModulePath(self):
        containerInitConfig = getContainerInit()

        class_ = loadClass(containerInitConfig[0], containerInitConfig[1]) # pylint: disable = invalid-name
        rootModuleName = class_.__module__[0:class_.__module__.find('.')]

        return resolvePath(rootModuleName).replace('\\', '/')
