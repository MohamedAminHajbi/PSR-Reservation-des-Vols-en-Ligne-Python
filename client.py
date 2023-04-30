import socket
import pickle
HEADERSIZE = 10
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((socket.gethostname(), 1235))
while True:
    full_msg = b''
    new_msg = True
    while True:
        msg = c.recv(16)
        if new_msg:
            print(f"new message length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_msg += msg
        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recieved")
            print(full_msg[HEADERSIZE:])
            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)

            new_msg = True
            full_msg = b''

    print(full_msg)
