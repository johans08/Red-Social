from tkinter import StringVar #Para asociar los campos de texto con el compomente texto
from tkinter import IntVar #Para asociar los campos de numero con el compomente radio

class Amigos: #POJO

    def __init__(self):
        self.nivelAmistad = IntVar()
        self.idUsuario = StringVar()
        self.idAmigo = StringVar()

    def limpiar(self):
        self.nivelAmistad.set("")
        self.idUsuario.set("")
        self.idAmigo.set("")

    def printInfo(self):
        print(f"Nivel de amistad: {self.nivelAmistad.get()}")
        print(f"id Usuario: {self.idUsuario.get()}")
        print(f"id Amigo: {self.idAmigo.get()}")

