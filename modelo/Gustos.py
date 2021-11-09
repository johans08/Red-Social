from tkinter import StringVar #Para asociar los campos de texto con el compomente texto
from tkinter import IntVar #Para asociar los campos de numero con el compomente radio

class Gustos: #POJO

    def __init__(self):
        self.idGustos = StringVar()
        self.idUsuarios = StringVar()
        self.nombreGustos = StringVar()
        self.descripcionGustos = StringVar()
        
 
        

    def limpiar(self):
        self.idGustos.set("")
        self.idUsuarios.set("")
        self.nombreGustos.set("")
        self.descripcionGustos.set("")

    def printInfo(self):
        print(f"id Gustos: {self.idGustos.get()}")
        print(f"id Usuario: {self.idUsuarios.get()}")
        print(f"Nombre Gustos: {self.nombreGustos.get()}")
        print(f"Descripcion Gustos: {self.descripcionGustos.get()}")
        
