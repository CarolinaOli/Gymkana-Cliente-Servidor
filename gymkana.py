#!/usr/bin/python3

## PRACTICA GYMKANA
## REDES II - 2015 - 2016
## JOSUE GUTIERREZ DURAN
## 2ºB
## ESCUELA SUPERIOR DE INFORMATICA

###################
#	          #
#  IMPORTACIONES  #
#	          #
###################

from socket import *
import urllib.request
import struct
import time
import os
import _thread

###############
#	      #
#  VARIABLES  #
#	      #
###############

host_uclm = 'atclab.esi.uclm.es' #HOST DE LA GYMKANA
puerto1_uclm = 2000 #PUERTO 1 DE LA GYMKANA
puerto2_uclm = 1985 #PUERTO 2 DE LA GYMKANA
puerto3_uclm = 5000 #PUERTO 3 DE LA GYMKANA
puerto4_uclm = 9000 #PUERTO 4 DE LA GYMKANA
puerto_local = 1234 #PUERTO SERVIDOR LOCAL


###############
#	      #
#  FUNCIONES  #
#	      #
###############

# FUNCION SOCKET TCP CLIENTE
def socketTCP_Client (host, puerto):
    sock = socket(AF_INET, SOCK_STREAM) # Creacion del Socket TCP
    sock.connect((host, puerto)) # Conexion

    return sock
# FIN FUNCION SOCKET TCP


# FUNCION SOCKET TCP SERVIDOR
def socketTCP_Server (puerto):
    sock = socket(AF_INET, SOCK_STREAM) # Creacion del Socket TCP
    sock.bind(('', puerto)) # Creacion del Servidor

    return sock
# FIN FUNCION SOCKET TCP SERVIDOR


# FUNCION SOCKET UDP SERVIDOR
def socketUDP_Server (puerto):
    sock = socket(AF_INET, SOCK_DGRAM) #C reacion del Socket UDP
    sock.bind(('', puerto)) # Creacion del Servidor

    return sock
# FIN FUNCION SOCKET UDP SERVIDOR


# FUNCION PASO 0
def paso0 (host, puerto):
    print('\n**** PASO 0 ****') # CABECERA

    sock0 = socketTCP_Client(host, puerto) # Socket TCP
    message = sock0.recv(2048).decode() # Recepcion del mensaje y decodificacion
    print(message) # Impresion del mensaje
    sock0.close() # Cierre de la conexion

    return message[:5] # Se devuelve el Identificador
# FIN FUNCION PASO 0


# FUNCION PASO 1
def paso1 (identificador, puerto_local, host, puerto):
    print('\n**** PASO 1 ****') # CABECERA
    print('Identificador Etapa 0: ', identificador, '\n') # IDENTIFICADOR

    sock1 = socketUDP_Server(puerto_local) # Socket UDP
    message_in = str(identificador) + ' '+ str(puerto_local) # Construccion del Mensaje
    sock1.sendto(message_in.encode(),(host, puerto)) # Envio del mensaje

    message_out = sock1.recv(2048).decode() # Recepcion del mensaje y decodificacion
    print(message_out) # Impresion del mensaje
    sock1.close() # Cierre de la conexion

    return message_out[:5] # Se devuelve el Identificador
# FIN FUNCION PASO 1


# FUNCION RESOLVER EXPRESION
# FUNCION MEJORABLE - LA MEJORARE AL TERMINAR EL ULTIMO PASO
def resolver (cadena):

    parentesis_a = 0
    num1a = ''
    num2a = ''
    num1 = 0
    num2 = 0
    simbolo = ''
    neg_num1 = False
    neg_num2 = False

    if cadena[0] == '(' and cadena[-1] == ')' :
        cadena = cadena[1:-1]
              
    reset = False
    pos_act = 0

    while pos_act < len(cadena):
        actual = cadena[pos_act]
        if actual == '(' :

            temp = pos_act
            newcadena = ''

            while cadena[temp] != ')' or parentesis_a > 1 :     
                newcadena += cadena[temp]
                if cadena[temp] == '(':
                    parentesis_a += 1
                elif cadena[temp] == ')':
                    parentesis_a -= 1
                temp += 1

            parentesis_a = 0
            newcadena += ')'

            sol = resolver(newcadena)
            cadena = cadena.replace(newcadena, sol)         
            reset = True            

            num1a=''
            num2a=''

        if actual.isdigit() or actual == '.' :
            if simbolo == '' :
                num1a += actual
  				
            else:
                num2a += actual
   	
        elif cadena[(pos_act+1)] == '-' :
                neg_num2 = True
                simbolo = actual
        elif actual == '-' and num1a == '':
            neg_num1 = True
        else:
            if simbolo == '':
                simbolo = actual
            
        if reset:
            num1a=''
            num2a=''
            simbolo = ''
            pos_act = 0
            reset = False
        else:        
            pos_act += 1
            
    if neg_num1:
        num1a = '-'+num1a
        num1a = num1a.replace(" ", "") #Eliminacion de espacios en blanco
    if neg_num2 :
        num2a = '-'+num2a  
        num2a = num2a.replace(" ", "") #Eliminacion de espacios en blanco
         
    num1 = (float(num1a))  
    num2 = (float(num2a))
    resul= ''

    if simbolo == '+':
        resul = "{0:.2f}".format(num1+num2)
    elif simbolo == '*':
        resul = "{0:.2f}".format(num2*(num1))
    elif simbolo == '/':
        resul= str(int(num1//num2))+'.00'
    elif simbolo == '-':
        resul = "{0:.2f}".format(num1-num2)

    if resul == '-0.00':
        resul = '0.00'
    return resul
# FIN FUNCION RESOLVER EXPRESION


# FUNCION PASO 2
def paso2 (host, clave):
	print('\n**** PASO 2 ****') # CABECERA
	print('Identificador Etapa 1: ', clave) # IDENTIFICADOR	

	sock2 = socketTCP_Client(host, int(clave)) # Socket TCP	

	expresion = sock2.recv(4096).decode() #Recepcion de la ecuacion

	parentesis_a = 0
	parentesis_c = 0

	for actual in expresion:
            if actual == '(':
                parentesis_a += 1
            if actual == ')':
                parentesis_c += 1
    
	if not parentesis_a==parentesis_c:
	    expresion += sock2.recv(4096).decode() # Recepcion de la ecuacion	

	expresion = expresion.replace(" ", "") # Eliminacion de espacios en blanco
	
	while expresion[0] == '(' : # Bucle que se repite mientras se reciban ecuaciones		
                expresion = expresion.replace(" ", "") #Eliminacion de espacios en blanco		
                print('Ecuacion a Resolver:', expresion) #Impresion de ecuacion

                sol = resolver(expresion)

                solucion = '('+sol[:-3]+')'
                print('Solucion: ', solucion) #Impresion de solucion
                sock2.sendto(solucion.encode(),(host, int(clave))) #Envio de la solucion
                expresion = sock2.recv(4096).decode() #Recepcion del mensaje y decodificacion

                parentesis_a = 0
                parentesis_c = 0

                for actual in expresion:
                    if actual == '(':
                        parentesis_a += 1
                    if actual == ')':
                        parentesis_c += 1
    
                if not parentesis_a==parentesis_c:                
                    expresion += sock2.recv(4096).decode() #Recepcion de la ecuacion

	print('\n', expresion) # Impresion del mensaje
	sock2.close() # Cierre de la conexion

	return expresion[:5] # Se devuelve el Identificador
# FIN FUNCION PASO 2


# FUNCION PASO 3
def paso3(host, puerto, clave):
    print('\n**** PASO 3 ****') # CABECERA
    print('Identificador Etapa 2: ', clave) # IDENTIFICADOR	   

    message_in = 'http://' + host + ':' + str(puerto) + '/' + str(clave) # Creacion del mensaje

    with urllib.request.urlopen(message_in) as f: # Lectura del mensaje
        message_out = f.read(2048).decode('utf-8')

    print(message_out) # Impresion del mensaje

    return message_out[:5] # Se devuelve el Identificador
# FIN FUNCION PASO 3


# FUNCION CHECKSUM
def cksum(data):

    def sum16(data):
        "sum all the the 16-bit words in data"
        if len(data) % 2:
            data += '\0'.encode()

        return sum(struct.unpack("!%sH" % (len(data) // 2), data))

    retval = sum16(data)                       # sum
    retval = sum16(struct.pack('!L', retval))  # one's complement sum
    retval = (retval & 0xFFFF) ^ 0xFFFF        # one's complement
    return retval
# FIN FUNCION CHECKSUM


# FUNCION PASO 4
def paso4(host, clave):	
    print('\n**** PASO 4 ****') # CABECERA
    print('Identificador Etapa 3: ', clave) # IDENTIFICADOR	

    ICMP_ECHO_REQUEST = 8 # Variable ICMP
    checksum = 0 # Checksum Inicial
    proccess_id = os.getpid() # PID

    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, checksum, proccess_id, 1) # Creacion de la cabecera
    payload = struct.pack('!d', float(str(time.time())[:8])) + clave.encode() # Creacion de la carga

    message = header + payload # Composicion del mensaje

    header = struct.pack('!BBHHH', ICMP_ECHO_REQUEST, 0, cksum(message), proccess_id, 1) # Creacion de la cabecera
    
    message = header + payload # Composicion del mensaje

    sock4 = socket(AF_INET, SOCK_RAW, getprotobyname ("icmp")) # Socket ICMP
    sock4.sendto(message , (host, 2000)) # Envio del mensaje

    message = sock4.recv(2048) #Captura del mensaje
    message = sock4.recv(2048) #Captura del mensaje  
    message = (message[36:]).decode('utf-8') # Decodificacion del mensaje
    
    print(message) # Impresion del mensaje
    
    sock4.close() # Cierre del Socket
    
    return message[:5] # Se devuelve el Identificador
# FIN FUNCION PASO 4

# FUNCION SERVIDOR HTTP
def serverHTTP(sock):
    while 1: # Bucle Infinito
        child_sock, client = sock.accept() # Aceptacion del Socket
        _thread.start_new_thread(procesador, (child_sock, client)) # Nuevo hilo de procesamiento
# FIN FUNCION SERVIDOR HTTP


# FUNCION DE PROCESAMIENTO
def procesador(sock, client):

    message_out = sock.recv(1024) # Captura del Mensaje

    print(message_out.decode()) # Impresion del mensaje

    URL = (message_out.decode()).split(' ')[1] # Obtencion de la URL

    file_out = urllib.request.urlopen(URL) # Obtencion del Fichero

    message_in = file_out.read() # Captura del Mensaje del Fichero

    sock.send(message_in) # Envio del Mensaje

    file_out.close() # Cierre del archivo
    sock.close() # Cierre del Socket
# FIN FUNCION DE PROCESAMIENTO


# FUNCION PASO 5
def paso5(host, puerto, clave) :
    print('\n**** PASO 5 ****') # CABECERA
    print('Identificador Etapa 4: ', clave) # IDENTIFICADOR	
  
    sock_client = socketTCP_Client(host, puerto) # Socket TCP
    sock_server = socketTCP_Server(puerto_local) # Socket TCP 

    sock_server.listen(0) # Servidor a la escucha

    message = clave + ' ' + str(puerto_local) # Composicion del mensaje
    sock_client.sendto(message.encode(), (host, puerto)) # Envio del mensaje

    _thread.start_new_thread(serverHTTP, (sock_server, )) # Inicio de nuevo hilo

    msg_received = sock_client.recv(1024) # Captura del mensaje
    sock_server.close() # Cierre del Servidor
    sock_client.close() # Cierre del Cliente
    print(msg_received.decode()) # Mensaje del Cliente

# FIN FUNCION 5


# FUNCION PRINCIPAL
def main() :

    # PASO 0
    clave1 = paso0(host_uclm, puerto1_uclm) #PASO 0 Devuelve la Clave del PASO 1

    # PASO 1
    if not clave1 == '':
        clave2 = paso1(clave1, puerto_local, host_uclm, puerto1_uclm) #PASO 1 Devuelve la Clave del PASO 2

    # PASO 2
    if not clave2 == '':
        clave3 = paso2(host_uclm, clave2) #PASO 2 Devuelve la Clave del PASO 3

    #PASO 3
    if not clave3 == '':
        clave4 = paso3(host_uclm, puerto3_uclm, clave3) #PASO 3 Devuelve la Clave del PASO 4

    #PASO 4
    if not clave4 == '':
        clave5 = paso4(host_uclm, clave4) #PASO 4 Devuelve la Clave del PASO 5

    #PASO 5
    if not clave5 == '':
        paso5(host_uclm, puerto4_uclm, clave5) #PASO 5 Devuelve la Clave del PASO 
# FIN FUNCION PRINCIPAL


#########################
#	          	#
#  EJECUCION PRINCIPAL  #
#	          	#
#########################

main()

# FIN DE PRACTICA
