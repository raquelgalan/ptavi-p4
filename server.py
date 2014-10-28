#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#Raquel Galan Montes
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys
import time

dic_clientes = {}


class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """
    def register2file(self, dic_clientes):
        """
        Si un usuario se registra o se da de baja se imprime en registered.txt
        """
        fich = open("registered.txt", "w")
        fich.write("User\tIP\tExpires\r\n")

        for usuario in dic_clientes:
            ip = dic_clientes[usuario][0][0]
            tiemp = dic_clientes[usuario][1]
            valores = usuario + "\t" + ip + "\t" + tiemp + "\r\n"
            fich.write(valores)
        fich.close()

    def handle(self):
        """
        Escribe dirección y puerto del cliente (de tupla client_address)
        """
        #iteramos por el diccionario
        lista = []
        for usuario in dic_clientes.keys():
            print ("tiempo", time.time())
            print ("caducidad:", dic_clientes[usuario][2])
            if time.time() >= dic_clientes[usuario][2]:
                print("marco el usuario: ", usuario)
                lista.append(usuario)

        for usuario in lista:
            print("borrado:", usuario)
            del dic_clientes[usuario]

        print self.client_address
        self.wfile.write("Hemos recibido tu peticion ")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            text = self.rfile.read()
            if text != "":
                print "El cliente nos manda " + text
                mensaje = text.split()
                metodo = mensaje[0]
                email = mensaje[1].split(":")[1]
                print int(mensaje[4])
                expires_value = int(mensaje[4])
                cad_regist = time.time() + expires_value
                print ("tiempo", time.time())
                print ("caducidad:", cad_regist)

                if metodo == "REGISTER":
                    self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
                    t = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                    dic_clientes[email] = [self.client_address, t, cad_regist]
                    self.register2file(dic_clientes)
                    if expires_value == 0:
                        del dic_clientes[email]
                        self.wfile.write("SIP/1.0 200 OK\r\n\r\n")
                        self.register2file(dic_clientes)
            else:
                break
        print dic_clientes

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
