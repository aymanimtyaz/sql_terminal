def execute_from_file(curs, argument):
    sql = open(argument).read()
    print('EXECUTING FROM FILE...\n')
    print(sql, '\n')
    curs.execute(sql)
    print(curs.statusmessage)
    curs.close()