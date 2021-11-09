from tkinter import StringVar #Para asociar los campos de texto con el compomente texto
from tkinter import IntVar #Para asociar los campos de numero con el compomente radio

class Persona: #POJO

    def __init__(self):
        self.idUsuario = StringVar()
        self.nombreUsuario = StringVar()
        self.contrasena = StringVar()
        self.correo = StringVar()
        self.nombrePersona = StringVar()
        self.apellidoPersona = StringVar()
        self.fechaNacimiento = StringVar()
        self.estado = StringVar()
        self.descripcionPersona = StringVar()

    def limpiar(self):
        self.idUsuario.set("")
        self.nombreUsuario.set("")
        self.contrasena.set("")
        self.correo.set("")
        self.nombrePersona.set("")
        self.apellidoPersona.set("")
        self.fechaNacimiento.set("")
        self.estado.set("")
        self.descripcionPersona.set("")

    def printInfo(self):
        print(f"idUsuario: {self.idUsuario.get()}")
        print(f"Nombre Usuario: {self.nombreUsuario.get()}")
        print(f"Contraseña: {self.contrasena.get()}")
        print(f"Correo: {self.correo.get()}")
        print(f"Nombre Persona: {self.nombrePersona.get()}")
        print(f"Apellido Persona: {self.apellidoPersona.get()}")
        print(f"Fecha Nacimiento: {self.fechaNacimiento.get()}")
        print(f"Estado: {self.estado.get()}")
        print(f"Descripcion Persona: {self.descripcionPersona.get()}")
