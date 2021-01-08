import psycopg2 as pg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from getpass import getpass

class connection:

    def __init__(self, database, user, password, iso_level, host = 'localhost', port = '5432'):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.iso_level = iso_level
        self.con = pg2.connect(database = self.database, host = self.host, port = self.port, user = self.user, 
                               password = self.password, application_name = 'sql-terminal')
        if self.iso_level == 'y':
            self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def close_con(self):
        self.con.close()

def exit_routine(conn):
    conn.close_con()
    print('\n')
    import sys
    sys.exit(0)

def get_connection_info():

    print('\n******************************* SQL TERMINAL *******************************')
    host = input('Enter host (default: localhost): ')
    port = input('Enter port (default: 5432): ')
    dbname = ''; usr = ''; pw = ''; isolation_bool = ''
    while True:
        dbname = input('Enter database name: ')
        if dbname != '':
            break
    while True:
        usr = input('Enter user: ')
        if usr != '':
            break
    while True:
        pw = getpass('Enter password: ')
        if pw != '':
            break
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
    print(f'Connected to database {conn.database} on {conn.host}:{conn.port}\n')
    while True:
        try:
            sql = input(f'{conn.user}@{conn.database}-$ ')
            curs.execute(sql)
            print(curs.statusmessage)
            res = curs.fetchall()
            for row in res:
                print(row)
        except KeyboardInterrupt:
            exit_routine(conn)
        except Exception as e:
            if str(e) == 'no results to fetch':
                continue
            print('ERROR: ', e)
            if conn.iso_level == 'n':
                conn.con.rollback()

if __name__=='__main__':
    con = get_connection_info()
    terminal(con)




