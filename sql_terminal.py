from src.get_info import get_connection_info
from src.terminal import terminal
if __name__=='__main__':
    print('\n******************************* \u001b[32mSQL TERMINAL\u001b[0m *******************************')
    con = get_connection_info()
    terminal(con)