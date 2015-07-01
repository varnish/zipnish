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

    def insert(self, table, rows):
        print "Table: " + table
        print rows

    # truncate data in tables related to our application
    def truncateTables(self):
        print 'Truncating Tables:'

        if self.db is not None and self.db.is_open():
            for tableName in self.tables:
                # table prefix + table name
                table = self.tablesPrefix + tableName

                print 'truncating table -> ' + table

                # delete table, and commit changes to database
                self.db.delete(table)
                self.db.commit()
