import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 7777))

data = s.recv(1024)

file = open('robux-hack.bat', 'wb')

file.write(data)

file.close()
