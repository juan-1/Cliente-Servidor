import socket
import getpass

servidor = "127.0.0.1"
puerto = 5555
contra=0
apagar=0

def comandos():
	global apagar, contra
	while True:
		cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cliente.connect((servidor, puerto))
		comando=input("#")
		if(comando=="exit"):
			cliente.send(comando.encode());
			respuesta = cliente.recv(4096)
			print (respuesta.decode())
			contra=0
			break
		if(comando =="salir"):
			cliente.send(comando.encode());
			apagar=1
			break
		if(len(comando)== 0):
			comando="NULO"
		cliente.send(comando.encode());
		respuesta = cliente.recv(4096)
		print (respuesta.decode())
	return(contra)


def contraseña():
	global contra, apagar
	while True:
		if(contra == 0):
			print("\n\t¡ingrese la contraseña del servidor!\n")
			contra=1
		if(apagar==1):
			break
		cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		cliente.connect((servidor, puerto))
		password=getpass.getpass("Indica tu contraseña:")
		if(len(password)== 0):
			password="NULO"
		cliente.send(password.encode());
		respuesta = cliente.recv(4096)
		print (respuesta.decode())
		if(respuesta.decode()=="autorizado"):
			sesion=comandos()
			if(sesion==0):
				contra=0

contraseña()
