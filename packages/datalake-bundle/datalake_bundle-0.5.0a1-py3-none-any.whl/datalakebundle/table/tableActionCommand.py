# pylint: disable = protected-access
from argparse import Namespace

def tableActionCommand(originalClass):
    originalRun = originalClass.run

    def run(self, inputArgs: Namespace):
        if not self._tablesConfigManager.exists(inputArgs.identifier):
            self._logger.error(f'Identifier {inputArgs.identifier} not found among datalakebundle.tables')
            return

        originalRun(self, inputArgs)

    originalClass.run = run
    return originalClass
