from simplemysql import SimpleMysql


class LogDatabase:

    def __init__(self, **keyVals):
        # saving database parameters
        self.dbParams = keyVals

        # table information
        self.tablePrefix = 'zipnish_'
        self.tables = ['spans', 'annotations']

        # connect to database
        self.db = SimpleMysql(
            host=keyVals['host'],
            db=keyVals['db'],
            user=keyVals['user'],
            passwd=keyVals['passwd'],
            keep_alive=keyVals['keep_alive']
        )

        self.__create_tables()

        if 'truncate_tables' in keyVals and keyVals['truncate_tables'] == True:
            self.truncateTables()

    def __create_tables(self):
        spans_table_query = "CREATE TABLE IF NOT EXISTS zipnish_spans " \
            "(span_id BIGINT NOT NULL, " \
            "parent_id BIGINT, " \
            "trace_id BIGINT NOT NULL, " \
            "span_name VARCHAR(255) NOT NULL, " \
            "debug SMALLINT NOT NULL, " \
            "duration BIGINT, " \
            "created_ts BIGINT);"

        span_id_index0 = "ALTER TABLE zipnish_spans ADD INDEX(span_id);"
        trace_id_index0 = "ALTER TABLE zipnish_spans ADD INDEX(trace_id);"
        span_name_index0 = "ALTER TABLE zipnish_spans ADD INDEX(span_name(64));"
        created_ts_index = "ALTER TABLE zipnish_spans ADD INDEX(created_ts);"

        annotations_table_query = "CREATE TABLE IF NOT EXISTS zipnish_annotations " \
            "(span_id BIGINT NOT NULL, " \
            "trace_id BIGINT NOT NULL, " \
            "span_name VARCHAR(255) NOT NULL, " \
            "service_name VARCHAR(255) NOT NULL, " \
            "value TEXT, " \
            "ipv4 INT, " \
            "port INT, " \
            "a_timestamp BIGINT NOT NULL, " \
            "duration BIGINT);"

        span_id_key = "ALTER TABLE zipnish_annotations ADD FOREIGN KEY(span_id) " \
                      "REFERENCES zipnish_spans(span_id) ON DELETE CASCADE;"
        trace_id_indx = "ALTER TABLE zipnish_annotations ADD INDEX(trace_id);"
        span_name_index = "ALTER TABLE zipnish_annotations ADD INDEX(span_name(64));"
        value_index = "ALTER TABLE zipnish_annotations ADD INDEX(value(64));"
        a_timestamp_index = "ALTER TABLE zipnish_annotations ADD INDEX(a_timestamp);"

        queryes = [spans_table_query, span_id_index0, trace_id_index0,
                   span_name_index0, created_ts_index,
                   annotations_table_query, span_id_key, trace_id_indx,
                   span_name_index, value_index, a_timestamp_index]

        stmt = "SHOW TABLES LIKE 'zipnish_%'"
        cursor = self.db.query(stmt)
        table_count = len(cursor.fetchall())

        if table_count == 0:
            for query in queryes:
                self.db.query(query)

            self.db.commit()

    def getParams(self):
        return self.dbParams

    def getDB(self):
        return self.conn

    def insert(self, tableName, rows):
        table = self.tablePrefix + tableName
        if len(rows) > 0:
            for row in rows:
                self.db.insert(table, row)
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
