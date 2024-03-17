#Importar librerias#
import socket
import threading

username = input("Enter your username: ")

#Definimos el host y el puerto#
host = '127.0.0.1'
port = 5555

#Configurar el socket y mediante el argumento AF_INET vamos a usar de direccion el host y el port, SOCK STREAM para usar el protocolo TCP#
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Conectar el cliente al socket#
client.connect((host, port))

def receive_messages():
    while True:
        try:
            #Recibe el mensaje del servidor y se decodifica con la funcion decode#
            message = client.recv(1024).decode('utf-8')

            #Verifica si el mensaje es para solicitar el username#
            if message == "@username":
                #Envia el username y transforma el string en bytes#
                client.send(username.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error has ocurred")
            #Cierra la conexion#
            client.close
            break

#Envia los mensajes al servidor#
def write_messages():
    while True:
        message = f"{username}: {input('')}"
        #El servidor envia los mensajes a los demas clientes y transforma el string en bytes#
        print("Su MENSAJE AH SIDO ENVIADO ")
        client.send(message.encode('utf-8'))
        

#Permite que las funciones puedan estar ejecutandose varias veces al mismo tiempo en diferentes hilos#
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=write_messages)
write_thread.start()
