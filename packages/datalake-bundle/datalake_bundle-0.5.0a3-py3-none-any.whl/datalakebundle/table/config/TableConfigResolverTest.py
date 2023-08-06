import unittest
from pathlib import Path
from box import Box
from datalakebundle.table.config.TableConfig import TableConfig
from datalakebundle.table.config.TableConfigResolver import TableConfigResolver

class TableConfigResolverTest(unittest.TestCase):

    def test_basic(self):
        tableConfigParser = TableConfigResolver(
            '{rootModulePath}/foo/{dbIdentifier}/{tableIdentifier}/{tableIdentifier}',
            Box({
                'mydatabase.my_table': {
                    'schemaPath': 'datalakebundle.test.TestSchema',
                    'dbIdentifier': 'mydatabase',
                    'dbName': 'test_mydatabase',
                    'tableIdentifier': 'my_table',
                    'tableName': 'my_table',
                    'targetPath': '/data/mydatabase/my_table',
                }
            })
        )

        result = tableConfigParser.resolve(Path('/foo/bar/mydatabase/my_table/my_table.py'))

        expectedResult = TableConfig(
            'mydatabase.my_table',
            'test_mydatabase',
            'my_table',
            'datalakebundle.test.TestSchema',
            '/data/mydatabase/my_table'
        )

        self.assertEqual(expectedResult, result)

    def test_missingPlaceholder(self):
        tableConfigParser = TableConfigResolver(
            '/foo/{tableIdentifier}',
            Box({})
        )

        with self.assertRaises(Exception) as cm:
            tableConfigParser.resolve(Path('/foo/my_table.py'))

        self.assertEqual('No config found for /foo/my_table.py in datalakebundle.tables', str(cm.exception))

    def test_placeholderNotMatching(self):
        tableConfigParser = TableConfigResolver(
            '/foo/{dbIdentifier}/{tableIdentifier}',
            Box({})
        )

        with self.assertRaises(Exception) as cm:
            tableConfigParser.resolve(Path('/foo/my_table.py'))

        self.assertEqual('datalakebundle.notebook.scriptPathTemplate doesn\'t match real notebook path', str(cm.exception))

    def test_onePlaceholderDifferentValues(self):
        tableConfigParser = TableConfigResolver(
            '{rootModulePath}/foo/{dbIdentifier}/{tableIdentifier}/{tableIdentifier}',
            Box({})
        )

        with self.assertRaises(Exception) as cm:
            tableConfigParser.resolve(Path('/foo/bar/mydatabase/my_table2/my_table.py'))

        self.assertEqual('Placeholder {tableIdentifier} matches different values from the real notebook path', str(cm.exception))

if __name__ == '__main__':
    unittest.main()
