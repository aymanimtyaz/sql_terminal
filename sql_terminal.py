import psycopg2 as pg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from getpass import getpass
import sys, os, json
from tabulate import tabulate

hostname = ''
dbport = ''
ssh_connection = None

class ssh_con:

    def __init__(self, host, port, user, password = None, private_key = None, remote_bind_address = None):
        import sshtunnel
        from sshtunnel import SSHTunnelForwarder as stf
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.private_key = private_key
        self.remote_bind_address = remote_bind_address
        self.tunnel = stf(ssh_address_or_host = self.host, ssh_port = self.port, ssh_username = self.user, ssh_pkey = self.private_key,
             remote_bind_address = self.remote_bind_address)
        self.tunnel.start()
        print(f'SSH connection established to \u001b[32m{self.host}:\u001b[36m{self.port}\u001b[0m')

    def disconnect_ssh(self):
        self.tunnel.close()

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

def establish_ssh_tunnel():
    global ssh_connection
    if len(sys.argv) > 1:
        for argument in sys.argv[1:]:
            if os.path.splitext(argument)[1] == '.json':
                with open(argument) as config_json:
                    config = json.loads(config_json.read())
                    host = config['ssh_host']
                    port = config['ssh_port']
                    user = config['ssh_username']
                    password = config['ssh_password']
                    if password == "":
                        password = None
                    private_key = config["ssh_pkey"]
                    remote_host = config['host']
                    remote_port = int(config['port'])
                    remote_bind_address = (remote_host, remote_port)
                    ssh_connection = ssh_con(host, port, user, password, private_key, remote_bind_address)
                    return ssh_connection
    global hostname; global dbport
    while True:
        host = input("Enter the hostname/ip of the server to SSH to: ")
        if host != '':
            break
    port = input("Enter port of the server to SSH to (default 22): ")
    if port == '':
        port = 22
    while True:
        user = input("Enter the username to SSH in as: ")
        if user != '':
            break
    password = input("Enter the password if required: ")
    if password == '':
        password = None
    private_key = input("Enter the path to the private key if using a private key: ")
    if private_key == '':
        private_key = None
    remote_bind_address = (hostname, int(dbport))
    ssh_connection = ssh_con(host, port, user, password, private_key, remote_bind_address)
    return ssh_connection
             
def execute_from_file(curs, argument):
    sql = open(argument).read()
    print('EXECUTING FROM FILE...\n')
    print(sql, '\n')
    curs.execute(sql)
    print(curs.statusmessage)
    curs.close()

def exit_routine(conn):
    conn.close_con()
    global ssh_connection
    if ssh_connection is not None:
        ssh_connection.disconnect_ssh()
    print('\n') 
    sys.exit(0)

def get_from_cli_arguments(argument):
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
    if port == '':
        port = '5432'
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
    global hostname; global dbport

    print('\n******************************* \u001b[32mSQL TERMINAL\u001b[0m *******************************')
    creds_not_validated = True
    for argument in sys.argv[1:]:
        if os.path.splitext(argument)[1] == '.json':
            hostname, dbport, dbname, usr, pw, isolation_bool = get_from_cli_arguments(argument)
            creds_not_validated = False
            break
    if creds_not_validated:
        hostname, dbport, dbname, usr, pw, isolation_bool = get_interactive()

    ssh_mode = ''

    while True:
        ssh_mode = input('Would you like to connect through an SSH tunnel? (y/n): ')
        if ssh_mode == 'y' or ssh_mode == 'n':
            break

    if ssh_mode == 'y':
        ssh_tunnel = establish_ssh_tunnel()
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool, host = 'localhost', port = ssh_tunnel.tunnel.local_bind_port)
        return conn

    print('\nConnecting to database...')

    if hostname == '' and dbport == '':
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool)
    elif dbport == '' and hostname != '':
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool, host = hostname)
    elif hostname == '' and dbport != '':
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool, port = dbport)
    else:
        conn = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool, host = hostname, port = dbport)

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
            print(curs.statusmessage, '\n')
            res = curs.fetchall()
            print(tabulate(res, [desc[0] for desc in curs.description]), '\n')
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