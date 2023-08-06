from typing import List
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.container.ContainerInterface import ContainerInterface
from injecta.package.pathResolver import resolvePath
from pyfonycore.Kernel import Kernel
from pyfonybundles.Bundle import Bundle
from pyfonybundles.loader import pyfonyBundlesLoader, testingScopeBundlesLoader
from datalakebundle.DataLakeBundle import DataLakeBundle

def initContainer(appEnv: str):
    bundles = [*pyfonyBundlesLoader.loadBundles(), DataLakeBundle.autodetect()]

    return _createKernel(appEnv, bundles).initContainer()

def initContainerConsoleTesting(appEnv: str) -> ContainerInterface:
    bundles = [*testingScopeBundlesLoader.loadBundles('console'), DataLakeBundle.createForConsole()]

    return _createKernel(appEnv, bundles).initContainer()

def initContainerNotebookTesting(appEnv: str) -> ContainerInterface:
    bundles = [*testingScopeBundlesLoader.loadBundles('notebook'), DataLakeBundle.createForNotebook()]

    return _createKernel(appEnv, bundles).initContainer()

def _createKernel(appEnv: str, bundles: List[Bundle]):
    return Kernel(
        appEnv,
        resolvePath('datalakebundle') + '/_config',
        YamlConfigReader(),
        bundles,
    )
