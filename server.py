import socket #biblioteca necesaria para realizar una conexión con sockets
login=0
exit=0
apagar=0
disco_temp=[]
nombre="alumno"
ip = "0.0.0.0" 
puerto = 5555 
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((ip, puerto))
servidor.listen(1)
print ("[*] Esperando conexiones en %s:%d" % (ip, puerto))


def crear_db():
	global nombre
	#crear la base de datos
	archivo=open(nombre+".txt", 'w')
	cadena="Id,Nombre,Apellido,Semestre,Carrera\n1,Juan,Perez,5,Computacion\n2,Anita,Lopez,8,Electronica"
	archivo.write(cadena)
	archivo.close()

def leer_tabla(recibido):
	global nombre, disco_temp
	#nombre_t=archivo.split('.')
	if(recibido==nombre):
		#regresas tabla
		global disco_temp
		archivo=open(nombre+".txt", 'r')
		while True:
			linea=archivo.readline()
			disco_temp.append(linea)
			if not linea:
				break
		archivo.close()
		respuesta="".join(disco_temp)
	else:
		respuesta="No existe la tabla"
	return(respuesta)

def leer_tabla_dos(tabla):
	global nombre, disco_temp
	#nombre_t=archivo.split('.')
	if(recibido==nombre):
		#regresas tabla
		global disco_temp
		archivo=open(nombre+".txt", 'r')
		while True:
			linea=archivo.readline()
			disco_temp.append(linea)
			if not linea:
				break
		archivo.close()
		disco_temp.pop()
		respuesta="".join(disco_temp)
	else:
		respuesta="No existe la tabla"
	return(respuesta)

def escribir_tabla(insertar, tabla):
	global disco_temp
	leer_tabla(tabla)
	disco_temp.append(insertar)
	escribe = "".join(disco_temp)
	archivo=open(tabla+".txt", 'w')
	archivo.write(escribe)
	archivo.close()
	del disco_temp[:]
	return("registro insertado con éxito")

def escribir_tabla_dos(cadena):
	archivo=open(tabla+".txt", 'w')
	archivo.write(cadena)
	archivo.close()
	return("registro eliminado")

def instruc_sys(comando):
	global exit, apagar
	if(comando=="ayuda"):
		ayuda="HOLA CLIENTE YO TE AYUDO"
		respuesta=ayuda
	elif(comando=="exit"):
		terminado="Sesión terminada"
		respuesta=terminado
		exit=1
	elif(comando=="salir"):
		apagar=1
		respuesta="conexión terminada"
	else:
		des="comando invalido"
		respuesta=des
	return(respuesta)

def buscar_id(tabla):
	cadena=leer_tabla(tabla)#cadena con contenido de la tabla
	lista=cadena.split('\n')
	tamano=len(lista)
	ultim_reg=lista[tamano-1]
	linea=ultim_reg.split(',')
	del disco_temp[:]
	return(linea[0])

def select_db(comando_recivido):
	if(comando_recivido[0]!="SELECT"):
		respuesta_select="error de sintaxis"
	elif(comando_recivido[1]!="*"):
		respuesta_select="error de sintaxis"
	elif(comando_recivido[2]!="FROM"):
		respuesta_select="error de sintaxis"
	else:
		#respuesta_select="bien"
		respuesta_select=leer_tabla(comando_recivido[3])
		del disco_temp[:]
	return(respuesta_select)

def insert_db(comando_recivido):
	global	nombre
	if(comando_recivido[0]!="INSERT"):
		respuesta_insert="error de sintaxis"
	elif(comando_recivido[1]!="INTO"):
		respuesta_insert="error de sintaxis"
	elif(comando_recivido[2]!=nombre):
		respuesta_insert="no existe la tabla"
	elif(comando_recivido[3]!="VALUES"):
		respuesta_insert="error de sintaxis"
	else:
		#se pueden insertar los valores
		datos=comando_recivido[4].split(',')
		num_datos=len(datos)
		if(num_datos<4):
			respuesta_insert="error en datos a insertar"
		else:
			cadena=comando_recivido[4]
			tamano_cad=len(cadena)
			cad_sin_paren=cadena[1:tamano_cad-1]
			identificador=int(buscar_id(nombre))
			new_id=identificador+1
			insertar='\n'+str(new_id)+','+cad_sin_paren
			respuesta_insert=escribir_tabla(insertar, nombre)
			#respuesta_insert=leer_id(comando_recivido[3])
		del datos[:]
	return(respuesta_insert)

def delete_db(comando_recivido):
	global	nombre
	if(comando_recivido[0]!="DELETE"):
		respuesta_delete="error de sintaxis"
	elif(comando_recivido[1]!="FROM"):
		respuesta_delete="error de sintaxis"
	elif(comando_recivido[2]!=nombre):
		respuesta_delete="no existe la tabla"
	elif(comando_recivido[3]!="WHERE"):
		respuesta_delete="error de sintaxis"
	else:
		cadena=leer_tabla_dos(nombre)
		respuesta_delete=escribir_tabla_dos(cadena)
		del datos[:]
	return(respuesta_insert)
	
def comando(socket_cliente):
	global exit, apagar
	peticion = socket_cliente.recv(1024)
	print ("[*] Mensaje recibido: %s" % peticion.decode())
	comando_recivido=peticion.decode().split()
	print(comando_recivido)
	if(len(comando_recivido)==1):
		#un solo argumento
		respuesta=instruc_sys(peticion.decode())
		socket_cliente.send(respuesta.encode())
	elif(len(comando_recivido)==2):
		#genera un error
		respuesta="comando invalido"
		socket_cliente.send(respuesta.encode())
	elif(len(comando_recivido)==3):
		#genera un error
		respuesta="comando invalido"
		socket_cliente.send(respuesta.encode())
	elif(len(comando_recivido)==4):
		#SELECT * FROM tabla
		respuesta=select_db(comando_recivido)
		socket_cliente.send(respuesta.encode())
	elif(len(comando_recivido)==5):
		#INSERT INTO tabla VALUES (valores)
		respuesta=insert_db(comando_recivido)
		socket_cliente.send(respuesta.encode())
	elif(len(comando_recivido)==5):
		respuesta=delete_db(comando_recivido)
		socket_cliente.send(respuesta.encode())
	#DELETE FROM Alumno WHERE Id=2
	socket_cliente.close()

def logear(socket_cliente):
	global login, apagar
	peticion = socket_cliente.recv(1024)
	print ("[*] Mensaje recibido: %s" % peticion.decode())
	aut="autorizado"
	if(peticion.decode()=="fi-unam"):
		socket_cliente.send(aut.encode())
		login=1
	elif(peticion.decode()=="exit -f"):
		apagar=1
	else:
		s_aut="Contraseña incorrecta"
		socket_cliente.send(s_aut.encode())
	socket_cliente.close()



def comandos():
	global exit, apagar
	while True:
		if(apagar==1):
			break
		if(exit == 0):
			cliente, direccion = servidor.accept()
			print ("[*] Conexion establecida con %s:%d" % (direccion[0] , direccion[1]))
			comando(cliente)
			#conexiones.start()
		else:
			break
	return(exit)

def autenticacion():
	global login, exit, apagar, base
	#crear_db()
	while True:
		if(apagar==1):
			break
		if(login == 0):
			cliente, direccion = servidor.accept()
			print ("[*] Conexion establecida con %s:%d" % (direccion[0] , direccion[1]))
			logear(cliente)
			#conexiones.start()
		else:
			termina_conex=comandos()
			if(termina_conex==1):
				exit=0
				login=0

autenticacion()