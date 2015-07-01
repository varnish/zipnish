from simplemysql import SimpleMysql

class LogDatabase:
    def __init__(self, **keyVals):
        # saving database parameters
        self.dbParams = keyVals

        # table information
        self.tablesPrefix = 'zipkin_'
        self.tables = ['spans', 'annotations']

        # connect to database
        self.conn = SimpleMysql(\
                    host=keyVals['host'], \
                    db=keyVals['db'], \
                    user=keyVals['user'], \
                    passwd=keyVals['passwd'] \
                )

        if 'truncateTables' in keyVals:
            self.truncateTables()

    def getParams(self):
        return self.dbParams

    def getConnection(self):
        return self.conn

    def insert(self, table, **params):
        print params

    # truncate data in tables related to our application
    def truncateTables(self):
        if self.conn is not None:
            for tableName in self.tables:
                self.conn.delete(self.tablesPrefix + tableName)
