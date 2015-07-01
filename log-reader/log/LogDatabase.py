from simplemysql import SimpleMysql

class LogDatabase:
    def __init__(self, **args):
        self.dbParams = args

    def getParams(self):
        return self.dbParams
