from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk 


from tksheet import Sheet # para instalarlo -> pip3 install tksheet

from tkcalendar import Calendar, DateEntry # para instalarlo -> pip3 install tkcalendar

#Incluye el objeto de persona
from modelo import Amigos
from modelo import Persona
from modelo import Gustos

#Incluye el objeto de logica de negocio
from modelo import AmigosBO
from modelo import PersonaBO
from modelo import GustosBO

import mant_gustos
import mant_amigos

#include para reportes, para instalar reportlab -> pip3 install reportlab
from reportlab.pdfgen import canvas as reportPDF
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors

#Importa para ejecutar un comando
import subprocess

class ReferenciasAmistad():
    

    def __init__(self, parent):
        self.parent = parent
        #*************************************************************************
        #Crea un objeto TK
        #*************************************************************************
        self.raiz = Toplevel(self.parent) #para crear ventanas secundarias
        self.raiz.title ("Referenias de Amistad")
        self.raiz.geometry('900x510') 

        #*************************************************************************
        #crea el menu de la pantalla
        #*************************************************************************
        menubar = Menu(self.raiz)
        self.raiz.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Acerca de..")
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.raiz.quit)

        mantmenu = Menu(menubar, tearoff=0)
        mantmenu.add_command(label="Personas", command=self.mostrar_mant_personas)
        mantmenu.add_command(label="Amigos", command=self.mostrar_mant_amigos)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        #*************************************************************************
        #crea un objeto tipo fuenta
        #*************************************************************************
        self.fuente = font.Font(weight="bold")

        #*************************************************************************
        #se crean atributos de la clase
        #*************************************************************************
        self.amigos = Amigos.Amigos() #se crea el objeto de dominio para guardar la información
        self.personaas = Amigos.Amigos() #se crea el objeto de dominio para guardar la información
        self.insertando = True
        self.nombrePersona = StringVar() #crea un objeto de tipo string var para asociarlo al nombre de la persona 
        self.nombreAmigo = StringVar() #crea un objeto de tipo string var para asociarlo al nombre del amigo

        self.persona = Persona.Persona()
        self.amigo = Persona.Persona()
        
        #*************************************************************************
        #se crean los campos de la pantalla
        #*************************************************************************

        #Se coloca un label del titulo
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE AMIGOS", font = self.fuente)
        self.lb_tituloPantalla.place(x = 320, y = 20) #colocar por medio de espacion en pixeles de la parte superior de la pantalla considerando un eje x y un eje y
        
        #coloca en el formulario el campo y el label del idUsuario
        self.lb_idUsuario = Label(self.raiz, text = "idUsuario:")
        self.lb_idUsuario.place(x = 240, y = 60)
        self.txt_idUsuario = Entry(self.raiz, textvariable=self.amigos.idUsuario, justify="right", width=12)
        self.txt_idUsuario.place(x = 370, y = 60)

        #coloca el boton de consultar persona
        self.bt_consultar = Button(self.raiz, text="Consultar Persona", width=15, command = self.consultarNombre)
        self.bt_consultar.place(x = 530, y = 60)

        #coloca el boton de consultar persona
        self.bt_consultarAmigo = Button(self.raiz, text="Consultar Amigo", width=15, command = self.consultarNombreAmigo)
        self.bt_consultarAmigo.place(x = 530, y = 90)

        #coloca en el formulario el campo y el label de nombre
        self.lb_nombre = Label(self.raiz, text = "Nombre Persona:")
        self.lb_nombre.place(x = 240, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.nombrePersona, justify="right", width=30)
        self.txt_nombre.place(x = 370, y = 90)

        #coloca en el formulario el campo y el label del idAmistad
        self.lb_idAmistad = Label(self.raiz, text = "idAmigo:")
        self.lb_idAmistad.place(x = 240, y = 120)
        self.txt_idAmistad = Entry(self.raiz, textvariable=self.amigos.idAmigo, justify="right", width=30)
        self.txt_idAmistad.place(x = 370, y = 120)

        #coloca en el formulario el campo y el label de nombre Amigo
        self.lb_nombreAmigo = Label(self.raiz, text = "Nombre Persona:")
        self.lb_nombreAmigo.place(x = 240, y = 150)
        self.txt_nombreAmigo = Entry(self.raiz, textvariable=self.nombreAmigo, justify="right", width=30)
        self.txt_nombreAmigo.place(x = 370, y = 150)


        #coloca en el formulario el campo y el label de nivelAmistad
        self.lb_nivelAmistad = Label(self.raiz, text = "nivelAmistad:")
        self.lb_nivelAmistad.place(x = 240, y = 180)
        self.txt_nivelAmistad = Entry(self.raiz, textvariable=self.amigos.nivelAmistad, justify="right", width=30)
        self.txt_nivelAmistad.place(x = 370, y = 180)

        #coloca los botones enviar y borrar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command=self.limpiarInformacion)
        self.bt_borrar.place(x = 370, y = 210)



        
        #*************************************************************************
        #se lama el metodo para cargar la informacion
        #*************************************************************************
        self.cargarTodaInformacion()

        #*************************************************************************
        #se inicial el main loop de la pantalla
        #*************************************************************************
        
        #Esconde la pantalla principal sin destruirla
        self.parent.withdraw()

        #Se configura el evento al cerrar la pantalla hija
        self.raiz.protocol("WM_DELETE_WINDOW", self.on_closing) #cuando se cierra la pantalla hija debe cerrar la principal



    #*************************************************************************
    #Metodo para limpiar el formulario
    #*************************************************************************
    def limpiarInformacion(self):
        self.amigos.limpiar() #llama al metodo de la clase persona para limpiar los atritudos de la clase
        self.nombrePersona.set("")
        self.nombreAmigo.set("")
        self.insertando = True
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente") # muestra un mensaje indicando que se limpio el formulario


    #*************************************************************************
    #Metodo para consultar el nombre de una persona
    #*************************************************************************
    def consultarNombre(self):
        try:
            self.personaBo = PersonaBO.PersonaBO()
            self.persona.idUsuario.set(self.amigos.idUsuario.get()) #setea el idUsuario de la persona 
            self.personaBo.consultarPersona(self.persona) #se envia a consultar
            if self.persona.nombrePersona.get() == "":
                self.nombrePersona = "No existe la persona "
            else:
                self.nombrePersona.set(self.persona.nombrePersona.get() + " " + self.persona.apellidoPersona.get())


        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    def consultarNombreAmigo(self):
        try:
            self.amigoBo = PersonaBO.PersonaBO()
            self.amigo.idUsuario.set(self.personaas.idUsuario.get()) #setea el idUsuario de la persona
            self.amigoBo.consultarPersona(self.amigo) #se envia a consultar
            if self.amigo.nombrePersona.get() == "" :
                self.nombreAmigo = "No existe la persona "
            else:
                self.nombreAmigo.set(self.amigo.nombrePersona.get() + " " + self.amigo.apellidoPersona.get())

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error'''

    #*************************************************************************
    #Metodo para consultar la información de la base de datos para 
    #cargarla en la tabla
    #*************************************************************************
    def cargarTodaInformacion(self):
        try:
            self.amigosBo = AmigosBO.AmigosBO() #se crea un objeto de logica de negocio
            resultado = self.amigosBo.consultar()

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    

    #*************************************************************************
    #Llamadas a otras pantallas
    #*************************************************************************
    def mostrar_mant_personas(self):
        self.parent.deiconify()
        self.raiz.destroy()

    def mostrar_mant_amigos(self):
        mant_amigos.MantAmigos(self.raiz)

    def on_closing(self):
       self.parent.destroy()
