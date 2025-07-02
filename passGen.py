import random

### FUNCIONES ###

def generar_password(cantMayusculas, cantMinusculas, cantNumeros, cantCarEsp, largo):
	cualquierCaracter = []
	cadenaCaracteres = []
	mayusculas = ["A","B","C","D","E","F","G","H","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
	cadenaCaracteres.extend(random.choices(mayusculas, k=cantMayusculas))
	minusculas = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	cadenaCaracteres.extend(random.choices(minusculas, k=cantMinusculas))
	numeros = ["1","2","3","4","5","6","7","8","9"]
	cadenaCaracteres.extend(random.choices(numeros, k=cantNumeros))
	caracteresEspeciales = [";","!","#","$","%","&","*","(",")","+","=","-","{","}",":","<",">","?"]
	cadenaCaracteres.extend(random.choices(caracteresEspeciales, k=cantCarEsp))
	if len(cadenaCaracteres) < largo:
		if cantMayusculas > 0:
			cualquierCaracter = mayusculas
		if cantMinusculas > 0:
			cualquierCaracter = cualquierCaracter + minusculas
		if cantNumeros > 0:
			cualquierCaracter = cualquierCaracter + numeros
		if cantCarEsp > 0:
			cualquierCaracter = cualquierCaracter + caracteresEspeciales
	cadenaCaracteres.extend(random.choices(cualquierCaracter, k=(largo - len(cadenaCaracteres))))  
	random.shuffle(cadenaCaracteres)  
	password = ""    
	for contenido in cadenaCaracteres:
		password += contenido
	return password

def verificar_seguridad(password, cantMayusculas, cantMinusculas, cantNumeros, cantCarEsp):
	longitud = len(password)
	tieneMayusculas = False
	tieneMinusculas = False  
	tieneNumeros = False  
	tieneCarEsp = False   
	if cantMayusculas > 0:
		tieneMayusculas = True
	if cantMinusculas > 0:
		tieneMinusculas = True
	if cantNumeros > 0:
		tieneNumeros = True
	if cantCarEsp > 0:
		tieneCarEsp = True
	if longitud >= 12 and tieneMayusculas and tieneMinusculas and tieneNumeros and tieneCarEsp:
		nivel = "Muy Alta" 	 
	elif longitud >= 8 and ((tieneMayusculas and tieneMinusculas and tieneNumeros) or (tieneMayusculas and tieneMinusculas and tieneCarEsp) 
		or (tieneMayusculas and tieneNumeros and tieneCarEsp) or (tieneMinusculas and tieneNumeros and tieneCarEsp)):
		nivel = "Alta"
	elif longitud >= 8 and (tieneMayusculas or tieneMinusculas) and (tieneNumeros or tieneCarEsp):
		nivel = "Media"
	elif longitud >= 8:
		nivel = "Baja"
	else:
		nivel = "Muy Baja"
	return nivel

def imprimir_historial(historialPassword,historialNivelSeguridad):
	print("")
	print("Historial de contraseñas generadas:")
	largoLista = len(historialPassword)  
	if largoLista == 0:
		print("AÚN NO SE HA GENERADO NINGUNA PASSWORD")
	else:
		for i in range(largoLista):
			print("En el registro",i+1,"La password generada fue:",historialPassword[i],"Y el nivel de seguridad es:",historialNivelSeguridad[i])

def menu():            	 
	print("")	 
	print("________")
	print("")
	print(" Menú:")
	print("________")
	print("")
	print("Selecciones el numero de la operación deseada y presione enter para continuar.")
	print("1. Generar nueva contraseña")
	print("2. Ver historial de claves generadas")
	print("3. Finalizar el programa. Los datos previamente generados se perderán!")
	return input("Elige una opción: ")  

def requerimientos():
	flagMayusculas = True  
	flagMinusculas = True
	flagNumeros = True    
	flagEspeciales = True
	flagLongitud = True  
	sumaTotal = 0	 
	while sumaTotal == 0:
		cantMayusculas = int(input("Ingrese la cantidad minima de caracteres en mayúsculas deseados: "))
		while flagMayusculas == True:
			if cantMayusculas >= 0:
				flagMayusculas = False
			else:
				cantMayusculas = int(input("VALOR NO VÁLIDO: Ingrese nuevamente la cantidad minima de caracteres en mayúsculas deseados: "))  
		cantMinusculas = int(input("Ingrese la cantidad minima de caracteres en minúsculas deseados: "))
		while flagMinusculas == True:
			if cantMinusculas >= 0:
				flagMinusculas = False
			else:
				cantMinusculas = int(input("VALOR NO VÁLIDO: Ingrese nuevamente la cantidad minima de caracteres en minúsculas deseados: "))
		cantNumeros = int(input("Ingrese la cantidad minima de caracteres numéricos deseados: "))
		while flagNumeros == True:
			if cantNumeros >= 0:
				flagNumeros = False
			else:
				cantNumeros = int(input("VALOR NO VÁLIDO: Ingrese nuevamente la cantidad minima de caracteres numéricos deseados: "))
		cantCarEsp = int(input("Ingrese la cantidad minima de caracteres especiales deseados: "))
		while flagEspeciales == True:
			if cantCarEsp >= 0:
				flagEspeciales = False
			else:
				cantCarEsp = int(input("VALOR NO VÁLIDO: Ingrese nuevamente la cantidad minima de caracteres especiales deseados: "))   
		sumaTotal = cantMayusculas + cantMinusculas + cantNumeros + cantCarEsp
		if sumaTotal > 0:
			datos = False
		else:
			print("LOS REQUERIMIENTOS NO PUEDEN SER TODOS NULOS, DEBE ELEGIR AL MENOS 1 TIPO DE CARACTER")
	largo = int(input("Ingrese la longitud total deseada para la contraseña: "))  
	while flagLongitud == True:
		if largo > 0:
			if cantMayusculas + cantMinusculas + cantNumeros + cantCarEsp > largo:
				print("La suma de los caracteres deseados especificados excede la longitud total.")
				largo = int(input("Ingrese nuevamente la longitud total deseada para la contraseña: "))  
			else:
				flagLongitud = False
				password = generar_password(cantMayusculas, cantMinusculas, cantNumeros, cantCarEsp, largo)
				seguridad = verificar_seguridad(password, cantMayusculas, cantMinusculas, cantNumeros, cantCarEsp)  
				historialPassword.append(password)
				historialNivelSeguridad.append(seguridad)
		else:
			largo = int(input("VALOR NO VÁLIDO: Ingrese nuevamente la longitud total deseada para la contraseña: "))
	return cantMayusculas,cantMinusculas,cantNumeros,cantCarEsp,sumaTotal,largo,password,seguridad

### INICIO - MAIN ###      	 

if __name__ == '__main__':

	historialPassword = []	 
	historialNivelSeguridad = []  
	continuar = True    

	while continuar == True:
		entradaUsuario = menu()   
		
		if entradaUsuario == "1":
			cantMayusculas,cantMinusculas,cantNumeros,cantCarEsp,sumaTotal,largo,password,seguridad = requerimientos()
			print("___________________")
			print("               	")
			print("Contraseña generada:",password)
			print("Nivel de seguridad:",seguridad)
			print("___________________")
		
		elif entradaUsuario == "2":
			imprimir_historial(historialPassword,historialNivelSeguridad)

		elif entradaUsuario == "3":  
			continuar = False

		else:
			print("##################################")
			print("VALOR NO VÁLIDO: Intenta de nuevo.")
			print("##################################")

