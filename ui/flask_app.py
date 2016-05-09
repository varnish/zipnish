import ConfigParser

from app import create_app


def main():
    etc_config_path = '/etc/zipnish/zipnish.cfg'
    config = ConfigParser.ConfigParser()
    config.read(etc_config_path)

    host = config.get('Database', 'host')
    db = config.get('Database', 'db_name')
    user = config.get('Database', 'user')
    passwd = config.get('Database', 'pass')
    db_port = 3306

    db_dialect = "mysql+mysqldb://{}:{}@{}:{}/{}". \
        format(user, passwd, host, db_port, db)

    app = create_app(db_dialect)
    app.run()

if __name__ == '__main__':
    main()
