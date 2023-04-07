# Administrador de recetas de comidas
import os
from pathlib import Path
import ast # para convertir una string en forma de objeto a objeto
# para limpiar la consola
import platform
from shutil import rmtree
import sys
from fpdf import FPDF # para generar el archivo pdf de las recetas
import webbrowser
import time
# Variables


# Funciones
def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def cargar_BD_base():
    ruta_bd_categorias = Path(Path.home(), "Recetas", "BD_Categorias.txt")
    ruta_bd_recetas = Path(Path.home(), "Recetas", "BD_Recetas.txt")
    categorias = []
    recetas = []
    if ruta_bd_categorias.exists():
        data = open(ruta_bd_categorias)
        for item in data:
            categorias.append(item.rstrip())
        data.close()
    
    if ruta_bd_recetas.exists():
        data = open(ruta_bd_recetas)
        for item in data:
            recetas.append(ast.literal_eval(item.rstrip()))
        data.close()
    
    return categorias, recetas
              
def crear_directorio_base():
    ruta_copia_seguridad = Path(Path.home(), "Recetas", "copia_de_seguridad")
    
    ruta_home = Path.home()
    ruta_recetas = Path(ruta_home, "Recetas")
    if not ruta_recetas.exists():
        os.makedirs(ruta_recetas)
        os.makedirs(ruta_copia_seguridad)
    # creacion del archivo de la base de datos de recetas
    ruta_bd_recetas = Path(Path.home(), "Recetas", "BD_Recetas.txt")
    if not ruta_bd_recetas.exists():
        archivo_bd_recetas = open(ruta_bd_recetas,"w")
        datos_base = str({"nombre": "pizza hawaiiana", "procedimiento": "mezclar, hornear y comer", "ingredientes": ["polvo para hornear", "salsa de tomate", "queso parmesano","trozos de piña"], "categoria": "Carnes"})
        archivo_bd_recetas.write(datos_base + "\n")
        archivo_bd_recetas.close()
    # creacion del archivo de la base de datos de categorias
    ruta_bd_categorias = Path(Path.home(), "Recetas", "BD_Categorias.txt")
    if not ruta_bd_categorias.exists():
        archivo_bd_categorias = open(ruta_bd_categorias,"w")
        datos_base = ["Carnes", "Ensaladas", "Pastas", "Postres", "Bebidas"]
        for item in datos_base:
            archivo_bd_categorias.write(item + "\n")
        archivo_bd_categorias.close()

def crear_carpetas_categorias():
    categorias = consultar_bd_categorias()
    for cat in categorias:
        ruta_cat = Path(Path.home(), "Recetas", cat)
        if not ruta_cat.exists():
            os.makedirs(ruta_cat)
        
def crear_archivos_recetas():
    
    recetas = consultar_bd_recetas()
    for receta in recetas:
        nombre = receta["nombre"]
        procedimiento = receta["procedimiento"]
        ingredientes = receta["ingredientes"]
        categoria = receta["categoria"]
        ruta_receta = Path(Path.home(), "Recetas")
        ruta_receta = Path(ruta_receta, categoria, nombre + ".txt")
        if not ruta_receta.exists():
            archivo_receta = open(ruta_receta, "w")
            archivo_receta.write(nombre.title() + "\n")
            archivo_receta.write("\n")
            archivo_receta.write("Ingredientes: \n")
            for item in ingredientes:
                archivo_receta.write("- " + item.title() + "\n")
            archivo_receta.write("\n")
            archivo_receta.write("Procedimiento: \n")
            archivo_receta.write(procedimiento + "\n")
            archivo_receta.write("\n")
            archivo_receta.write("Categoria: \n")
            archivo_receta.write(categoria + "\n")
            archivo_receta.close()
          
def guardar_receta(nueva_receta):
    nombre = nueva_receta["nombre"]
    procedimiento = nueva_receta["procedimiento"]
    ingredientes = nueva_receta["ingredientes"]
    categoria = nueva_receta["categoria"]
    bd_recetas = Path(Path.home(), "Recetas", "BD_Recetas.txt")
    bd = open(bd_recetas,"a")
    bd.write(str(nueva_receta) + "\n")
    bd.close()
    crear_archivos_recetas()

def consultar_bd_recetas():
    ruta = Path(Path.home(),"Recetas", "BD_Recetas.txt")
    data = open(ruta)
    recetas = []
    for receta in data:
        recetas.append(ast.literal_eval(receta.rstrip()))
    data.close()
    return recetas
    
def consultar_bd_categorias():
    ruta = Path(Path.home(),"Recetas", "BD_Categorias.txt")
    data = open(ruta)
    categorias = []
    for item in data:
        categorias.append(item.rstrip())
    data.close()
    return categorias

def crear_receta():
    ruta_categorias = Path(Path.home(),"Recetas","BD_Categorias.txt")
    archivo_categorias = open(ruta_categorias)
    categorias = []
    for item in archivo_categorias:
        categorias.append(item.rstrip())
    archivo_categorias.close()
    categoria_seleccionada = ""
    entrada_incorrecta = True
    nombre_receta = ""
    procedimiento = ""
    ingredientes = []
    añadir_ingredientes = True
    print("crear receta".title())
    for indice, categoria in enumerate(categorias): 
        print(f"[{indice + 1}]- {categoria}")
    print(f"[{len(categorias) + 1}] Volver al menu principal") 
    while entrada_incorrecta:
        entrada_usuario = input("selecciona la categoria:\t")
        if entrada_usuario.isdecimal():
            entrada_usuario = int(entrada_usuario)
            if entrada_usuario == len(categorias) + 1:
                volver()
            else:
                if entrada_usuario in range(1, len(categorias) + 1):
                    categoria_seleccionada = categorias[entrada_usuario - 1]
                    entrada_incorrecta = False
                else:
                    entrada_incorrecta = True
        else:
            entrada_incorrecta = True
    limpiar_pantalla()
    print(f"Tu nueva receta pertenece a la categoria {categoria_seleccionada}   ")
    # validacion nombre
    nombre_invalido = True
    recetas = consultar_bd_recetas()
    while nombre_invalido:
        nombre_receta = input("Ingresa el nombre de tu receta:\t")
        if nombre_receta == "" or  nombre_receta.isdigit():
            continue
        else:
            for receta in recetas:
                if receta["nombre"] == nombre_receta:
                    print("la receta ya existe")
                    nombre_invalido = True 
                    break
                else:
                    nombre_invalido = False
    
    print("Añade la lista de ingredientes   ")
    while añadir_ingredientes:
        ingrediente = input("Añadir:\t")
        if ingrediente == "" or ingrediente.isdigit():
            continue
        else:
            ingredientes.append(ingrediente)
        print("¿Deseas añadir otro ingrediente? S/N ")
        
        respuesta = input("Respuesta:\t").lower()
        if not respuesta in "s" or respuesta == "":
            break
    
    while True:
        procedimiento = input(f"describe el procedimiento para preparar {nombre_receta} ")    
        if procedimiento != "" or procedimiento.isdigit():
            break
    
    return {
        "nombre": nombre_receta,
        "procedimiento": procedimiento,
        "ingredientes": ingredientes,
        "categoria": categoria_seleccionada
    }
    
def opciones():
    limpiar_pantalla()
    recetas = open(Path(Path.home(), "Recetas", "BD_Recetas.txt"))
    lista_recetas = []
    for item in recetas:
        lista_recetas.append(ast.literal_eval(item.rstrip()))
    ruta_recetas = Path(Path.home(), "Recetas")
    num_recetas = len(lista_recetas)
    print("Bienvenido, Administra facilmente tus recetas favoritas")
    print(f"Tus recetas estan almacenadas en: {ruta_recetas}")
    
    if num_recetas == 0:
        print("aun no tienes recetas agregadas")
    elif num_recetas == 1:
        print(f"tienes {num_recetas} receta")
    else:
        print(f"tienes {num_recetas} recetas")
    
    print("[1]- Leer Receta")
    print("[2]- Crear Receta")
    print("[3]- Crear Categoria")
    print("[4]- Eliminar Receta")
    print("[5]- Eliminar Categoria")
    print("[6]- Copia de seguridad")
    print("[7]- Salir")

def ejecutar(entrada_usuario):
    if entrada_usuario == '1':
        limpiar_pantalla()
        print("leer receta")
        leer_receta()
    elif entrada_usuario == '2':
        limpiar_pantalla()
        guardar_receta(crear_receta())
        print("Receta creada correctamente")
    elif entrada_usuario == '3':
        limpiar_pantalla()
        crear_categoria()
    elif entrada_usuario == '4':
        limpiar_pantalla()
        print("Eliminar receta")
        eliminar_receta()
        print("Receta eliminada")
    elif entrada_usuario == '5':
        limpiar_pantalla()
        print("Eliminar categoria")
        eliminar_categoria()
        print("Categoria eliminada")
    elif entrada_usuario == '6':
        limpiar_pantalla()
        print("Realizando copia de seguridad...")
        copia_de_seguridad()
        print("copia de seguridad finalizada")
       

def crear_categoria():
    nombre_invalido = True
    categorias = consultar_bd_categorias()
    while nombre_invalido:
        nombre = input("Ingresa el nombre de la categoria   ")
        if len(nombre) > 1 and not nombre.isdigit() and nombre.title() not in categorias:
            # añadir a la bd
            ruta = Path(Path.home(),"Recetas", "BD_Categorias.txt")
            data = open(ruta,'a')
            data.write(nombre.title() + "\n")
            data.close()
            crear_carpetas_categorias()
            print("Categoria guardada correctamente")
            break
        else:
            print("El nombre que ingresaste no es correcto, intenta nuevamente")
            continue

def leer_receta():
    recetas = consultar_bd_recetas()
    categorias = consultar_bd_categorias()
    # filtrar las categorias que tienen recetas
    categorias_con_contenido = []
    for categoria in categorias:
        for receta in recetas:
            if categoria == receta["categoria"]:
                categorias_con_contenido.append(categoria)
            else:
                continue
    categorias_con_contenido = set(categorias_con_contenido)
    categorias_con_contenido = list(categorias_con_contenido)
                             
    entrada_incorrecta = True
    categoria_seleccionada = ""
    while entrada_incorrecta:
        limpiar_pantalla()
        for indice, categoria in enumerate(categorias_con_contenido):
            print(f"[{indice + 1}] {categoria}")
        print(f"[{len(categorias_con_contenido) + 1}] Volver al menu principal")
        entrada_usuario = input("Selecciona la categoria:    ")
        if entrada_usuario.isdecimal():
            entrada_usuario = int(entrada_usuario)
            if entrada_usuario == len(categorias_con_contenido) + 1:
                volver()
            else: 
                if entrada_usuario in range(1, len(categorias_con_contenido) + 1):
                    categoria_seleccionada = categorias_con_contenido[entrada_usuario - 1]
                    entrada_incorrecta = False
                else:
                    entrada_incorrecta = True
        else:
            entrada_incorrecta = True
    limpiar_pantalla()
    print(f"{categoria_seleccionada}")
    # aqui inicia el segundo bloque
    input_incorrecto = True
    receta_seleccionada = ""
    while input_incorrecto:
        limpiar_pantalla()
        recetas_filtradas = [receta["nombre"] for receta in recetas if receta["categoria"] == categoria_seleccionada]
        for indice,item in enumerate(recetas_filtradas):
            print(f"[{indice + 1}] {item}")
        leer = input("Selecciona la receta a leer:  ")
        if leer.isdecimal():
            leer = int(leer)
            if leer in range(1, len(recetas_filtradas) + 1):
                receta_seleccionada = recetas_filtradas[leer - 1]
                input_incorrecto = False
            else:
                input_incorrecto = True
        else:
            input_incorrecto = True
        limpiar_pantalla()
        print("-"*20)
        ruta_receta_seleccionada = Path(Path.home(), "Recetas", categoria_seleccionada, receta_seleccionada + ".txt")
        info_receta_seleccionada = [receta for receta in recetas if receta["nombre"] == receta_seleccionada]
        data_receta = info_receta_seleccionada[0]
        print(data_receta["nombre"].title())
        print("Ingredientes:")
        for ingrediente in data_receta["ingredientes"]:
            print(f"- {ingrediente}")
        print("Proceso de preparacion: ")
        print(data_receta["procedimiento"])
        print("Categoria: ")
        print(data_receta["categoria"])
        print(f"Puedes leer directamente el archivo de tu receta en: {ruta_receta_seleccionada}")        
        print("-"*20)

def eliminar_categoria():
    # leer categoria a eliminar
    categorias = consultar_bd_categorias()
    entrada_incorrecta = True
    categoria_seleccionada = ""
    while entrada_incorrecta:
        limpiar_pantalla()
        for indice, categoria in enumerate(categorias):
            print(f"[{indice + 1}] {categoria}")
        print(f"[{len(categorias) + 1}] Volver al menu principal")
        entrada_usuario = input("Selecciona la categoria a eliminar:    ")
        if entrada_usuario.isdecimal():
            entrada_usuario = int(entrada_usuario)
            if entrada_usuario == len(categorias) + 1:
                volver()
            else:
                if entrada_usuario in range(1, len(categorias) + 1):
                    categoria_seleccionada = categorias[entrada_usuario - 1]
                    entrada_incorrecta = False
                else:
                    entrada_incorrecta = True
        else:
            entrada_incorrecta = True
    limpiar_pantalla()
    print(f"{categoria_seleccionada}")
    # Eliminar recetas con la categoria eliminada
    recetas = consultar_bd_recetas()
    recetas_filtro = [receta for receta in recetas if receta["categoria"] != categoria_seleccionada]
    ruta = Path(Path.home(),"Recetas", "BD_Recetas.txt")
    bd = open(ruta,"w")
    for item in recetas_filtro:
        bd.write(str(item) + "\n")
    bd.close()
    crear_archivos_recetas()
    # Eliminar la categoria
    categorias_filtro = [cat for cat in categorias if cat != categoria_seleccionada]
    ruta = Path(Path.home(),"Recetas", "BD_Categorias.txt")
    bd = open(ruta,"w")
    for item in categorias_filtro:
        bd.write(item.title() + "\n")
    bd.close()
    # remover el directorio
    ruta_categoria_eliminar = Path(Path.home(), "Recetas", categoria_seleccionada)
    rmtree(ruta_categoria_eliminar)
    
def eliminar_receta():
    recetas = consultar_bd_recetas()
    entrada_incorrecta = True
    receta_seleccionada = ""
    while entrada_incorrecta:
        limpiar_pantalla()
        for indice, receta in enumerate(recetas):
            nombre_receta = receta["nombre"]
            print(f"[{indice + 1}] {nombre_receta.title()}")
        print(f"[{len(recetas) + 1}] Volver al menu principal")
        entrada_usuario = input("Selecciona la Receta a eliminar:    ")
        if entrada_usuario.isdecimal():
            entrada_usuario = int(entrada_usuario)
            if entrada_usuario == len(recetas) + 1:
                volver()
            else:
                if entrada_usuario in range(1, len(recetas) + 1):
                    receta_seleccionada = recetas[entrada_usuario - 1]["nombre"]
                    entrada_incorrecta = False
                else:
                    entrada_incorrecta = True
        else:
            entrada_incorrecta = True
    limpiar_pantalla()
    print(receta_seleccionada)
    recetas_filtro = [receta for receta in recetas if receta["nombre"] != receta_seleccionada]
    # Eliminar recetas con la categoria eliminada
    ruta = Path(Path.home(),"Recetas", "BD_Recetas.txt")
    bd = open(ruta,"w")
    for item in recetas_filtro:
        bd.write(str(item) + "\n")
    bd.close()
    info_receta_seleccionada = [receta for receta in recetas if receta_seleccionada == receta["nombre"]]
    ruta_receta_eliminar = Path(Path.home(), "Recetas",info_receta_seleccionada[0]["categoria"] , receta_seleccionada + ".txt")
    os.remove(ruta_receta_eliminar)
    crear_archivos_recetas()
    
def volver():
    iniciar_app()
    
def iniciar_app():
    continuar = True
    while continuar:
        respuesta_incorrecta = True
        while respuesta_incorrecta:
            opciones()
            respuesta_usuario = input("¿Qué te gustaria hacer?\t")
            if respuesta_usuario == '1' or respuesta_usuario == '2' or respuesta_usuario == '3' or respuesta_usuario == '4' or respuesta_usuario == '5' or respuesta_usuario == '6' and len(respuesta_usuario) == 1:
                ejecutar(respuesta_usuario)
                respuesta_incorrecta = False
            elif respuesta_usuario == '7':
                sys.exit() # cerrar programa
            else:
                respuesta_incorrecta = True
        seguir = input("¿Deseas continuar administrando tus recetas? s/n\t")
        if seguir.lower() in "s":
            continuar = True
        else:
            continuar = False
        limpiar_pantalla()

def copia_de_seguridad():
    ruta_copia_seguridad = Path(Path.home(), "Recetas", "copia_de_seguridad")
    if not ruta_copia_seguridad.exists():
        os.makedirs(ruta_copia_seguridad)
    recetas = consultar_bd_recetas()
    pdf = FPDF()
    pdf.set_font("Arial", size=12)
    for receta in recetas:
        nombre = receta['nombre']
        procedimiento = receta['procedimiento']
        ingredientes = receta['ingredientes']
        categoria = receta['categoria']
        cadena_ingredientes = ""
        for ingrediente in ingredientes:
            cadena_ingredientes += f"- {ingrediente}\n"
    
        info = f"Nombre de la Receta:\n{nombre.title()}\n\nProcedimiento:\n{procedimiento}\n\nIngredientes:\n{cadena_ingredientes}\n\nCategoría:\n{categoria}\n\n"
        pdf.add_page()
        pdf.multi_cell(0, 10, info)
        
    ruta_copia_seguridad_archivo = ruta_copia_seguridad / "Recetas"
    if ruta_copia_seguridad_archivo.exists():
        os.remove(ruta_copia_seguridad_archivo)
    pdf.output(ruta_copia_seguridad / "Recetas.pdf")
    print(f"El archivo esta ubicado en: {ruta_copia_seguridad_archivo}")
    ruta_copia_directa = Path(Path.home(),"Recetas", "copia_de_seguridad", "Recetas.pdf")
    print("Abriendo archivo...")
    time.sleep(3)
    webbrowser.open_new(ruta_copia_directa)
    
# Ejecución inicial
limpiar_pantalla()
crear_directorio_base()
crear_carpetas_categorias()
crear_archivos_recetas()


# Ejecución loop
iniciar_app()
    
