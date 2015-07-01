from simplemysql import SimpleMysql

class LogDatabase:
    def __init__(self, **args):
        self.dbParams = args
        self.conn = SimpleMysql(\
                    host=args['host'], \
                    db=args['db'], \
                    user=args['user'], \
                    passwd=args['passwd'] \
                )

    def getParams(self):
        return self.dbParams

    def getConnection(self):
        return self.conn

    def insert(self, table, **params):
        print params
