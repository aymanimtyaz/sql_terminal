from getpass import getpass
import json, sys, os

def get_ssh_info():
    for argument in sys.argv[1:]:
        if os.path.splitext(argument)[1] == '.json':
            credentials = json.loads(open(argument).read())
            ssh_host = credentials['ssh_host']
            ssh_port = credentials['ssh_port']
            ssh_username = credentials['ssh_username']
            ssh_password = credentials['ssh_password']
            ssh_private_key = credentials['ssh_pkey']
            if ssh_password == '':
                ssh_password = None
            if ssh_private_key == '':
                ssh_private_key = None
            print("\u001b[33mSSH hostname/ip:\u001b[0m", ssh_host)
            print("\u001b[33mSSH port:\u001b[0m", ssh_port)
            print("\u001b[33mSSH username:\u001b[0m", ssh_username)
            print('\n')
            return ssh_host, ssh_port, ssh_username, ssh_password, ssh_private_key
    while True:
        ssh_host = input("Enter the hostname/ip address of the SSH gateway: ")
        if ssh_host != '':
            break
    ssh_port = input("Enter the port to access the SSH gateway (default 22): ")
    if ssh_port == '':
        ssh_port = 22
    while True:
        ssh_username = input("Enter the username to log into the SSH gateway as: ")
        if ssh_username != '':
            break
    ssh_password = getpass("Enter the password if authenticating with a password: ")
    if ssh_password == '':
        ssh_password = None
    ssh_private_key = input("Enter the filename of the private key file (if in the same directory) or its filepath if authenticating with a private key: ")
    if ssh_private_key == '':
        ssh_private_key = None
    return ssh_host, ssh_port, ssh_username, ssh_password, ssh_private_key

def get_db_info():
    creds_obtained = False
    for argument in sys.argv[1:]:
        if os.path.splitext(argument)[1] == '.json':
            credentials = json.loads(open(argument).read())
            host = credentials["host"]
            port = credentials["port"]
            dbname = credentials["database"]
            usr = credentials["username"]
            pw = credentials["password"]
            isolation_bool = credentials["autocommit"]
            print("\u001b[33mhostname/ip:\u001b[0m", host)
            print("\u001b[33mport:\u001b[0m", port)
            print("\u001b[33mdatabase:\u001b[0m", dbname)
            print("\u001b[33musername:\u001b[0m", usr)
            print("\u001b[33mautocommit:\u001b[0m", isolation_bool)
            print('\n')
            creds_obtained = True
            break
    if not creds_obtained:
        host = input('Enter host (default: localhost): ')
        if host == '':
            host = 'localhost'
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
    hostname, dbport, dbname, usr, pw, isolation_bool = get_db_info()
    while True:
        ssh_mode = input('Would you like to connect through an SSH tunnel? (y/n): ')
        if ssh_mode == 'y' or ssh_mode == 'n':
            if ssh_mode =='n':
                from src.connections import connection
                con = connection(database = dbname, user = usr, password = pw, iso_level = isolation_bool, host = hostname, port = dbport)
                return con
            else:
                from src.connections import ssh_con
                ssh_host, ssh_port, ssh_username, ssh_password, ssh_private_key = get_ssh_info()
                con = ssh_con(database = dbname, user = usr, password = pw, iso_level = isolation_bool, ssh_host = ssh_host,
                              ssh_port = ssh_port, ssh_username = ssh_username, ssh_password = ssh_password, ssh_private_key = ssh_private_key,
                              host = hostname, port = dbport)
                return con

    