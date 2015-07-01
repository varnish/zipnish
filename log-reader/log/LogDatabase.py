from simplemysql import SimpleMysql

class LogDatabase:
    def __init__(self, **keyVals):
        # saving database parameters
        self.dbParams = keyVals

        # table information
        self.tablesPrefix = 'zipkin_'
        self.tables = ['spans', 'annotations']

        # connect to database
        self.db = SimpleMysql(\
                    host=keyVals['host'], \
                    db=keyVals['db'], \
                    user=keyVals['user'], \
                    passwd=keyVals['passwd'], \
                    keep_alive=keyVals['keep_alive'] \
                )

        if 'truncate_tables' in keyVals:
            self.truncateTables()

    def getParams(self):
        return self.dbParams

    def getDB(self):
        return self.conn

    def insert(self, table, **params):
        print params

    # truncate data in tables related to our application
    def truncateTables(self):
        print 'Truncating tables'

        if self.db is not None and self.db.is_open():
            for tableName in self.tables:
                print 'truncating table: ' + table

                # table prefix + table name
                table = self.tablesPrefix + tableName

                # delete table, and commit changes to database
                self.db.delete(table)
                self.db.commit()
