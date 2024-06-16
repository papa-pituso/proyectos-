#   programa creado por estudiante autodidacta
#   compartido por creador PAPA-PITUSO
#   el intento es crear un programa sencillo y con los datos necesarios para que sea util en la industria

import tkinter as tk
from tkinter import ttk
import serial
from serial.tools import list_ports
import threading

conectar = None

def obtener_puertos_com():
    puertos_com = [port.device for port in list_ports.comports()]
    return puertos_com

def mostrar_puertos_com():
    combo_puertos['values'] = obtener_puertos_com()
    combo_puertos.set("")

def conectar_puerto(puerto):
    try:
        conectar = serial.Serial(puerto, baudrate=9600, stopbits=1, parity='N', bytesize=8)
        return conectar
    except serial.SerialException as e:
        return None

def desconectar_puerto(conectar):
    if conectar:
        conectar.close()


def recibir_datos():
    global conectar
    while conectar:
        try:
            # en conectar.readline () depende de la bascula sera a 32, 24, o cualquier otro valor para ajustar la velocidad del visor
            
            datos_recibidos = conectar.readline(32).decode("ascii")# otros codigos ("iso-8859-1")("windows-1252")("latin-1")("ascii")("utf-8")
            mostrar(datos_recibidos)
            print(datos_recibidos)
        except serial.SerialException:
            conectar = None
            btn_conectar.config(text="Conectar")
            break

def conectar_o_desconectar():
    global conectar
    if conectar is None:
        puerto_seleccionado = combo_puertos.get()
        conectar = conectar_puerto(puerto_seleccionado)
        if conectar:
            btn_conectar.config(text="Desconectar")
            recibir_datos_thread = threading.Thread(target=recibir_datos)
            recibir_datos_thread.start()
                
    else:
        desconectar_puerto(conectar)
        conectar = None
        btn_conectar.config(text="Conectar")



# Crea la ventana de la interfaz grafica
ventana = tk.Tk(className=" Visor de peso")
ventana.geometry("760x200")
ventana.config(bg="#f3d6c2")

# Etiqueta para mostrar el titulo del proyecto
etiqueta = tk.Label(ventana, text="VISOR DE PESO M. B. O.", font=("Arial", 14), bg="#6b88f9", fg="white")
etiqueta.pack(side=tk.TOP, fill="both")


# Ventana mostrar puertos com
combo_puertos = ttk.Combobox(ventana, state='readonly')
combo_puertos.place(x=5, y=30)

# Botón para actualizar la lista de puertos COM disponibles
btn_actualizar = tk.Button(ventana, text="Actualizar", command=mostrar_puertos_com)
btn_actualizar.place(x=235, y=30)

# Botón para conectarse al puerto COM seleccionado
btn_conectar = tk.Button(ventana, text="Conectar", command=conectar_o_desconectar)
btn_conectar.place(x=155, y=30)

# Actualizar la lista de puertos COM disponibles al abrir la ventana
mostrar_puertos_com()

################################################################################################
# mostramos datod recibidos

def mostrar(datos_recibidos):
   
    id_sen = datos_recibidos[1:2] # obtiene el caracter 1 e ignora el 0
    numero = datos_recibidos[2:10]# obtiene los caracteres del 2 al 19
    
    # seleccionamos ver peso 0 estable o peso en carga estable
    # las basculas epelsa probadas, devuelven A, I, ! o ) dependiendo de estable, 0, pesando, paso a 0
    
    if id_sen == "A" or id_sen == "I": # si se quiere ver el movimiento de los digitos mientras pesa, se elimina este if
        
         label_val_sen1.config(text=numero)# Muestra el valor en la etiqueta si es estable o 0

    # Etiqueta zero

    if id_sen == "I":
        amarillo = "#fff200"
    else:
        amarillo = "#dad790"
    
    zero = tk.Label(ventana, text="-->0<--", font=("arial",20),bg= amarillo)
    zero.place(x=330,y=30)


    # Etiqueta pesando

    if id_sen == "!":
        azul = "#06bff8"
    else:
        azul = "#aadfef"
    pesando = tk.Label(ventana, text="pesando", font=("arial",20),bg= azul)
    pesando.place(x=480,y=30)


    # Etiqueta estable

    if id_sen == "A":
        verde = "#09f64c"
    else:
        verde = "#aaefbe"
    estable = tk.Label(ventana, text="estable", font=("arial",20),bg= verde)
    estable.place(x=650,y=30)



# Etiqueta para mostrar nombre kg
label_sen1 = tk.Label(ventana, text="PESO Kg:", font=("Arial", 40), bg="#f3d6c2", fg="black")#5C6B72
label_sen1.place(x=10, y=90)

# Etiqueta para mostrar el valor del peso
label_val_sen1= tk.Label(ventana, text="0", font=("Arial", 60), bg="white", fg="Black", anchor=tk.NE, width=10, height=1)
label_val_sen1.place(x=280, y=80)



################################################################################################



# creamos bucle
ventana.mainloop()
