#!/usr/bin/python3

"""
Simple HTTP Server
Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket
import random

# Create a TCP objet socket and bind it to a port
# We bind to 'localhost', therefore only accepts connections from the
# same machine
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

num1 = None;
suma = None;

# Accept connections, read incoming data, and answer back an HTML page
#  (in an infinite loop)

try:
	while True:
	    
	    print('Waiting for connections')
	    (recvSocket, address) = mySocket.accept()
	    print('HTTP request received:')

	    info_recibida = recvSocket.recv(2048).decode('utf-8', 'strict')
	    print(info_recibida)
	    try:
	    	if(num1 == None):
	    		num1 = int(info_recibida.split(' ')[1][1:])
	    		if(num1 == "favicon.ico"):
	    			recvSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1> Not Found </h1></body></html>\r\n", 'utf-8'))
	    			recvSocket.close()	
	    			num1 = None
	    		html = "<html><body> El primer sumando es: " + str(num1) + "<p>Introduce otro sumando para realizar la suma.</p></body></html>" 
	    	elif(num1 != None ):
	    		num2 = int(info_recibida.split(' ')[1][1:])
	    		html = "<html><body> Tu primer sumando es: " + str(num1)
	    		html += "<p> El segundo sumando es: " + str(num2) + "</p>" 
	    		suma = num1 + num2
	    		html += "<p>La suma de tus get es: " + str(suma) + "</p></body></html>"
	    		num1 = None
	    		suma = None

	    except ValueError:
	    	recvSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n<html><body><h1> No me has dado un numero. intenta de nuevo </h1></body></html>\r\n", 'utf-8'))
	    	recvSocket.close()
	    	num1 = None
	    	continue

	    recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n" + html  + "\r\n", 'utf-8'))
	    recvSocket.close()

except KeyboardInterrupt:
	mySocket.close()
	print ("Closing binding socket...")
