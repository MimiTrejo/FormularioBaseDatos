
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 07:48:47 2024

@author: trejo
"""
import tkinter as tk
from tkinter import messagebox
import re
import mysql.connector # Libreria para conectar con MySQL

def insertarRegistro(nombres, apellidos, edad, estatura, telefono, genero):
    try:
        #Conectar a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root", #Cambiar con el usuario de MySQL se personaliza 
            password="", #Reemplazar con nuestra contraseña de MySQL si se personaliza
            database="programacion_avanzada_formulario" #Remplazaremos con el nombre de nuestra base de datos
            )
        cursor = conexion.cursor()
        #Crear el query SQL para insertar el registro
        query = "INSERT INTO registros (Nombre, Apellido, Edad, Estatura, Telefono, Genero) VALUES (%s, %s, %s, %s, %s, %s)"
        valores =(nombres, apellidos, edad, estatura, telefono, genero)
        #Ejecutamoe el query
        cursor.execute(query, valores)
        #Guardamos los cambios en la base de datos
        conexion.commit()
        #Cerramos conexion
        cursor.close()
        conexion.close()
        messagebox.showinfo("Informacion", "Datos guardados en la base de datos con exito.")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar los datos: {err}")
def entero_valido(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False

def decimal_valido(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def telefono_valido(valor):
    return valor.isdigit() and len(valor) == 10

def texto_valido(valor):
    return bool(re.match("^[a-zA-Z]+$", valor))

### Definición de funciones
def limpiar_campos():
    tbNombre.delete(0, tk.END)
    tbApellidos.delete(0, tk.END)
    tbEdad.delete(0, tk.END)
    tbEstatura.delete(0, tk.END)
    tbTelefono.delete(0, tk.END)
    var_genero.set(0)

def borrar_fun():
    limpiar_campos()

def guardar_valores():
    # Obtener valores desde los entrys
    nombres = tbNombre.get()
    apellidos = tbApellidos.get()
    edad = tbEdad.get()
    estatura = tbEstatura.get()
    telefono = tbTelefono.get()
    
    genero = ""
    if var_genero.get() == 1:
        genero = "Hombre"
    elif var_genero.get() == 2:
        genero = "Mujer"

    if (entero_valido(edad) and decimal_valido(estatura) and telefono_valido(telefono) and texto_valido(nombres) and texto_valido(apellidos)):
    # Generar la cadena de caracteres
        datos = (f"Nombres: {nombres}\n"+f"Apellidos: {apellidos}\n"+
            f"Edad: {edad} anos\n"+
            f"Estatura: {estatura}\n"+
            f"Telefono: {telefono}\n"+
            f"Genero: {genero}\n")

    # Guardar los datos en el archivo TXT
        with open("Practica.txt", "a") as archivo:
            archivo.write(datos + "\n\n")
            insertarRegistro(nombres, apellidos, edad, estatura, telefono, genero)

    # Mostrar mensaje de confirmación
        messagebox.showinfo("Informacion", "Datos guardados con exito: \n\n" + datos)
        limpiar_campos()
        
    else: 
        # Mensaje de error en caso de validación fallida
        messagebox.showinfo("ERROR", "Los datos contienen formatos no validos:\n\n")

## Creación de ventana
ventana = tk.Tk()
ventana.geometry("520x500")
ventana.title("Formulario Vr.01")

# Crear variable para el RadioButton
var_genero = tk.IntVar()

## Creación de etiquetas y campos de entrada
lbNombre = tk.Label(ventana, text="Nombres:")
lbNombre.pack()
tbNombre = tk.Entry(ventana)
tbNombre.pack()

lbApellidos = tk.Label(ventana, text="Apellidos:")
lbApellidos.pack()
tbApellidos = tk.Entry(ventana)
tbApellidos.pack()

lbTelefono = tk.Label(ventana, text="Telefono:")
lbTelefono.pack()
tbTelefono = tk.Entry(ventana)
tbTelefono.pack()

lbEdad = tk.Label(ventana, text="Edad:")
lbEdad.pack()
tbEdad = tk.Entry(ventana)
tbEdad.pack()

lbEstatura = tk.Label(ventana, text="Estatura:")
lbEstatura.pack()
tbEstatura = tk.Entry(ventana)
tbEstatura.pack()

lbGenero = tk.Label(ventana, text="Genero:")
lbGenero.pack()

rbHombre = tk.Radiobutton(ventana, text="Hombre", variable=var_genero, value=1)
rbHombre.pack()
rbMujer = tk.Radiobutton(ventana, text="Mujer", variable=var_genero, value=2)
rbMujer.pack()

## Creación de Botones
btnBorrar = tk.Button(ventana, text="Borrar valores", command=borrar_fun)
btnBorrar.pack()

btnGuardar = tk.Button(ventana, text="Guardar valores", command=guardar_valores)
btnGuardar.pack()

## Ejecución de ventana
ventana.mainloop()
