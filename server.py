#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#Raquel Galan Montes
"""
Clase (y programa principal) para un servidor de eco
en UDP simple
"""

import SocketServer
import sys

diccionario_clientes = {}
class SIPRegisterHandler(SocketServer.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print self.client_address
        self.wfile.write("Hemos recibido tu peticion ")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            text = self.rfile.read()
            if text != "":
                print "El cliente nos manda " + text
                mensaje = text.split()
                metodo = mensaje[0]
                email = mensaje[1]
                expires_value = int(mensaje[4])

                
                if metodo == "REGISTER":
                    self.wfile.write ("SIP/1.0 200 OK\r\n\r\n")
                    diccionario_clientes[email] = self.client_address
                       
                    
                if expires_value == 0:
                    del diccionario_clientes[email]
                    self.wfile.write ("SIP/1.0 200 OK\r\n\r\n")    
                    
            else:
                break
            

        print diccionario_clientes


           
        

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = SocketServer.UDPServer(("", PORT), SIPRegisterHandler)
    print "Lanzando servidor UDP de eco..."
    serv.serve_forever()
