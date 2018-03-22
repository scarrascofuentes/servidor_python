import socket
import os
import json

print("Servidor HTTP")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9100))
s.listen(1)

while True:

    client_connection, client_address = s.accept()
    request = client_connection.recv(1024)
    #print(request)
    request_lines = request.split("\r\n")
    #print(request_lines)
    request_line_0 = request_lines[0]
    #print(request_line_0)
    items_line_0 = request_line_0.split(" ")
    #print(items_line_0)
    request_path = items_line_0[1]
    filesystem_path = "./documentRoot/%s" % request_path

    print(request_path)
    print(filesystem_path)

    #diccionario
    headers = {}
    i=1
    while request_lines[i]:

        primer_header = request_lines[i]
        nombre_header, valor_header = primer_header.split(":", 1)
        #print(nombre_header)
        #print(valor_header)

        headers[nombre_header] = valor_header
        #print(headers)

        request_echo_header = {}
        request_echo_header["method"] = items_line_0[0]
        request_echo_header["headers"] = headers
        #print(request_echo_header)
        request_echo_json = json.dumps(request_echo_header)
        print(request_echo_json)
        i = i+1

    if os.path.isfile(filesystem_path):

        client_connection.sendall("HTTP/1.1 200 OK\r\n".encode())
        client_connection.sendall("X-RequestEcho: %s\r\n\r\n".encode() % request_echo_json)
        client_connection.sendall("CONTENIDO!! : ".encode())
    else:
        print("404 archivo invalido")
        client_connection.sendall("HTTP/1.1 404 Not Found".encode())

    client_connection.close()
