#region Librerias
from collections import namedtuple
import re
import os
import datetime
from datetime import datetime as dt
import sys
import csv
from prettytable import PrettyTable
#endregion

# region Declaracion de variables
LimpiarPantalla = lambda: os.system('cls')
Producto = namedtuple("Producto", ("descripcion", "cantidad", "precio"))
monto_total = 0
diccionario_ventas = {}
regexLetras = "^[a-zA-Z ]+$"
lista_productos = []
#endregion

#region Metodos

def separador():
    print("*" * 20)

def registrarVenta():
    lista_productos = []
    global monto_total
    monto_total = 0
    switch = True
    clave = int(input("Ingrese la clave de la venta: "))
    if clave in diccionario_ventas.keys():
        print("Esa clave ya está registrada, intente de nuevo. ")
        input("Pulse enter para continuar... ")
    else:
        while switch:
            while True:
                descripcion = input("Ingrese la descripción del producto: ")
                if descripcion == "":
                    print("Este dato no puede ser vacío")
                else:
                    break

            while True:
                try:
                    cantidad = int(input("Ingrese la cantidad del producto: "))
                except Exception:
                    print(f"Ocurrió un problema, debe ingresar un dato numérico entero: {sys.exc_info()[0]}")
                    input("Pulse enter para continuar... ")
                else:
                    break

            while True:
                try:
                    precio = float(input("Ingrese el precio del producto: "))
                except Exception:
                    print(f"Ocurrió un problema, debe ingresar un dato numérico de tipo entero o float: {sys.exc_info()[0]}")
                    input("Pulse enter para continuar... ")
                else:
                    break

            # Luego de capturar, se realiza la instancia de los datos en una tupla nominada,
            # se almacena en un diccionario y se actualiza la variable monto.
            producto_registrado = Producto(descripcion, cantidad, precio)
            lista_productos.append(producto_registrado)
            monto = (cantidad * precio)
            monto_total = monto_total + monto

            # Se pregunta al usuario si desea seguir capturando otro producto
            while True:
                respuesta = input("¿Desea agregar otro producto? [S/N]: ")
                if respuesta.upper() == "S":
                    LimpiarPantalla()
                    break
                elif respuesta.upper() == "N":
                    switch = False
                    # Si ya no desea capturar, se imprime el calculo del monto total e IVA
                    LimpiarPantalla()
                    fecha_procesada = dt.today().strftime('%d/%m/%Y')
                    IVA = (monto_total * 0.16)
                    print(f'El monto total a pagar es: {"${:,.2f}".format((monto_total + IVA))}')
                    print(f'El IVA aplicado del 16% es: {"${:,.2f}".format((IVA))}')
                    # Se agregan los productos registrados al diccionario principal, y el monto total se guarda
                    # tambien en un diccionario con los montos totales de las ventas para futuro despliegue
                    ruta = os.path.abspath(os.getcwd())
                    archivo_trabajo = ruta + "\\registro_ventas.csv"

                    lista_copia = lista_productos.copy()
                    diccionario_ventas[clave] = (lista_copia,fecha_procesada)
                    lista_productos.clear()
                    monto_total = 0
                    input("Pulse enter para continuar... ")
                    break
                else:
                    print("Error. Opcion no válida!")


def consultarVenta():
    LimpiarPantalla()
    monto_total_consulta = 0
    busqueda = int(input("Ingrese la clave de venta a buscar: "))

    # Luego de capturar que busqueda desea realizar el usuario,s
    # Se busca la clave en el diccionario y luego se imprimen los dato
    if busqueda in diccionario_ventas.keys():

        # diccionario_ventas[busqueda][0] es para especificar el campo
        # ya que es un diccionario de tuplas (Producto, fecha)
        # en el que Producto equivale a la posicion 0
        for producto in diccionario_ventas[busqueda][0]:
            separador()
            print(f"\nLa descripción del producto es: {producto[0]}")
            print(f"La cantidad del producto: {producto[1]}")
            print(f"El precio unitario del producto es: {producto[2]}")
            monto = producto[1] * producto[2]
            monto_total_consulta = monto_total_consulta + monto
        print(f"La fecha de venta fue: {diccionario_ventas[busqueda][1]}")
        IVA = monto_total_consulta * 0.16
        print(f"El monto total de la venta fue: {'${:,.2f}'.format(monto_total_consulta + IVA)}")
        print(f"El IVA aplicado del 16% fue: {'${:,.2f}'.format(IVA)}\n")
        separador()
        input("Pulse enter para continuar... ")
    else:
        print("Clave no registrada. ")
        input("Pulse enter para continuar... ")

def consultarVenta_porFecha():
    LimpiarPantalla()
    fecha_buscar = input("Ingrese la fecha a buscar en formato DD/MM/AAAA: ")
    for clave in diccionario_ventas.keys():
        monto_total_consulta = 0
        if fecha_buscar == diccionario_ventas[clave][1]:
            separador()
            print(f"CLAVE: {clave}")
            t = PrettyTable(['Descripcion','Cantidad', 'Precio'])
            for producto in diccionario_ventas[clave][0]:
                t.add_row([producto[0],producto[1],producto[2]])
                monto = producto[1] * producto[2]
                monto_total_consulta = monto_total_consulta + monto
            print(t)
            print(f"\nFecha de venta: {diccionario_ventas[clave][1]}")
            IVA = monto_total_consulta * 0.16
            print(f"Monto total: {'${:,.2f}'.format(monto_total_consulta + IVA)}")
            print(f"El IVA aplicado del 16% fue: {'${:,.2f}'.format(IVA)}")
            separador()
        else:
            print("No hay ventas en la fecha buscada.")
            input("Pulse enter para continuar... ")
    else:
        input("\nPulse enter para continuar... ")

def guardarCSV():
    LimpiarPantalla()
    file_exists = os.path.isfile('registro_ventas.csv')
    # Si el archivo existe, se abre y se sobrescribe la informacion
    if file_exists:
        with open('registro_ventas.csv', mode='w+', newline='') as archivo_trabajo:
                grabador = csv.writer(archivo_trabajo, delimiter=',')
                grabador.writerow(['CLAVE_VENTA', 'DESCRIPCION', 'CANTIDAD', 'PRECIO', 'FECHA'])
                for clave in diccionario_ventas.keys():
                    fecha_csv = diccionario_ventas[clave][1]
                    for producto in diccionario_ventas[clave][0]:
                        descripcion_csv = producto[0]
                        cantidad_csv = producto[1]
                        precio_csv = producto[2]
                        grabador.writerow([clave, descripcion_csv, cantidad_csv, precio_csv, fecha_csv])
    else:
        # Si el archivo no existe se crea incluyendo los encabezados
        with open('registro_ventas.csv', mode='w', newline='') as archivo_trabajo:
                grabador = csv.writer(archivo_trabajo, delimiter=',')
                grabador.writerow(['CLAVE_VENTA', 'DESCRIPCION', 'CANTIDAD', 'PRECIO', 'FECHA'])
                for clave in diccionario_ventas.keys():
                    fecha_csv = diccionario_ventas[clave][1]
                    for producto in diccionario_ventas[clave][0]:
                        descripcion_csv = producto[0]
                        cantidad_csv = producto[1]
                        precio_csv = producto[2]
                        grabador.writerow([clave, descripcion_csv, cantidad_csv, precio_csv, fecha_csv])
    archivo_trabajo.close()
    print("Los datos se han cargado a CSV. ")
    print("Saldrás del sistema!")


def cargarCSV():
    try:
        with open('registro_ventas.csv', newline='') as csv_doc:
            archivo_csv = csv.reader(csv_doc, delimiter=',')
            next(archivo_csv)
            contador = 1
            for linea in csv_doc:
                registro = linea.split(",") #Lista
                print(registro)
                if linea[0] == str(contador):
                    clave = int(registro[0])
                    descripcion = registro[1]
                    cantidad = int(registro[2])
                    precio = float(registro[3])
                    fecha = registro[4]
                    fecha = fecha.replace("\r\n","")
                    producto_registrado = Producto(descripcion, cantidad, precio)
                    lista_productos.append(producto_registrado)
                else:
                    diccionario_ventas[clave] = (lista_productos.copy(),fecha)
                    lista_productos.clear()

                    clave = int(registro[0])
                    descripcion = registro[1]
                    cantidad = int(registro[2])
                    precio = float(registro[3])
                    fecha = registro[4]
                    fecha = fecha.replace("\r\n","")
                    producto_registrado = Producto(descripcion, cantidad, precio)
                    lista_productos.append(producto_registrado)
                    contador = contador + 1
            else:
                diccionario_ventas[clave] = (lista_productos.copy(),fecha)
    except:
        pass




def main():
    cargarCSV()
    while True:
        LimpiarPantalla()
        print("***MENU VENTA***")
        print("¿Qué desea hacer?")
        print("1: Registrar Venta")
        print("2: Consultar Venta")
        print("3: Reporte de ventas a partir de una fecha")
        print("4: Salir")
        try:
            opcion = int(input("Ingrese una opción: "))
            if opcion == 1:
                registrarVenta()
            elif opcion == 2:
                consultarVenta()
            elif opcion == 3:
                consultarVenta_porFecha()
            elif opcion == 4:
                guardarCSV()
                break
            else:
                print("Opcion no valida")
                input("Pulse enter para continuar... ")
        except ValueError:
            print('Ingrese un dato numérico entero. ')
            input("Pulse enter para continuar... ")
#endregion

# Se manda a llamar el metodo Main
main()