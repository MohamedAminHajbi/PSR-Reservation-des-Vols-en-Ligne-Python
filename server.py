import socket


s = socket.socket()
print('Socket Created')

s.bind(('localhost', 9999))
s.listen(3)
print('Waiting for clients')

while True:
    c, addr = s.accept()
    name = c.recv(1024).decode()
    print('Connected with ', addr, name)

    msg = "Welcome to the server!"
    print(f'{len(msg):<10}' + msg)

    c.send(bytes('Welcome to the Gulag '+name, 'utf-8'))
    c.close()
