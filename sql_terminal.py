import psycopg2 as pg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from getpass import getpass

class connection:

    def __init__(self, database, user, password, iso_level, host = 'localhost', port = '5432'):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.iso_level = iso_level
        self.con = pg2.connect(database = self.database, host = self.host, user = self.user, password = self.password)
        if self.iso_level == 'y':
            self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def close_con(self):
        self.con.close()


def get_connection_info():

    print('\n******************************* SQL TERMINAL *******************************')
    dbname = input('Enter database name: ')
    host = input('Enter host: ')
    port = input('Enter port: ')
    usr = input('Enter user: ')
    pw = getpass('Enter password: ')
    isolation_bool = ''
    while True:
        isolation_bool = input('Run with autocommit? (y/n): ')
        if isolation_bool == 'y' or isolation_bool == 'n':
            break
    print('\nConnecting to database...')

    if host == '' and port == '':
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool)
    elif port == '' and host != '':
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool, host = host)
    elif host == '' and port != '':
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool, port = port)
    else:
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool, host = host, port = port)

    return conn

def terminal(conn):
    curs = conn.con.cursor()
    print(f'Connected to database {conn.database} on {conn.host}')
    while True:
        sql = input(f'\n{conn.user}@{conn.database}-$ ')
        curs.execute(sql)
        res = curs.fetchall()
        for row in res:
            print(row)

if __name__=='__main__':
    con = get_connection_info()
    terminal(con)




