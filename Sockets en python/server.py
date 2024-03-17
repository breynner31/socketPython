#Importar librerias#
import socket
import threading

#Definimos el host y el puerto#
host = '127.0.0.1'
port = 5555

#Configurar el socket y mediante el argumento AF_INET vamos a usar de direccion el host y el port, SOCK STREAM para usar el protocolo TCP#
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Pasar los datos de conexion del servidor#
server.bind((host, port))

server.listen()
print(f"Server running on {host}:{port}")

#Almacena las conexiones de los clientes#
clients = []
#Almacena los usernames de cada clien
usernames = []

#Envia el mensaje a todos los clientes#
def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

#El servidor maneja los mensajes de cada cliente#
def handle_messages(client):
    while True:
        try:
            #Obtiene el mensaje del cliente#
            message = client.recv(1024)
            #Ejecuta la funcion broadcast#
            broadcast(message,  client)
        except:
                #Obtiene el index de la lista clients#
                index = clients.index(client)
                #Obtiene el username con el index#
                username = usernames[index]
                #Ejecuta la funcion broadcast y transforma el string en bytes#
                broadcast(f"ChatBot: {username} disconnected".encode('utf-8'))
                #Elimina el cliente y el username de la lista#
                clients.remove(client)
                usernames.remove(username)
                #Cierra la conexion del cliente
                client.close()
                break
        
#El servidor acepta y maneja las conexiones#
def receive_connections():
     while True:
        client, address = server.accept()

        #Solicita el username al usuario y transforma el string en bytes#
        client.send("@username".encode("utf-8"))
        
        #Recibe el username del cliente y se decodifica con la funcion decode#
        username = client.recv(1024).decode('utf-8')

        #Agrega el cliente y el username a las listas#
        clients.append(client)
        usernames.append(username)

        #Se imprime el mensaje cuando se conecte el usuario con su username y la direccion de conexion#
        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} joined the chat".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))
        
        #Permite que las funciones puedan estar ejecutandose varias veces al mismo tiempo en diferentes hilos#
        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()
     


     

   

    


