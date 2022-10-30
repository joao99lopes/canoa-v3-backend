class DBConfig():
    #DB_USER = 'read_only_dev'
    #DB_PASSWORD = '64mXtiKtwUgJYe2B'
    DB_USER = 'postgres'
    DB_PASSWORD = 'postgres'
    DB_ADDRESS = 'postgres-db'
    DB_NAME = 'scoutify_db'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'
