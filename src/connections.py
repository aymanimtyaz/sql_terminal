import psycopg2 as pg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

class connection:

    def __init__(self, database, user, password, iso_level, host = 'localhost', port = '5432'):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.iso_level = iso_level
        print('Connecting to database...')
        self.con = pg2.connect(database = self.database, host = self.host, port = self.port, user = self.user, 
                               password = self.password, application_name = 'sql-terminal')
        print(f'Connected to database \u001b[31m{self.database}\u001b[0m on \u001b[36m{self.host}:\u001b[33m{self.port}\u001b[0m\n')
        if self.iso_level == 'y':
            self.con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def close_con(self):
        self.con.close()

class ssh_con(connection):

    def __init__(self, database, user, password, iso_level, ssh_host, ssh_port, ssh_username, ssh_password = None,
                 ssh_private_key = None, host = 'localhost', port = '5432'):
        import sshtunnel
        from sshtunnel import SSHTunnelForwarder as stf 
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_user = ssh_username
        self.ssh_password = ssh_password
        self.ssh_private_key = ssh_private_key
        self.remote_bind_address = (host, int(port))
        print('Establishing SSH connection...')
        self.tunnel = stf(ssh_address_or_host = self.ssh_host, ssh_port = self.ssh_port, ssh_username = self.ssh_user, ssh_password = self.ssh_password, 
                          ssh_pkey = self.ssh_private_key, remote_bind_address = self.remote_bind_address)
        self.tunnel.start()
        print(f'SSH connection established to \u001b[32m{self.ssh_host}:\u001b[36m{self.ssh_port}\u001b[0m\n')
        super().__init__(database = database, user = user, password = password, iso_level = iso_level, host = 'localhost', port = self.tunnel.local_bind_port)

    def close_con(self):
        super().close_con()
        self.tunnel.close()

def exit_routine(conn):
    conn.close_con()
    print('\n')
    sys.exit(0)

