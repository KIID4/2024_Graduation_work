
def receive_data(client_socket, length):
    data = b''
    while len(data) < length:
        packet = client_socket.recv(min(length - len(data), 1024))
        if not packet:
            break
        data += packet
    return data