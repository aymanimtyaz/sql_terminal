import psycopg2 as pg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from getpass import getpass
import sys, os

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

def execute_from_file(curs, argument):
    sql = open(argument).read()
    print('EXECUTING FROM FILE...\n')
    print(sql, '\n')
    curs.execute(sql)
    print(curs.statusmessage)
    curs.close()

def exit_routine(conn):
    conn.close_con()
    print('\n') 
    sys.exit(0)

def get_from_cli_arguments(argument):
    import json
    credentials = json.loads(open(argument).read())
    host = credentials["host"]
    port = credentials["port"]
    dbname = credentials["database"]
    usr = credentials["username"]
    pw = credentials["password"]
    isolation_bool = credentials["autocommit"]
    print("\u001b[33mhost:\u001b[0m", host)
    print("\u001b[33mport:\u001b[0m", port)
    print("\u001b[33mdatabase:\u001b[0m", dbname)
    print("\u001b[33musername:\u001b[0m", usr)
    print("\u001b[33mautocommit:\u001b[0m", isolation_bool)
    return host, port, dbname, usr, pw, isolation_bool

def get_interactive():
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
    
    return host, port, dbname, usr, pw, isolation_bool

def get_connection_info():

    print('\n******************************* \u001b[32mSQL TERMINAL\u001b[0m *******************************')
    creds_not_validated = True
    for argument in sys.argv[1:]:
        if os.path.splitext(argument)[1] == '.json':
            host, port, dbname, usr, pw, isolation_bool = get_from_cli_arguments(argument)
            creds_not_validated = False
            break
    if creds_not_validated:
        host, port, dbname, usr, pw, isolation_bool = get_interactive()

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
    print(f'Connected to database \u001b[31m{conn.database}\u001b[0m on \u001b[36m{conn.host}:\u001b[33m{conn.port}\u001b[0m\n')
    curs = conn.con.cursor()
    if len(sys.argv) > 1:
        for argument in sys.argv[1:]:
            if os.path.splitext(argument)[1] == ('.sql' or '.txt'):
                execute_from_file(curs, argument)
                exit_routine(conn)
    while True:
        try:
            sql = input(f'\u001b[32m{conn.user}\u001b[37m@\u001b[34m{conn.database}-\u001b[0m$ ')
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
            print('\u001b[31mERROR: \u001b[0m', e)
            if conn.iso_level == 'n':
                conn.con.rollback()

if __name__=='__main__':
    con = get_connection_info()
    terminal(con)