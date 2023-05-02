import socket
import select
import vols_manager

HEADER_LENGTH = 10
IP = "192.168.95.131"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]

clients = {}


def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(
        sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print(
                f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:   
                while True:
                    message = receive_message(notified_socket)
                    if message is False:
                        print(
                            f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                        sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                        continue
                    user = clients[notified_socket]
                    if message['data'].decode('utf-8') == "Reservation":
                        msg = receive_message(notified_socket)
                        print(
                            f"Received message from {user['data'].decode('utf-8')} : {msg['data'].decode('utf-8')}")
                        request = msg['data'].decode('utf-8').split(' ')
                        print(request)
                        reservation_successful, crendu = vols_manager.GestionnaireVols().reserver(
                            request[0], request[1], request[2], int(request[3]))
                        notified_socket.send(
                            user['header'] + user['data'] + message['header'] + bytes(crendu, 'utf-8'))
                        request = []
                    elif message['data'].decode('utf-8') == "Facturation":
                        notified_socket.send(user['data']+ vols_manager.GestionnaireVols().getFacture(user['data']))
                    elif message['data'].decode('utf-8') == "Historique":
                        notified_socket.send(vols_manager.GestionnaireVols.getHisto(user['data']))
                    elif message['data'].decode('utf-8') == "Exit":
                        break
                    else:
                        notified_socket.send("Message inconnu")
                        continue
                for client_socket in clients:
                        if client_socket != notified_socket:
                            client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]