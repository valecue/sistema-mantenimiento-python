''' Sistema de Seguimiento para Taller Mecánico '''

''' Importamos la funcion que genera contraseñas aleatorias seguras realizado en el TP de Introduccion a la Algoritmia y los diccionarios. '''

from colorama import init, Fore, Style, Back
init(convert=True)  # Forzar colores en Windows
from passGen import generar_password
from usuarios import usuarios
import re
from datetime import datetime
import json
from getpass import getpass
from datetime import timedelta


''' Funcion que invoca a las funciones de login y menu; controla si el usuario esta logueado. '''
def login_y_menu():
    logeo = True  # Controla si el usuario se está logueando

    while logeo == True:
        usuario, perfil = acceso_sistema(usuarios)
        salir = False
        salir = main_menu(usuario, perfil)  # Retorna True si el usuario selecciona "Salir"

        if salir == True:
            # Confirmación de solicitud de salida
            bucle_salir = False
            while bucle_salir == False:
                confirmacion = input(Fore.CYAN + "¿Estás seguro que deseas salir del sistema? (S/N): " + Style.RESET_ALL).upper()
                if confirmacion == 'S':
                    logeo = False  # Cambiamos a False si confirma la salida
                    bucle_salir = True
                    print(Fore.YELLOW + "Saliendo del sistema... Programa terminado." + Style.RESET_ALL)
                elif confirmacion == 'N':
                    print(Fore.YELLOW + "Regresando al sistema..." + Style.RESET_ALL)
                    logeo = True  # Continuar el ciclo para seguir en el sistema
                    bucle_salir = True
                else:
                    print(Fore.RED + "Opcion no valida, intente nuevamente:" + Style.RESET_ALL)

    print(Fore.YELLOW + "Programa terminado." + Style.RESET_ALL)


''' Funcion de login, validamos usuario, password y perfil de usuario. Tambien bloquea usuario al 3er intento de acceso fallido. '''
def acceso_sistema(usuarios): 
    print(Fore.YELLOW + "Bienvenido al Sistema de Seguimiento de Taller Mecánico" + Style.RESET_ALL)
    login = True
    while login == True:
        nombre = input(Fore.CYAN + "Ingrese su nombre de usuario: " + Style.RESET_ALL).upper()
        usr_pass = getpass(Fore.CYAN + "Ingrese su contraseña: " + Style.RESET_ALL)

        ''' Verificamos si el usuario existe y la contraseña es correcta y no esta bloqueado '''
        if nombre in usuarios and usuarios[nombre]["password"] == usr_pass and usuarios[nombre]["failed_login_count"] < 3:
            print(Fore.GREEN + f" ####  Login exitoso. Bienvenido {nombre} al sistema de gestión.  #### " + Style.RESET_ALL)
            perfil = usuarios[nombre]["perfil"]
    
            # Usamos lambda para verificar si hay tickets abiertos e imprimir una notificacion
            try:
                with open("tickets.json", "r") as file:
                    tickets = json.load(file)
            except FileNotFoundError:
                tickets = {}  # Si no existe el archivo, inicializar un diccionario vacío
    
            tickets_abiertos = lambda: True if [t for t in tickets.values() if t["estado"] == "ABIERTO"] else False
            if perfil == "admin":
                if tickets_abiertos() == True:
                    print(Fore.YELLOW + "TENES TICKETS ABIERTOS PENDIENTES." + Style.RESET_ALL)
            usuarios[nombre]["failed_login_count"] = 0
            return nombre, perfil  # Retorna el usuario autenticado y su perfil
        else:
            if nombre in usuarios:  # Verificamos si el nombre de usuario existe e incrementamos el contador en 1
                usuarios[nombre]["failed_login_count"] += 1
            print(Fore.RED + "Nombre de usuario o contraseña incorrectos. Intente nuevamente o contacte a un administrador." + Style.RESET_ALL)
            print(Fore.RED + "Recuerde que al tercer intento erroneo el usuario quedara bloqueado." + Style.RESET_ALL)
            
        
''' Funcion que crea usuario y password, ademas verifica que el usuario no este en uso. '''
def alta_usuario(usuarios): 
    new_user = True
    while new_user == True:
        user = input(Fore.CYAN + "Ingrese el nombre de usuario: " + Style.RESET_ALL).strip().upper()

        if not user:
            print(Fore.RED + "El nombre de usuario no puede estar vacío. Intente nuevamente." + Style.RESET_ALL)
            continue

        if user not in usuarios:
            password = generar_password(2, 2, 2, 2, 8)
            
            ''' Submenú para elegir perfil '''
            elegir_perfil = "0"
            while elegir_perfil not in ["1", "2"]:
                print(Fore.YELLOW + "Seleccione el perfil del usuario:" + Style.RESET_ALL)
                print(Fore.YELLOW + "1 para admin; 2 para mecanico " + Style.RESET_ALL)
                
                elegir_perfil = input(Fore.CYAN + "Ingrese el número correspondiente al perfil: " + Style.RESET_ALL)

                if elegir_perfil == "1":
                    perfil = "admin"
                elif elegir_perfil == "2":
                    perfil = "mecanico"
                else:
                    print("")
                    print(Fore.RED + "Opción no válida. Intente nuevamente." + Style.RESET_ALL)
                    
            # Añadimos el nuevo usuario al diccionario
            usuarios[user] = {"password": password, "perfil": perfil, "failed_login_count":0}
            print(Fore.YELLOW + "*******************************************************************" + Style.RESET_ALL)
            print(Fore.GREEN + f"   Se creó el usuario {user} y su nueva contraseña es {password}" + Style.RESET_ALL)
            print(Fore.YELLOW + "*******************************************************************" + Style.RESET_ALL)
            new_user = False
        else:
            print(Fore.RED + "El usuario ya existe. Intente nuevamente con uno diferente." + Style.RESET_ALL)
    
        # Guardar cambios en el archivo `usuarios.py`
        with open("usuarios.py", "w") as file:
            file.write("# Listado de usuarios, claves y perfiles.\n")
            file.write("usuarios = {\n")
            for user, data in usuarios.items():
                file.write(f"    \"{user}\": {data},\n")
            file.write("}\n")

    return usuarios


''' Funcion que lista usuarios y roles '''
''' Se listan los usuarios con las contraseñas '''
def lista_usuarios(usuarios): 
    print(Fore.YELLOW + "\n####################" + Style.RESET_ALL)
    print(Fore.YELLOW + "Usuario  -  Perfil  -  Password  -  Failed_login_count" + Style.RESET_ALL)
    for user, info in usuarios.items():
        print(Fore.YELLOW + f"{user}   -   {info['perfil']}   -   {info['password']}  -  {info['failed_login_count']}" + Style.RESET_ALL)
    print(Fore.YELLOW + "####################" + Style.RESET_ALL)
    return


''' Registro de autos '''
def registroVehiculos(matrizAutos):

    # Obtener el año actual
    anio_actual = datetime.now().year

    registroAuto = input(Fore.CYAN + 'Ingrese la marca del auto (o ingrese "-1" para salir): ' + Style.RESET_ALL).upper()
    while registroAuto != "-1":

        # Opción de cancelar en cualquier momento
        if registroAuto == "-1":
            print(Fore.YELLOW + "Operación cancelada. Regresando al menú." + Style.RESET_ALL)
            return matrizAutos

        # Solicitar datos adicionales del vehículo
        modeloAuto = input(Fore.CYAN + 'Ingrese el modelo del Auto (o ingrese "-1" para cancelar): ' + Style.RESET_ALL).upper()
        if modeloAuto == "-1":
            print(Fore.YELLOW + "Operación cancelada. Regresando al menú." + Style.RESET_ALL)
            return matrizAutos

        # Validar que el año no esté vacío y sea un número
        anioAuto = None
        while not anioAuto:
            anioAuto_input = input(Fore.CYAN + f'Ingrese el año del auto (por ejemplo, {anio_actual}): ' + Style.RESET_ALL)
            if anioAuto_input == "-1":
                print(Fore.YELLOW + "Operación cancelada. Regresando al menú." + Style.RESET_ALL)
                return matrizAutos
            if anioAuto_input.isdigit() and 1900 <= int(anioAuto_input) <= anio_actual:  # Usar el año actual
                anioAuto = int(anioAuto_input)
            else:
                print(Fore.RED + f"Año inválido. Ingrese un año válido entre 1900 y {anio_actual}." + Style.RESET_ALL)

        # Inicializar variable de control (bandera)
        patenteValida = False
        correoValido = False
        
        # Bucle para validar la patente
        while patenteValida == False:
            patenteAuto = input(Fore.CYAN + 'Ingrese la patente del auto (o ingrese "-1" para cancelar): ' + Style.RESET_ALL).upper()
            if patenteAuto == "-1":
                print(Fore.YELLOW + "Operación cancelada. Regresando al menú." + Style.RESET_ALL)
                return matrizAutos
            if re.match("^[A-Z]{3}[0-9]{3}$|^[A-Z]{2}[0-9]{3}[A-Z]{2}$", patenteAuto):
                patenteValida = True  # Actualiza la variable de control si la patente es válida
            else:
                print(Fore.RED + "Patente inválida. Debe ser formato ABC123 o AB123CD." + Style.RESET_ALL)
        
        # Validar que los kilómetros sean un número positivo
        cantKM = None
        while cantKM is None:
            cantKM_input = input(Fore.CYAN + 'Ingrese la cantidad de kilometros (o ingrese "-1" para cancelar): ' + Style.RESET_ALL)
            if cantKM_input == "-1":
                print(Fore.YELLOW + "Operación cancelada. Regresando al menú." + Style.RESET_ALL)
                return matrizAutos
            if cantKM_input.isdigit() and int(cantKM_input) >= 0:
                cantKM = int(cantKM_input)
            else:
                print(Fore.RED + "Kilómetros inválidos. Ingrese un número positivo." + Style.RESET_ALL)
        
        titular = input(Fore.CYAN + 'Ingrese el nombre del titular del vehículo (o ingrese "-1" para cancelar): ' + Style.RESET_ALL).lower()
        if titular == "-1":
            print(Fore.YELLOW + "Operación cancelada. Regresando al menú." + Style.RESET_ALL)
            return matrizAutos
        
        while correoValido == False:
            mail = input(Fore.CYAN + 'Ingrese el correo electrónico del titular (o ingrese "-1" para cancelar): ' + Style.RESET_ALL).lower()
            if mail == "-1":
                print(Fore.YELLOW + "Operación cancelada. Regresando al menú." + Style.RESET_ALL)
                return matrizAutos
            if re.match(r"[^@]+@[^@]+\.[^@]+", mail):
                correoValido = True
            else: 
                print(Fore.RED + "Correo inválido. Debe ser formato usuario@dominio.com o similar" + Style.RESET_ALL)
        
        # Agregar los datos del vehículo a la lista
        matrizAutos.append([registroAuto, modeloAuto, anioAuto, patenteAuto, cantKM, titular, mail])
        
        # Imprimir los datos del vehículo cargado
        print(Fore.GREEN + "\n¡Vehículo registrado correctamente!")
        print(Fore.GREEN + "Marca: " + registroAuto)
        print(Fore.GREEN + "Modelo: " + modeloAuto)
        print(Fore.GREEN + "Año: " + str(anioAuto))
        print(Fore.GREEN + "Patente: " + patenteAuto)
        print(Fore.GREEN + "Kilómetros: " + str(cantKM))
        print(Fore.GREEN + "Titular: " + titular.capitalize())
        print(Fore.GREEN + "Correo: " + mail)
        print(Style.RESET_ALL)

        # Solicitar el modelo del siguiente auto o ingresar "-1" para salir
        registroAuto = input(Fore.CYAN + 'Ingrese la marca del auto (o ingrese "-1" para salir): ' + Style.RESET_ALL).upper()
    
    return matrizAutos


''' Listado de los autos en la matriz '''
def listarVehiculos(matrizAutos):
    # Listar todos los autos registrados
    if len(matrizAutos) <= 0:
        print(Fore.RED + "No hay vehiculos ingresados en el sistema!" + Style.RESET_ALL)
    else:
        for auto in matrizAutos:
            print(Fore.YELLOW + f"Marca: {auto[0]} ,Modelo: {auto[1]}, Año: {auto[2]} ,Patente: {auto[3]} , Kilómetros: {auto[4]}, Titular: {auto[5]}, Correo: {auto[6]}" + Style.RESET_ALL)
        

''' Funcion que agrega el servicio realizado al vehiculo (redefinir campos o datos requeridos '''
def carga_servicio_realizado(matrizAutos):
    try:
        with open("serv.json", "r") as file:
            serv = json.load(file)
    except FileNotFoundError:
        serv = {}

    new_service = True
    while new_service:
        # Solicitar dominio/patente
        dominio = input(Fore.CYAN + "Ingrese el dominio/patente (o -1 para cancelar): " + Style.RESET_ALL).upper()
        
        if dominio == "-1":
            print(Fore.YELLOW + "Operación cancelada por el usuario." + Style.RESET_ALL)
            return serv  # Salimos de la función completamente

        # Buscar el vehículo en matrizAutos usando la patente
        vehiculo_encontrado = None
        for vehiculo in matrizAutos:
            if vehiculo[3] == dominio:
                vehiculo_encontrado = vehiculo
        if not vehiculo_encontrado:
            print(Fore.RED + "El dominio seleccionado no existe!" + Style.RESET_ALL)
            print(Fore.RED + "Debe dar de alta el vehículo antes de cargar el servicio!" + Style.RESET_ALL)
            continue

        # Solicitar descripción del servicio
        servicio = input(Fore.CYAN + f"Ingrese la descripción de las tareas realizadas sobre el dominio {dominio} (o -1 para cancelar): " + Style.RESET_ALL)
        if servicio == "-1":
            print(Fore.YELLOW + "Operación cancelada por el usuario." + Style.RESET_ALL)
            return serv

        # Solicitar y validar kilometraje
        kilometraje_valido = False
        while not kilometraje_valido:
            nuevo_kilometraje = input(Fore.CYAN + f"Ingrese el nuevo kilometraje para el vehículo {dominio} (o -1 para cancelar): " + Style.RESET_ALL)
            
            if nuevo_kilometraje == "-1":
                print(Fore.YELLOW + "Operación cancelada por el usuario." + Style.RESET_ALL)
                return serv
            
            if nuevo_kilometraje.isdigit():
                nuevo_kilometraje = int(nuevo_kilometraje)
                
                # Comparar con el kilometraje actual
                kilometraje_actual = vehiculo_encontrado[4]
                if nuevo_kilometraje >= kilometraje_actual:
                    kilometraje_valido = True
                else:
                    print(Fore.RED + f"El kilometraje ingresado ({nuevo_kilometraje}) no puede ser menor al actual ({kilometraje_actual}). Intente nuevamente." + Style.RESET_ALL)
            else:
                print(Fore.RED + "El kilometraje ingresado no es válido. Debe ser un número." + Style.RESET_ALL)
        
        # Actualizar el kilometraje en la matrizAutos
        vehiculo_encontrado[4] = nuevo_kilometraje
        print(Fore.GREEN + f"Kilometraje actualizado a {nuevo_kilometraje} km para el vehículo {dominio}." + Style.RESET_ALL)
        
        # Añadir el servicio al archivo JSON
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if dominio not in serv:
            serv[dominio] = []  # Inicializar lista de servicios para el dominio
        
        serv[dominio].append({"descripcion": servicio, "fecha": fecha})
        
        # Guardar los servicios en el archivo
        with open("serv.json", "w") as file:
            json.dump(serv, file, indent=4)
        
        print(Fore.GREEN + f"Se cargó al dominio {dominio} el servicio: {servicio} realizado el {fecha}." + Style.RESET_ALL)

        # Preguntar si desea continuar
        continuar = input(Fore.CYAN + "¿Desea cargar otro servicio? (s/n): " + Style.RESET_ALL).lower()
        if continuar != "s":
            new_service = False

    return serv

''' Funcion que lista servicios realizados a un vehiculo '''
def lista_servicios_realizados(matrizAutos):
    try:
        with open("serv.json", "r") as file:
            servicios = json.load(file)
    except FileNotFoundError:
        print(Fore.RED + "No hay servicios registrados todavía." + Style.RESET_ALL)
        return

    while True:
        print(Fore.YELLOW + "\n#### Consulta de Servicios ####" + Style.RESET_ALL)
        print("1. Listar servicios de un vehículo específico.")
        print("2. Listar servicios de todos los vehículos.")
        print("3. Buscar servicios por cliente o correo.")
        print("0. Volver al menú principal.")

        opcion = input(Fore.CYAN + "\nSeleccione una opción: " + Style.RESET_ALL)

        if opcion == "0":
            return

        elif opcion == "1":
            # Buscar servicios por dominio
            dominio = input(Fore.CYAN + "\nIngrese el dominio/patente del vehículo: " + Style.RESET_ALL).upper()
            if dominio in servicios:
                print(Fore.YELLOW + f"\nServicios realizados para el vehículo {dominio}:" + Style.RESET_ALL)
                for idx, servicio in enumerate(servicios[dominio], start=1):
                    print(Fore.GREEN + f"  {idx}. {servicio['descripcion']} (Fecha: {servicio['fecha']})" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"No se encontraron servicios para el vehículo {dominio}." + Style.RESET_ALL)

        elif opcion == "2":
            # Listar servicios de todos los vehículos
            print(Fore.YELLOW + "\nServicios realizados por vehículo:" + Style.RESET_ALL)
            for dominio, historial in servicios.items():
                print(Fore.CYAN + f"\nVehículo: {dominio}" + Style.RESET_ALL)
                for idx, servicio in enumerate(historial, start=1):
                    print(Fore.YELLOW + f"  {idx}. {servicio['descripcion']} (Fecha: {servicio['fecha']})" + Style.RESET_ALL)

        elif opcion == "3":
            # Buscar servicios por cliente o correo
            busqueda = input(Fore.CYAN + "\nIngrese el nombre del cliente o su correo electrónico: " + Style.RESET_ALL).lower()
            dominios = [auto[3] for auto in matrizAutos if busqueda in auto[5:]]

            if dominios:
                print(Fore.GREEN + f"\nDominios encontrados para '{busqueda}':" + Style.RESET_ALL)
                for dominio in dominios:
                    print(Fore.YELLOW + f"- {dominio}" + Style.RESET_ALL)

                print(Fore.CYAN + "\nMantenimientos realizados:" + Style.RESET_ALL)
                for dominio in dominios:
                    if dominio in servicios:
                        print(Fore.CYAN + f"\nVehículo: {dominio}" + Style.RESET_ALL)
                        for idx, servicio in enumerate(servicios[dominio], start=1):
                            print(Fore.GREEN + f"  {idx}. {servicio['descripcion']} (Fecha: {servicio['fecha']})" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + f"\nNo se encontraron servicios registrados para el vehículo {dominio}." + Style.RESET_ALL)
            else:
                print(Fore.RED + f"\nNo se encontraron dominios asociados a '{busqueda}'." + Style.RESET_ALL)

        else:
            print(Fore.RED + "\nOpción no válida. Intente nuevamente." + Style.RESET_ALL)

        input(Fore.CYAN + "\nPresione ENTER para continuar..." + Style.RESET_ALL)

''' Funcion para dar de baja a un usuarios '''
def baja_usuario():   
    # Listar usuarios para elegir cuál dar de baja
    print(Fore.YELLOW + "Usuarios disponibles:" + Style.RESET_ALL)
    for index, user in enumerate(usuarios.keys(), start=1):
        print(Fore.YELLOW + f"{index}. {user}" + Style.RESET_ALL)

    ''' Solicitar al usuario que elija el número correspondiente al usuario a eliminar '''
    try:
        opcion = int(input(Fore.CYAN + "Ingrese el número del usuario que desea dar de baja: " + Style.RESET_ALL))
        if opcion < 1 or opcion > len(usuarios):
            print(Fore.RED + "Opción no válida." + Style.RESET_ALL)
            return
        
        # Obtener el nombre del usuario a eliminar
        usuario_a_eliminar = list(usuarios.keys())[opcion - 1]

        # Verificar si hay al menos un administrador
        admins = [user for user, data in usuarios.items() if data["perfil"] == "admin"]
        if len(admins) == 1 and usuario_a_eliminar == admins[0]:
            print(Fore.RED + "No se puede eliminar el último administrador del sistema." + Style.RESET_ALL)
            return

        # Confirmar eliminación
        confirmacion = input(Fore.CYAN + f"¿Está seguro de que desea eliminar al usuario '{usuario_a_eliminar}'? (s/n): " + Style.RESET_ALL)
        if confirmacion.lower() != 's':
            print(Fore.YELLOW + "Operación cancelada." + Style.RESET_ALL)
            return
        
        # Eliminar el usuario y actualizar archivo
        del usuarios[usuario_a_eliminar]
        print(Fore.GREEN + f"Usuario '{usuario_a_eliminar}' eliminado exitosamente." + Style.RESET_ALL)

        # Guardar cambios en el archivo `usuarios.py`
        with open("usuarios.py", "w") as file:
            file.write("# Listado de usuarios, claves y perfiles.\n")
            file.write("usuarios = {\n")
            for user, data in usuarios.items():
                file.write(f"    \"{user}\": {data},\n")
            file.write("}\n")

    except ValueError:
        print(Fore.RED + "Entrada no válida. Por favor, ingrese un número." + Style.RESET_ALL)
        

''' Funcion para desbloquear usuarios '''
def desbloqueo_usuario(usuarios):
    # Crear una lista de usuarios bloqueados (failed_login_count >= 3)
    usuarios_bloqueados = [user for user, info in usuarios.items() if info["failed_login_count"] >= 3]
    
    if len(usuarios_bloqueados) == 0:
        print(Fore.YELLOW + "No hay usuarios bloqueados en este momento." + Style.RESET_ALL)
        return

    # Mostrar los usuarios bloqueados con un índice usando enumerate
    print(Fore.YELLOW + "\nUsuarios bloqueados:\n" + Style.RESET_ALL)
    for id, user in enumerate(usuarios_bloqueados):
        print(Fore.YELLOW + f"{id} - {user}" + Style.RESET_ALL)

    # Solicitar al admin que seleccione un usuario para desbloquear
    cicloWhile = True
    while cicloWhile == True:
        try:
            print(Fore.YELLOW + "\nA continuacion seleccione el numero de usuario a desbloquear o ingrese -1 para cancelar." + Style.RESET_ALL)
            seleccion = int(input(Fore.CYAN + "Ingrese la opcion deseada: " + Style.RESET_ALL))
            if 0 <= seleccion < len(usuarios_bloqueados): #recordar que len da el total pero el indice va de 0 a len-1.
                usuario_seleccionado = usuarios_bloqueados[seleccion] #carga como string el contenido de la posicion
                # Desbloquear el usuario (resetear failed_login_count)
                usuarios[usuario_seleccionado]["failed_login_count"] = 0
                print(Fore.GREEN + f"El usuario {usuario_seleccionado} ha sido desbloqueado." + Style.RESET_ALL)
                cicloWhile = False
            elif seleccion == -1:
                print(Fore.YELLOW + "Cancelando..." + Style.RESET_ALL)
                return
            else:
                print(Fore.RED + "Selección no válida." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Debe ingresar un número válido." + Style.RESET_ALL)


''' Función para actualizar el password de un usuario '''
def cambio_password(usuarios):
    print(Fore.YELLOW + "\nLista de usuarios:\n" + Style.RESET_ALL)
    # Mostrar la lista de usuarios con un índice
    for idx, user in enumerate(usuarios.keys()):
        print(Fore.YELLOW + f"{idx + 1}. {user}" + Style.RESET_ALL)
    
    # Solicitar al administrador que elija el usuario para cambiar el password
    try:
        seleccion = int(input(Fore.CYAN + "\nSeleccione el número del usuario para cambiar la contraseña o ingrese -1 para cancelar: " + Style.RESET_ALL))
        if seleccion == -1:
            print(Fore.YELLOW + "Cancelando cambio de contraseña..." + Style.RESET_ALL)
            return
        
        # Validar que la selección es válida
        if 1 <= seleccion <= len(usuarios):
            usuario_seleccionado = list(usuarios.keys())[seleccion - 1]
            
            # Solicitar el nuevo password
            nuevo_password = getpass(Fore.CYAN + f"Ingrese el nuevo password para el usuario {usuario_seleccionado}: " + Style.RESET_ALL)
            confirmar_password = getpass(Fore.CYAN + "Confirme el nuevo password: " + Style.RESET_ALL)
            
            # Verificar que el password cumple los requisitos de seguridad y es igual a la confirmación
            if nuevo_password == confirmar_password and len(nuevo_password) >= 8:
                usuarios[usuario_seleccionado]["password"] = nuevo_password
                
                # Actualizar el archivo usuarios.py
                with open("usuarios.py", "w") as file:
                    file.write("# Listado de usuarios, claves y perfiles.\n")
                    file.write("usuarios = {\n")
                    for user, data in usuarios.items():
                        file.write(f"    \"{user}\": {data},\n")
                    file.write("}\n")
                
                print(Fore.GREEN + f"Contraseña para {usuario_seleccionado} actualizada correctamente." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Error: Las contraseñas no coinciden o no cumplen con los requisitos de seguridad (mínimo 8 caracteres)." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Selección no válida." + Style.RESET_ALL)
    except ValueError:
        print(Fore.RED + "Debe ingresar un número válido." + Style.RESET_ALL)

    return usuarios


''' Función para modificar información de un vehículo '''
def modificar_vehiculo(matrizAutos):
    '''Función para modificar los datos de un vehículo sin eliminarlo, para mantener el historial'''
    
    # Ingreso la patente del vehículo que quiero modificar
    patente = input(Fore.CYAN + "Ingrese la patente del vehículo que desea modificar: " + Style.RESET_ALL).upper()
    
    # Buscar el vehículo por la patente
    vehiculo_encontrado = False
    for vehiculo in matrizAutos:
        if vehiculo[3] == patente:
            vehiculo_encontrado = True
            
            # Mostrar opciones de modificación
            opcion = "1"  # Inicializar con un valor diferente de "0" para entrar al bucle
            while opcion != "0":
                print(Fore.GREEN + f"\nVehículo a modificar: \nMarca: {vehiculo[0]}\nModelo: {vehiculo[1]}\nAño: {vehiculo[2]}\nPatente: {vehiculo[3]}\nKilómetros: {vehiculo[4]}\nTitular: {vehiculo[5]}\nCorreo: {vehiculo[6]}" + Style.RESET_ALL)
                print("")
                print(Fore.YELLOW + "\n¿Qué dato desea modificar?" + Style.RESET_ALL)
                print(Fore.YELLOW + "1. Marca" + Style.RESET_ALL)
                print(Fore.YELLOW + "2. Modelo" + Style.RESET_ALL)
                print(Fore.YELLOW + "3. Año" + Style.RESET_ALL)
                print(Fore.YELLOW + "4. Kilometraje" + Style.RESET_ALL)
                print(Fore.YELLOW + "5. Patente" + Style.RESET_ALL)  
                print(Fore.YELLOW + "6. Titular" + Style.RESET_ALL)
                print(Fore.YELLOW + "7. Correo" + Style.RESET_ALL)
                print(Fore.YELLOW + "0. Cancelar modificación / Volver" + Style.RESET_ALL)

                opcion = input(Fore.CYAN + "Seleccione una opción: " + Style.RESET_ALL)
                
                if opcion == "1":
                    nueva_marca = input(Fore.CYAN + "Ingrese la nueva marca: " + Style.RESET_ALL).upper()
                    vehiculo[0] = nueva_marca
                    print(Fore.GREEN + "Marca actualizada correctamente." + Style.RESET_ALL)
                
                elif opcion == "2":
                    nuevo_modelo = input(Fore.CYAN + "Ingrese el nuevo modelo: " + Style.RESET_ALL).upper()
                    vehiculo[1] = nuevo_modelo
                    print(Fore.GREEN + "Modelo actualizado correctamente." + Style.RESET_ALL)
                
                elif opcion == "3":
                    nuevo_anio = input(Fore.CYAN + "Ingrese el nuevo año: " + Style.RESET_ALL)
                    try:
                        vehiculo[2] = int(nuevo_anio)
                        print(Fore.GREEN + "Año actualizado correctamente." + Style.RESET_ALL)
                    except ValueError:
                        print(Fore.RED + "El año debe ser un número válido." + Style.RESET_ALL)
                
                elif opcion == "4":
                    nuevo_km = input(Fore.CYAN + "Ingrese el nuevo kilometraje: " + Style.RESET_ALL)
                    try:
                        vehiculo[4] = int(nuevo_km)
                        print(Fore.GREEN + "Kilometraje actualizado correctamente." + Style.RESET_ALL)
                    except ValueError:
                        print(Fore.RED + "El kilometraje debe ser un número válido." + Style.RESET_ALL)

                elif opcion == "5":  
                    nueva_patente = input(Fore.CYAN + "Ingrese la nueva patente: " + Style.RESET_ALL).upper()
                    vehiculo[3] = nueva_patente
                    print(Fore.GREEN + "Patente actualizada correctamente." + Style.RESET_ALL)
                
                elif opcion == "6":
                    nuevo_titular = input(Fore.CYAN + "Ingrese el nuevo titular: " + Style.RESET_ALL).upper()
                    vehiculo[5] = nuevo_titular
                    print(Fore.GREEN + "Titular actualizado correctamente." + Style.RESET_ALL)

                elif opcion == "7":
                    nuevo_correo = input(Fore.CYAN + "Ingrese el nuevo correo: " + Style.RESET_ALL).lower()
                    vehiculo[6] = nuevo_correo
                    print(Fore.GREEN + "Correo actualizado correctamente." + Style.RESET_ALL)

                elif opcion == "0":
                    print(Fore.YELLOW + "Modificación cancelada." + Style.RESET_ALL)
                
                else:
                    print(Fore.RED + "Opción no válida. No se realizaron cambios." + Style.RESET_ALL)
            # Si se encontró el vehículo, salimos de la función después de realizar las modificaciones
            return
    
    # Si se llega aquí, significa que no se encontró el vehículo
    if not vehiculo_encontrado:
        print(Fore.RED + f"No se encontró un vehículo con la patente {patente}." + Style.RESET_ALL)


''' Funcion para listar los servicios de un dominio '''
def servicio_por_patente(matrizAutos):
    '''Buscador por patente y muestra los detalles del vehículo'''
    try:
        with open("serv.json", "r") as file:
            servicios = json.load(file)
    except FileNotFoundError:
        print(Fore.RED + "No se encontró el archivo de servicios." + Style.RESET_ALL)
        return
    
    # Cargar los intervalos de mantenimiento de las marcas
    try:
        with open("mantenimientos.json", "r") as file:
            mantenimientos = json.load(file)
    except FileNotFoundError:
        print(Fore.RED + "No se encontró el archivo de intervalos de mantenimiento." + Style.RESET_ALL)
        return
    
    patente = input(Fore.CYAN + "Ingrese la patente a buscar: " + Style.RESET_ALL).upper()
    
    # Buscar los detalles del vehículo en matrizAutos
    vehiculo_encontrado = False
    for vehiculo in matrizAutos:
        if vehiculo[3] == patente:
            vehiculo_encontrado = True
            # Imprimir los detalles del vehículo
            print(Fore.YELLOW + f"\nDetalles del vehículo con patente {patente}:" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Marca: {vehiculo[0]}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Modelo: {vehiculo[1]}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Año: {vehiculo[2]}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Kilómetros: {vehiculo[4]}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Titular: {vehiculo[5]}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"Correo: {vehiculo[6]}" + Style.RESET_ALL)
            print(Fore.YELLOW + "───────────────────────────────────" + Style.RESET_ALL)
            # Guardo datos que usamos mas abajo
            marca_vehiculo = vehiculo[0]
            kilometros_actuales = vehiculo[4]
            anio_vehiculo = vehiculo[2]

    if vehiculo_encontrado:
        # Mostrar los servicios asociados a la patente
        if patente in servicios:
            print(Fore.YELLOW + f"\nServicios para la patente {patente}:" + Style.RESET_ALL)
            for servicio in servicios[patente]:
                print(Fore.YELLOW + f"Descripción: {servicio['descripcion']}" + Style.RESET_ALL)
                print(Fore.YELLOW + f"Fecha: {servicio['fecha']}" + Style.RESET_ALL)
                print(Fore.YELLOW + "───────────────────────────────────" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"No se encontraron servicios para la patente {patente}" + Style.RESET_ALL)
        
        if marca_vehiculo in mantenimientos:
            intervalo_mantenimiento = mantenimientos[marca_vehiculo]  # Intervalo de mantenimiento en km
            anio_actual = datetime.now().year  # Año actual
            
            # Calcular los kilómetros recorridos por año
            if anio_actual == anio_vehiculo:
                kilometros_por_ano = kilometros_actuales  # Si el vehículo es de este año, no se divide
            else:
                kilometros_por_ano = kilometros_actuales / (anio_actual - anio_vehiculo)
            
            # Calcular los kilómetros que faltan para el próximo mantenimiento
            proximo_mantenimiento_km = kilometros_actuales + intervalo_mantenimiento
            
            # Calcular el número de días necesarios para alcanzar el próximo mantenimiento
            dias_para_mantenimiento = intervalo_mantenimiento * 365 / kilometros_por_ano

            # Calcular la fecha estimada del próximo mantenimiento sumando los días
            fecha_proximo_mantenimiento = datetime.now() + timedelta(days=dias_para_mantenimiento)
            
            # Mostrar la fecha y kilometraje del próximo mantenimiento
            print(Fore.GREEN + f"El próximo mantenimiento se estima para el {fecha_proximo_mantenimiento.strftime('%Y-%m-%d')}, con un kilometraje de {proximo_mantenimiento_km} km. O lo que ocurra primero!" + Style.RESET_ALL)
        else:
            print(Fore.RED + f"No se tiene un intervalo de mantenimiento definido para la marca {marca_vehiculo}." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"No se encontró el vehículo con la patente {patente}" + Style.RESET_ALL)


''' Funcion para generar reporte de servicios realizados ayer '''
def reporte_ayer():
    '''Reporte de servicios realizados el día anterior'''
    try:
        with open("serv.json", "r") as file:
            servicios = json.load(file)
    except FileNotFoundError:
        print(Fore.RED + "No se encontró el archivo de servicios." + Style.RESET_ALL)
        return
        
    print(Fore.YELLOW + "\n#### REPORTE DE SERVICIOS DE AYER ####\n" + Style.RESET_ALL)
    
    # Obtener la fecha de ayer
    fecha_ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Filtrar servicios de ayer
    servicios_ayer = []
    for patente, lista_servicios in servicios.items():
        for servicio in lista_servicios:
            if servicio['fecha'].startswith(fecha_ayer):
                servicio['patente'] = patente
                servicios_ayer.append(servicio)
    
    if not servicios_ayer:
        print(Fore.YELLOW + f"No se encontraron servicios realizados el día {fecha_ayer}" + Style.RESET_ALL)
        return
        
    # Mostrar servicios encontrados
    print(Fore.YELLOW + f"Servicios realizados el {fecha_ayer}:" + Style.RESET_ALL)
    print(Fore.YELLOW + "═══════════════════════════════════════" + Style.RESET_ALL)
    for servicio in servicios_ayer:
        print(Fore.YELLOW + f"Patente: {servicio['patente']}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Descripción: {servicio['descripcion']}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Fecha: {servicio['fecha']}" + Style.RESET_ALL)
        print(Fore.YELLOW + "───────────────────────────────────" + Style.RESET_ALL)
    
    print(Fore.YELLOW + f"\nTotal de servicios encontrados: {len(servicios_ayer)}" + Style.RESET_ALL)
        

''' Funcion para generar reporte de servicios realizados la ultima semana '''
def reporte_semana():
    '''Reporte de servicios de la última semana'''
    try:
        with open("serv.json", "r") as file:
            servicios = json.load(file)
    except FileNotFoundError:
        print(Fore.RED + "No se encontró el archivo de servicios." + Style.RESET_ALL)
        return
        
    print(Fore.YELLOW + "\n#### REPORTE DE SERVICIOS DE LA ÚLTIMA SEMANA ####\n" + Style.RESET_ALL)
    
    # Obtener fecha de hace una semana
    fecha_inicio = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    fecha_fin = datetime.now().strftime("%Y-%m-%d")
    
    # Filtrar servicios de la última semana
    servicios_semana = []
    for patente, lista_servicios in servicios.items():
        for servicio in lista_servicios:
            fecha_servicio = servicio['fecha'].split()[0] # Obtener solo la fecha sin hora
            if fecha_servicio >= fecha_inicio and fecha_servicio <= fecha_fin:
                servicio['patente'] = patente
                servicios_semana.append(servicio)
    
    if not servicios_semana:
        print(Fore.YELLOW + f"No se encontraron servicios realizados entre {fecha_inicio} y {fecha_fin}" + Style.RESET_ALL)
        return
        
    print(Fore.YELLOW + f"Servicios realizados entre {fecha_inicio} y {fecha_fin}:" + Style.RESET_ALL)
    print(Fore.YELLOW + "═══════════════════════════════════════" + Style.RESET_ALL)
    for servicio in servicios_semana:
        print(Fore.YELLOW + f"Patente: {servicio['patente']}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Descripción: {servicio['descripcion']}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Fecha: {servicio['fecha']}" + Style.RESET_ALL)
        print(Fore.YELLOW + "───────────────────────────────────" + Style.RESET_ALL)
    
    print(Fore.YELLOW + f"\nTotal de servicios encontrados: {len(servicios_semana)}" + Style.RESET_ALL)


''' Funcion para generar reporte de estadisticas '''
def estadistica():
    '''Reporte estadístico de servicios'''
    print(Fore.YELLOW + "\n#### REPORTE ESTADÍSTICO ####\n" + Style.RESET_ALL)
    
    # Cargar el archivo de servicios
    try:
        with open("serv.json", "r") as file:
            servicios = json.load(file)
    except FileNotFoundError:
        print(Fore.RED + "No se encontró el archivo de servicios." + Style.RESET_ALL)
        return

    # Calcular el total de servicios
    total_servicios = sum(len(servicios[patente]) for patente in servicios)
    if total_servicios == 0:
        print(Fore.YELLOW + "No hay servicios registrados para generar estadísticas." + Style.RESET_ALL)
        return
    
    # Contadores por patente (vehículo), por mes, y por otros atributos relevantes
    servicios_por_patente = {}
    servicios_por_mes = {}
    
    for patente, lista_servicios in servicios.items():
        for servicio in lista_servicios:
            # Contar servicios por patente
            if patente not in servicios_por_patente:
                servicios_por_patente[patente] = 0
            servicios_por_patente[patente] += 1
            
            # Contar servicios por mes
            try:
                fecha = datetime.strptime(servicio['fecha'], "%Y-%m-%d %H:%M:%S")
                mes = fecha.strftime("%B %Y")
                if mes not in servicios_por_mes:
                    servicios_por_mes[mes] = 0
                servicios_por_mes[mes] += 1
            except ValueError:
                pass  # Si la fecha no es válida, se omite

    # Mostrar estadísticas
    print(Fore.YELLOW + f"Total de servicios registrados: {total_servicios}" + Style.RESET_ALL)
    
    # Servicios por patente (vehículo)
    print(Fore.YELLOW + "\nServicios por patente (vehículo):" + Style.RESET_ALL)
    for patente, cantidad in servicios_por_patente.items():
        print(Fore.YELLOW + f"{patente}: {cantidad}" + Style.RESET_ALL)
    
    # Servicios por mes
    print(Fore.YELLOW + "\nServicios por mes:" + Style.RESET_ALL)
    for mes, cantidad in servicios_por_mes.items():
        print(Fore.YELLOW + f"{mes}: {cantidad}" + Style.RESET_ALL)


'''Función para generar solicitudes/tickets para revisión de administradores'''
def generar_solicitud():
    
    print(Fore.YELLOW + "\n#### Generación de Nueva Solicitud ####\n" + Style.RESET_ALL)
    # Cargar los tickets existentes desde el archivo JSON
    try:
        with open("tickets.json", "r") as file:
            tickets = json.load(file)
    except FileNotFoundError:
        tickets = {}  # Si no existe el archivo, inicializar un diccionario vacío

    # Obtener información de la solicitud
    descripcion = input(Fore.CYAN + "Ingrese la descripción detallada de la solicitud: " + Style.RESET_ALL)
    
    # Generar número de ticket
    numero_ticket = len(tickets) + 1
    
    # Crear el ticket
    tickets[numero_ticket] = {
        "descripcion": descripcion,
        "estado": "ABIERTO",
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Guardar los tickets actualizados en el archivo JSON
    with open("tickets.json", "w") as file:
        json.dump(tickets, file, indent=4)

    print(Fore.GREEN + f"\nSolicitud generada exitosamente. Número de ticket: #{numero_ticket}" + Style.RESET_ALL)
    print(Fore.GREEN + "Un administrador revisará su solicitud a la brevedad." + Style.RESET_ALL)


''' Funcion para gestion de problemas '''
def solicitudes_admin():
    go_back = False
    while not go_back:
        print("\n #### Sistema de Gestión de Tickets #### \n")
        print("1. Listar Tickets ABIERTOS.")
        print("2. Listar todos los Tickets.")
        print("3. Cerrar Ticket.")
        print("0. Volver al menu anterior.")
        
        # Cargar los tickets desde el archivo JSON
        try:
            with open("tickets.json", "r") as file:
                tickets = json.load(file)
        except FileNotFoundError:
            tickets = {} 

        opcion = input(Fore.CYAN + "Seleccione una opción: \n" + Style.RESET_ALL)
        
        if opcion == "1":
            listar_tickets_abiertos(tickets) 
        elif opcion == "2":
            listar_tickets(tickets) 
        elif opcion == "3":
            cerrar_ticket(tickets)
        elif opcion == "0":
            print(Fore.YELLOW + "Volviendo al menu anterior..." + Style.RESET_ALL)
            go_back = True
        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente." + Style.RESET_ALL)
        
        # Guardar los tickets actualizados al archivo JSON
        with open("tickets.json", "w") as file:
            json.dump(tickets, file, indent=4)


''' Función para listar tickets ABIERTOS '''
def listar_tickets_abiertos(tickets):
    print("Listado de Tickets Abiertos:")
    for numero, info in tickets.items():
        if info["estado"] == "ABIERTO":
            print(f"Ticket #{numero}: {info['descripcion']} - estado: {info['estado']} - fecha: {info['fecha']}")
    print("###############")


''' Función para listar todos los tickets '''
def listar_tickets(tickets):
    print("Listado de Todos los Tickets:")
    for numero, info in tickets.items():
        print(f"Ticket #{numero}: {info['descripcion']} - Estado: {info['estado']} - Fecha: {info['fecha']}")
    
    print("###############")


''' Función para cerrar un ticket '''
def cerrar_ticket(tickets):
    # Filtrar los tickets abiertos
    tickets_abiertos = {num: info for num, info in tickets.items() if info["estado"] == "ABIERTO"}

    if not tickets_abiertos:
        print("No hay tickets abiertos para cerrar.")
        return

    print("Listado de tickets abiertos:")
    # Mostrar los tickets abiertos con enumerate para facilitar la selección
    for index, (numero, info) in enumerate(tickets_abiertos.items(), 1):
        print(f"{index}. Ticket #{numero}: {info['descripcion']} - Estado: {info['estado']}")

    # Solicitar al usuario que seleccione el ticket a cerrar
    try:
        seleccion = int(input("Seleccione el número del ticket a cerrar: "))
        # Obtener el ticket seleccionado
        ticket_seleccionado = list(tickets_abiertos.items())[seleccion - 1]
        numero_ticket = ticket_seleccionado[0]

        # Cambiar el estado del ticket a "CERRADO"
        tickets[numero_ticket]["estado"] = "CERRADO"
        
        # Actualizar el archivo JSON con el estado cambiado
        with open("tickets.json", "w") as file:
            json.dump(tickets, file, indent=4)

        print(f"Ticket #{numero_ticket} cerrado exitosamente.")
    except (ValueError, IndexError):
        print("Selección inválida. Por favor, elija un número válido.")


def buscar_por_patente(patente, servicios, matrizAutos):
    '''Función que busca una patente y muestra sus servicios y datos del vehículo'''
    patente = patente.upper()
    vehiculo_encontrado = False
    
    # Buscar el vehículo en matrizAutos
    for vehiculo in matrizAutos:
        if vehiculo[3] == patente:
            vehiculo_encontrado = True
            print(f"\nDatos del vehículo:")
            print(f"Marca: {vehiculo[0]}")
            print(f"Modelo: {vehiculo[1]}")
            print(f"Año: {vehiculo[2]}")
            print(f"Kilómetros: {vehiculo[4]}")
            
    # Buscar servicios asociados
    if patente in servicios:
        print(f"\nServicios realizados:")
        print(f"Servicio: {servicios[patente]['servicio']}")
    else:
        print("No se encontraron servicios registrados para esta patente")
        
    if not vehiculo_encontrado:
        print(f"No se encontró un vehículo con la patente {patente}")


'''Función que busca los vehículos asignados a un cliente'''
def buscar_por_cliente(nombre_cliente, matrizAutos):
    nombre_cliente = nombre_cliente.upper()
    vehiculos_cliente = []
    
    # Buscar vehículos del cliente
    for vehiculo in matrizAutos:
        if vehiculo[0] == nombre_cliente: 
            vehiculos_cliente.append(vehiculo)
    
    if vehiculos_cliente:
        print(f"\nVehículos registrados para {nombre_cliente}:")
        for v in vehiculos_cliente:
            print(f"Patente: {v[3]} - Marca: {v[0]} - Modelo: {v[1]} - Año: {v[2]} - Kilómetros: {v[4]}")
    else:
        print(f"No se encontraron vehículos registrados para {nombre_cliente}")


''' Funcion para actualizar mantenimientos por marca '''
def actualizar_mantenimientos():
    try:
        # Cargar datos del archivo JSON
        with open("mantenimientos.json", "r") as file:
            mantenimientos = json.load(file)
    except FileNotFoundError:
        # Si el archivo no existe, inicializar un diccionario vacío
        mantenimientos = {}
        print("Archivo de mantenimiento no encontrado. Se inicializa uno nuevo.")

    bucle_while = True
    while bucle_while == True:
        print("\n--- Menú de Actualización de Mantenimientos ---")
        print("1. Agregar nueva marca")
        print("2. Modificar marca existente")
        print("3. Mostrar listado")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            ''' Agregar una nueva marca '''
            nueva_marca = input("Ingrese el nombre de la nueva marca: ").strip().upper()
            if nueva_marca in mantenimientos:
                print(f"La marca {nueva_marca} ya existe con mantenimiento cada {mantenimientos[nueva_marca]} kilómetros.")
            else:
                try:
                    nuevo_kilometraje = int(input("Ingrese los kilómetros de mantenimiento: ").strip())
                    mantenimientos[nueva_marca] = nuevo_kilometraje
                    with open("mantenimientos.json", "w") as file:
                        json.dump(mantenimientos, file, indent=4)
                    print(f"Marca {nueva_marca} agregada exitosamente.")
                except ValueError:
                    print("Kilómetros inválidos. Por favor, ingrese un número.")

        elif opcion == "2":
            ''' Modificar una marca existente '''
            if len(mantenimientos) == 0:
                print("No hay marcas en el listado para modificar.")
            else:              
                print("\nListado de marcas:")
                for idx, (marca, km) in enumerate(mantenimientos.items(), 1):
                    print(f"{idx}. {marca}: {km} kilómetros")
                
                try:
                    seleccion = int(input("Seleccione el número de la marca a modificar: ").strip())
                    if 1 <= seleccion <= len(mantenimientos):
                        marca_seleccionada = list(mantenimientos.keys())[seleccion - 1]
                        print(f"Marca seleccionada: {marca_seleccionada} (Mantenimiento actual: {mantenimientos[marca_seleccionada]} kilómetros)")
                        nuevo_kilometraje = int(input("Ingrese los nuevos kilómetros de mantenimiento: ").strip())
                        mantenimientos[marca_seleccionada] = nuevo_kilometraje
                        print(f"Kilometraje de {marca_seleccionada} actualizado a {nuevo_kilometraje} kilómetros.")

                        with open("mantenimientos.json", "w") as file:
                            json.dump(mantenimientos, file, indent=4)
                        print("Cambios guardados exitosamente.")
                    else:
                        print("Selección inválida.")
                except ValueError:
                    print("Por favor, ingrese un número válido.")
        
        elif opcion == "3":
            # Mostrar listado
            if len(mantenimientos) == 0:
                print("No hay marcas en el listado.")
            else:
                print("\nListado de marcas:")
                for marca, km in mantenimientos.items():
                    print(f"- {marca}: {km} kilómetros")
        
        elif opcion == "0":
            # Salir del menú
            print("Guardando cambios y saliendo...")
            return
                    
        else:
            print("Opción inválida. Intente nuevamente.")
    

''' Funcion menu principal '''
def main_menu(usuario,perfil):

    desloguearse = False
    
    while desloguearse == False:
        
        input(Fore.CYAN + "\nPresione ENTER para continuar..." + Style.RESET_ALL)
        print("\n" + "#"*50)
        print(f"#### Bienvenido {usuario} al Sistema de Seguimiento de Taller Mecánico ####")
        print("#"*50 + "\n")
        
        if perfil == "admin":
            print("═══════════════════════════════════════")
            print("            MENÚ PRINCIPAL (ADMIN)     ")
            print("═══════════════════════════════════════")
            print("  1. Alta Usuario           2. Listar Usuarios           3. Baja usuario")
            print("  4. Desbloquear usuario    5. Cambiar password usuario")
            print("  6. Alta Vehículo          7. Listar Vehículos          8. Modificar Vehículo")
            print("  9. Buscar vehículo por patente y ver servicios realizados y proximo mantenimiento")
            print(" 10. Cargar Servicio Realizado            11. Listar Servicios Realizados")
            print(" 12. Generar reporte de servicios realizados ayer")
            print(" 13. Generar reporte de servicios realizados la última semana")
            print(" 14. Generar reporte estadístico")
            print(" 15. Reportar un problema a los administradores")
            print(" 16. Ingresar a Menú de problemas reportados")
            print(" 17. Actualizar kilometraje de mantenimiento segun marca")
            print("═══════════════════════════════════════")
            print("  99. Desloguearse")
            print("  0. Salir del sistema")
            print("═══════════════════════════════════════")
            opcion = input("Seleccione una opción: \n")
            
        elif perfil == "mecanico":
            print("═══════════════════════════════════════")
            print("            MENÚ PRINCIPAL (MECÁNICO)  ")
            print("═══════════════════════════════════════")
            print("  6. Alta Vehículo             7. Listar Vehículos")
            print("  9. Buscar vehículo por patente y ver servicios realizados y proximo mantenimiento")
            print(" 10. Cargar Servicio Realizado")
            print(" 11. Listar Servicios Realizados")
            print(" 12. Generar reporte de servicios realizados ayer")
            print(" 13. Generar reporte de servicios realizados la última semana")
            print(" 14. Generar reporte estadístico")
            print(" 15. Reportar un problema a los administradores")
            print(" 16. Ingresar a Menú de problemas reportados")
            print("═══════════════════════════════════════")
            print("  99. Desloguearse")
            print("  0. Salir del sistema")
            print("═══════════════════════════════════════")
            opcion = input("Seleccione una opción: \n")

        # Procesamiento de opciones 
        if opcion == "1" and perfil == "admin":
            alta_usuario(usuarios)
        elif opcion == "2" and perfil == "admin":
            lista_usuarios(usuarios)
        elif opcion == "3" and perfil == "admin":
            baja_usuario()
        elif opcion == "4" and perfil == "admin":
            desbloqueo_usuario(usuarios)
        elif opcion == "5" and perfil == "admin":
            cambio_password(usuarios)
        elif opcion == "6":
            registroVehiculos(matrizAutos)
        elif opcion == "7":
            listarVehiculos(matrizAutos)
        elif opcion == "8" and perfil == "admin":
            modificar_vehiculo(matrizAutos)
        elif opcion == "9":
            servicio_por_patente(matrizAutos)
        elif opcion == "10":
            carga_servicio_realizado(matrizAutos)
        elif opcion == "11":
            lista_servicios_realizados(matrizAutos)
        elif opcion == "12":
            reporte_ayer()
        elif opcion == "13":
            reporte_semana()
        elif opcion == "14":
            estadistica()
        elif opcion == "15":
            generar_solicitud()
        elif opcion == "16" and perfil == "admin":
            solicitudes_admin()
        elif opcion == "17" and perfil == "admin":
            actualizar_mantenimientos()
        elif opcion == "99":
            print("\nDeslogueando... Volviendo a la pantalla de login.")
            desloguearse = True 
        elif opcion == "0":
            print("\nSaliendo del sistema...")
            return True  # Devuelve True para salir completamente del programa
        else:
            print("\nOpción no válida. Intente nuevamente.")


    ### ### ### ### ### ### 


''' Ejecutar el menú principal '''
if __name__ == "__main__":


    matrizAutos = [
    ['FIAT', 'PALIO', 1999, 'CVD234', 276543, 'juan', 'juan@fakemail.com'],
    ['CHEVROLET', 'CORSA II', 1997, 'BVD264', 336543, 'pedro', 'pedro@fakemail.com'],
    ['CITROEN', 'C3', 2014, 'MNM323', 143523, 'pablo', 'pablo@fakemail.com'],
    ['FORD', 'FIESTA', 2005, 'RWP456', 123456, 'laura', 'laura@fakemail.com'],
    ['VOLKSWAGEN', 'GOLF', 2012, 'GBV789', 987654, 'carlos', 'carlos@fakemail.com'],
    ['TOYOTA', 'COROLLA', 2010, 'TYC567', 765432, 'lucía', 'lucia@fakemail.com'],
    ['RENAULT', 'CLIO', 2008, 'RLC998', 432765, 'marta', 'marta@fakemail.com'],
    ['PEUGEOT', '208', 2016, 'PEU123', 356897, 'ricardo', 'ricardo@fakemail.com'],
    ['NISSAN', 'X-TRAIL', 2017, 'NXT432', 654321, 'ana', 'ana@fakemail.com'],
    ['HONDA', 'CIVIC', 2015, 'HDC654', 341256, 'jorge', 'jorge@fakemail.com'],
    ['BMW', 'SERIE 3', 2013, 'BMW221', 423658, 'claudia', 'claudia@fakemail.com'],
    ['MAZDA', 'CX-5', 2016, 'MZC112', 876543, 'luis', 'luis@fakemail.com'],
    ['CHERY', 'TIGGO', 2010, 'CHT123', 124563, 'silvia', 'silvia@fakemail.com'],
    ['HYUNDAI', 'ELANTRA', 2018, 'HYC987', 213459, 'martín', 'martin@fakemail.com'],
    ['KIA', 'SPORTAGE', 2019, 'KIA543', 654321, 'gabriela', 'gabriela@fakemail.com'],
    ['AUDI', 'A4', 2023, 'AB123CD', 15000, 'diego', 'diego@fakemail.com'],
    ['MERCEDES-BENZ', 'C-CLASS', 2023, 'EF456GH', 12000, 'valeria', 'valeria@fakemail.com'],
    ['TESLA', 'MODEL 3', 2024, 'IJ789KL', 8000, 'sofia', 'sofia@fakemail.com'],
    ['VOLVO', 'XC90', 2024, 'MN012OP', 6000, 'gabriel', 'gabriel@fakemail.com'],
    ['BMW', 'X5', 2023, 'PQ345RS', 5000, 'camila', 'camila@fakemail.com'],
    ['JEEP', 'GRAND CHEROKEE', 2024, 'TU678VW', 4500, 'martin', 'martin@fakemail.com'],
    ['HONDA', 'HR-V', 2024, 'XY234ZA', 3500, 'roberto', 'roberto@fakemail.com'],
    ['MITSUBISHI', 'OUTLANDER', 2023, 'AB456CD', 10000, 'victor', 'victor@fakemail.com'],
    ['PORSCHE', 'MACAN', 2023, 'EF789GH', 12000, 'lucas', 'lucas@fakemail.com'],
    ['TOYOTA', 'RAV4', 2024, 'IJ012KL', 8000, 'mario', 'mario@fakemail.com']
    ]
    
    login_y_menu()


# ############################

# 80%
# Regex para el ingreso de datos (por ejemplo el formato de patente). LISTO
# Upper para el ingreso de datos, se guardará toda la información en mayúsculas. LISTO
# Mejorar en los datos que estamos registrando, por ejemplo agregar nombre y mail del titular (evaluar necesidades y realizar actualización). LISTO
# Usuario bloqueado por password erronea (3 intentos) y desbloqueo de usuario desde perfil Admin unicamente. LISTO
# Funciones de búsqueda por patente y cliente - LISTO  

# Modificación de datos de cliente y titularidad del vehículo. LISTO
# Cálculos de mantenimientos repetitivos por kms y tiempo (calcular con los kms actuales y el año de fabricación cuando le toca volver). LISTO (opcion 9)
# Para el punto anterior ver que recomienda cada fabricante, por ejemplo VW cada 15000 kms y Citroen cada 10000 kms. LISTO
# Otros mantenimientos (aceite y filtro, frenos, cubiertas, alineación y balanceo etc) - (Evaluar si usar texto libre o algunas opciones predefinidas para el ingreso de los servicios al sistema). TEXTO LIBRE
# Pruebas unitarias. LISTO
# Agregar libreria de color. LISTO

# 100%
# Manejo de archivos (persistencia de datos). LISTO // falta el manejo de archivo para autos
# Reporte servicios realizados en la semana o el día. LISTO
# Reporte de vehículos con servicios a vencer/vencidos. (NO EXISTE TODAVIA)
# Reporte de estadísticas, cantidad de servicios, modelos de vehículos, etc. LISTO
# Sistema de tickets para perfiles Admin donde se puedan reportar errores, problemas, mejoras. (al acceder como administrador nos muestra una lista de situaciones reportadas). LISTO   
# Solucionar cualquier problema que veamos en las pruebas. (Consultar con el docente)

# ############################

# ------------------------------------------------------------------------------------------------
# cuando se carga un servicio con km negativos se guarda el servicio y cuando listamos los servicios se carga la descripcion pero no los km

