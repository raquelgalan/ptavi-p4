#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#Raquel Galan Montes
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
SERVER = sys.argv[1]

PORT = int(sys.argv[2])

# Contenido que vamos a enviar
LINE = sys.argv[3]

CORREO = sys.argv[4]

# Si el cliente se ejecuta con register
if LINE == "register":
    text = "REGISTER sip:" + CORREO + " SIP/1.0\r\n\r\n"
else:
    text = ""

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print "Enviando: " + text
my_socket.send(text + '\r\n')
data = my_socket.recv(1024)

print 'Recibido -- ', data
print "Terminando socket..."

# Cerramos todo
my_socket.close()
print "Fin."
