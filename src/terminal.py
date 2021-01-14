import sys, os
from src.connections import exit_routine
from src.execute_from_file import execute_from_file
from tabulate import tabulate

def terminal(conn):
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