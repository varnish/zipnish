from simplemysql import SimpleMysql

class LogDatabase:
    def __init__(self, **keyVals):
        # saving database parameters
        self.dbParams = keyVals

        # table information
        self.tablePrefix = 'zipnish_'
        self.tables = ['spans', 'annotations']

        # connect to database
        self.db = SimpleMysql(\
                    host=keyVals['host'], \
                    db=keyVals['db'], \
                    user=keyVals['user'], \
                    passwd=keyVals['passwd'], \
                    keep_alive=keyVals['keep_alive'] \
                )

        if 'truncate_tables' in keyVals and keyVals['truncate_tables'] == True:
            self.truncateTables()

    def getParams(self):
        return self.dbParams

    def getDB(self):
        return self.conn

    def insert(self, tableName, rows):
        table = self.tablePrefix + tableName
        if len(rows) > 0:
            for row in rows:
                self.db.insert(table, row);
            self.db.commit()

    # truncate data in tables related to our application
    def truncateTables(self):
        print 'Truncating Tables:'

        if self.db is not None and self.db.is_open():
            for tableName in self.tables:
                # table prefix + table name
                table = self.tablePrefix + tableName

                print 'truncating table -> ' + table

                # delete table, and commit changes to database
                self.db.delete(table)
                self.db.commit()
