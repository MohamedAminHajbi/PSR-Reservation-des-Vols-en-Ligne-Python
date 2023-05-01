while True:
    c, addr = s.accept()
    print('Connected with ', addr)

    d = "how can i help you?"
    msg = pickle.dumps(d)

    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg

    c.send(msg)