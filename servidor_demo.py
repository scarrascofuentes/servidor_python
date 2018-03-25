import socket
import os
import json

print("Servidor HTTP\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9100))
s.listen(1)

while True:

    client_connection, client_address = s.accept()
    request = client_connection.recv(1024)
    request_lines = request.split("\r\n")
    request_line_0 = request_lines[0]
    items_line_0 = request_line_0.split(" ")
    request_path = items_line_0[1]
    filesystem_path = "./documentRoot/%s" % request_path

    # RUTAS
    #print(request_path)
    #print(filesystem_path)

    #diccionario
    headers = {}
    i=1
    if os.path.isfile(filesystem_path):

        # se abren los archivos HTML
        archivo = open(filesystem_path, "r")

        client_connection.sendall("HTTP/1.1 200 OK\r\n".encode())
        client_connection.sendall("X-RequestEcho: %s\r\n\r\n".encode() % request_echo_json)
        print(client_connection.send("HTTP/1.1 200 OK \r\n\r\n".encode()))
        print(client_connection.send("X-RequestEcho: %s\r\n\r\n".encode() % request_echo_json))
        client_connection.sendall("CONTENIDO: \n\r %s\n\r\n\r".encode() % archivo.read())

        archivo.close()

    else:
        print("404 archivo invalido")
        client_connection.sendall("HTTP/1.1 404 Not Found :'( ".encode())

    while request_lines[i]:

        lista_headers = request_lines[i]
        nombre_header, valor_header = lista_headers.split(":", 1)

        headers[nombre_header] = valor_header

        request_echo_header = {}
        request_echo_header["method"] = items_line_0[0]
        request_echo_header["headers"] = headers
        #print(request_echo_header)
        #print(request_line_0)
        request_echo_json = json.dumps(request_echo_header)
        print(request_echo_json)
        i = i+1



    client_connection.close()
