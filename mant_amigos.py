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
import referenciasAmistad

#include para reportes, para instalar reportlab -> pip3 install reportlab
from reportlab.pdfgen import canvas as reportPDF
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors

#Importa para ejecutar un comando
import subprocess

class MantAmigos():
    

    def __init__(self, parent):
        self.parent = parent
        #*************************************************************************
        #Crea un objeto TK
        #*************************************************************************
        self.raiz = Toplevel(self.parent) #para crear ventanas secundarias
        self.raiz.title ("Mantenimiento de Amigos")
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
        mantmenu.add_command(label="Referencias De Amistad", command=self.mostrar_referencias_amistad)
        mantmenu.add_command(label="Gustos", command=self.mostrar_mant_gustos)

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
        self.insertando = True
        self.nombrePersona = StringVar() #crea un objeto de tipo string var para asociarlo al nombre de la persona 

        self.persona = Persona.Persona()
        
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
        self.bt_consultar = Button(self.raiz, text="Consultar", width=15, command = self.consultarNombre)
        self.bt_consultar.place(x = 512, y = 60)

        #coloca en el formulario el campo y el label de nombre
        self.lb_nombre = Label(self.raiz, text = "Nombre:")
        self.lb_nombre.place(x = 240, y = 90)
        self.txt_nombre = Entry(self.raiz, textvariable=self.nombrePersona, justify="right", width=30)
        self.txt_nombre.place(x = 370, y = 90)

        #coloca en el formulario el campo y el label del idAmistad
        self.lb_idAmistad = Label(self.raiz, text = "idAmistad:")
        self.lb_idAmistad.place(x = 240, y = 120)
        self.txt_idAmistad = Entry(self.raiz, textvariable=self.amigos.idAmigo, justify="right", width=30)
        self.txt_idAmistad.place(x = 370, y = 120)


        #coloca en el formulario el campo y el label de nivelAmistad
        self.lb_nivelAmistad = Label(self.raiz, text = "nivelAmistad:")
        self.lb_nivelAmistad.place(x = 240, y = 150)
        self.txt_nivelAmistad = Entry(self.raiz, textvariable=self.amigos.nivelAmistad, justify="right", width=30)
        self.txt_nivelAmistad.place(x = 370, y = 150)

        #coloca los botones enviar y borrar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command=self.limpiarInformacion)
        self.bt_borrar.place(x = 370, y = 180)

        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command=self.enviarInformacion)
        self.bt_enviar.place(x = 510, y = 180)

        #Se coloca un label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 350, y = 230) #colocar por medio de espacion en pixeles de la parte superior de la pantalla considerando un eje x y un eje y

        #*************************************************************************
        #tabla con informacion
        #*************************************************************************
        
        self.sheet = Sheet(self.raiz,
                            page_up_down_select_row = True,
                            column_width = 120,
                            startup_select = (0,1,"rows"),
                            headers = ['idUsuario', 'Nombre Usuario','idAmigo', 'Nivel de Amistad'],
                            height = 195, #height and width arguments are optional
                            width = 720 #For full startup arguments see DOCUMENTATION.md
                            )
        
        self.sheet.enable_bindings(("single_select", 
                                    "column_select",
                                    "row_select",
                                    "column_width_resize",
                                    "double_click_column_resize",
                                    "arrowkeys",
                                    "row_height_resize",
                                    "double_click_row_resize",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "rc_insert_column",
                                    "rc_delete_column",
                                    "rc_insert_row",
                                    "rc_delete_row"))
        self.sheet.place(x = 20, y = 260)

        #*************************************************************************
        #coloca los botones cargar, eliminar y reporte
        #*************************************************************************
        self.bt_cargar = Button(self.raiz, text="Cargar", width=15, command=self.cargarInformacion)
        self.bt_cargar.place(x = 750, y = 255)

        self.bt_eliminar = Button(self.raiz, text="Eliminar", width=15, command=self.eliminarInformacion)
        self.bt_eliminar.place(x = 750, y = 295)

        self.bt_reporte = Button(self.raiz, text="Reporte", width=15, command = self.generarPDFListado)
        self.bt_reporte.place(x = 750, y = 335)
        
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


    def generarPDFListado(self):
        try:
            #Crea un objeto para la creación del PDF
            nombreArchivo = "ListadoAmigos.pdf"
            rep = reportPDF.Canvas(nombreArchivo)

            #Agrega el tipo de fuente Arial
            registerFont(TTFont('Arial','ARIAL.ttf'))
            
        
            #Crea el texto en donde se incluye la información
            textobject = rep.beginText()
            # Coloca el titulo
            textobject.setFont('Arial', 16)
            textobject.setTextOrigin(10, 800)
            textobject.setFillColor(colors.darkorange)
            textobject.textLine(text='LISTA DE AMIGOS')
            #Escribe el titulo en el reportes
            rep.drawText(textobject)

            #consultar la informacion de la base de datos
            self.amigosBo = AmigosBO.AmigosBO() #se crea un objeto de logica de negocio
            informacion = self.amigosBo.consultar()
            #agrega los titulos de la tabla en la información consultada
            titulos = ['idUsuario', 'Nombre', 'idAmigo', 'nivelAmistad']
            informacion.insert(0,titulos)
            #crea el objeto tabla  para mostrar la información
            t = Table(informacion)
            #Le coloca el color tanto al borde de la tabla como de las celdas
            t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                                  ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black)]))

            #para cambiar el color de las fichas de hace un ciclo según la cantidad de datos
            #que devuelve la base de datos
            data_len = len(informacion)
            for each in range(data_len):
                if each % 2 == 0:
                    bg_color = colors.whitesmoke
                else:
                    bg_color = colors.lightgrey

                if each == 0 : #Le aplica un estilo diferente a la tabla
                    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), colors.orange)]))
                else:
                    t.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

            #acomoda la tabla según el espacio requerido
            aW = 840
            aH = 780
            w, h = t.wrap(aW, aH)
            t.drawOn(rep, 10, aH-h)

            #Guarda el archivo
            rep.save()
            #Abre el archivo desde comandos, puede variar en MacOs es open
            #subprocess.Popen("open '%s'" % nombreArchivo, shell=True)
            subprocess.Popen(nombreArchivo, shell=True) #Windowsl
        except IOError:
            msg.showerror("Error",  "El archivo ya se encuentra abierto")


    

    #*************************************************************************
    #Metodo para enviar la información a la base de datos
    #*************************************************************************
    def enviarInformacion(self):
        try:
            self.amigosBo = AmigosBO.AmigosBO() #se crea un objeto de logica de negocio
            if(self.insertando == True):
                self.amigosBo.guardar(self.amigos)
            else:
                self.amigosBo.modificar(self.amigos)
            
            self.cargarTodaInformacion()
            self.amigos.limpiar()
            self.nombrePersona.set("")

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar amigos", "La información del amigo ha sido incluida correctamente") # Se muestra el mensaje de que todo esta correcto
            else:
                msg.showinfo("Acción: Modificar amigos", "La información del amigo ha sido modificada correctamente") # Se muestra el mensaje de que todo esta correcto
            
            self.insertando = True

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Metodo para limpiar el formulario
    #*************************************************************************
    def limpiarInformacion(self):
        self.amigos.limpiar() #llama al metodo de la clase persona para limpiar los atritudos de la clase
        self.nombrePersona.set("")
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
            if self.persona.nombrePersona.get() == "" :
                self.nombrePersona = "No existe la persona "
            else:
                self.nombrePersona.set(self.persona.nombrePersona.get() + " " + self.persona.apellidoPersona.get())

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Metodo para consultar la información de la base de datos para 
    #cargarla en la tabla
    #*************************************************************************
    def cargarTodaInformacion(self):
        try:
            self.amigosBo = AmigosBO.AmigosBO() #se crea un objeto de logica de negocio
            resultado = self.amigosBo.consultar()

            self.sheet.set_sheet_data(resultado)
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error


    #*************************************************************************
    #Metodo para cargar informacion
    #*************************************************************************
    def cargarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            idUsuarios = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            idAmigos = (self.sheet.get_cell_data(datoSeleccionado[0],2))
            self.amigos.idUsuario.set(idUsuarios)
            self.amigos.idAmigo.set(idAmigos)
            self.amigoBo = AmigosBO.AmigosBO() #se crea un objeto de logica de negocio
            self.amigoBo.consultarAmigos(self.amigos) #se envia a consultar
            self.consultarNombre()
            self.insertando = False
            msg.showinfo("Acción: Consultar amigo", "La información del amigo ha sido consultada correctamente") # Se muestra el mensaje de que todo esta correcto
            
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Metodo para cargar eliminar la informacion
    #*************************************************************************
    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            idUsuarios = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            idAmigos = (self.sheet.get_cell_data(datoSeleccionado[0],2))
            nombre = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar el amigo "+idUsuarios+" de "+nombre+" de la base de datos?")
            if resultado == "yes":
                self.amigos.idUsuario.set(idUsuarios)
                self.amigos.idAmigo.set(idAmigos)
                self.amigoBo = AmigosBO.AmigosBO() #se crea un objeto de logica de negocio
                self.amigoBo.eliminar(self.amigos) #se envia a consultar
                self.cargarTodaInformacion()
                self.amigos.limpiar()
                self.nombrePersona.set("")

        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Llamadas a otras pantallas
    #*************************************************************************
    def mostrar_mant_personas(self):
        self.parent.deiconify()
        self.raiz.destroy()

    def mostrar_mant_gustos(self):
        mant_gustos.MantGustos(self.raiz)

    def mostrar_referencias_amistad(self):
        referenciasAmistad.ReferenciasAmistad(self.raiz)

    def on_closing(self):
       self.parent.destroy()

  

