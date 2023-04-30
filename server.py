import socket
import time
import pickle


HEADERSIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket Created')

s.bind((socket.gethostname(), 1235))
s.listen(3)
print('Waiting for clients')

while True:
    c, addr = s.accept()
    print('Connected with ', addr)

    d = {1: "Hey", 2: "There"}
    msg = pickle.dumps(d)

    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg

    c.send(msg)
