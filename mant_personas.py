from tkinter import * 
from tkinter import font
from tkinter import messagebox as msg
from tkinter import ttk 

from tksheet import Sheet # para instalarlo -> pip3 install tksheet

from tkcalendar import Calendar, DateEntry # para instalarlo -> pip3 install tkcalendar

#Incluye el objeto de persona
from modelo import Persona

#Incluye el objeto de logica de negocio
from modelo import PersonaBO

#incluye las otras pantallas 
import mant_gustos
import mant_amigos
import referenciasAmistad

#include para reportes, para instalar reportlab -> pip3 install reportlab
from reportlab.pdfgen import canvas as reportPDF
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors

#Importa para ejecutar un comando
import subprocess

class Aplicacion:
    

    def __init__(self):
        #*************************************************************************
        #Crea un objeto TK
        #*************************************************************************
        self.raiz = Tk()
        self.raiz.title ("Mantenimiento de Personas")
        self.raiz.geometry('900x600') 

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

        mantmenu.add_command(label="Gustos", command=self.mostrar_mant_gustos)
        mantmenu.add_command(label="Amigos", command=self.mostrar_mant_amigos)
        mantmenu.add_command(label="Referencias de Amistad", command=self.mostrar_referencias_amistad)

        menubar.add_cascade(label="Archivo", menu=filemenu)
        menubar.add_cascade(label="Mantenimiento", menu=mantmenu)

        #*************************************************************************
        #crea un objeto tipo fuenta
        #*************************************************************************
        self.fuente = font.Font(weight="bold")

        #*************************************************************************
        #se crean atributos de la clase
        #*************************************************************************
        self.personas = Persona.Persona() #se crea el objeto de dominio para guardar la información
        self.insertando = True
        
        #*************************************************************************
        #se crean los campos de la pantalla
        #*************************************************************************

        #Se coloca un label del titulo
        self.lb_tituloPantalla = Label(self.raiz, text = "MANTENIMIENTO DE PERSONAS", font = self.fuente)
        self.lb_tituloPantalla.place(x = 320, y = 20) #colocar por medio de espacion en pixeles de la parte superior de la pantalla considerando un eje x y un eje y
        
        #coloca en el formulario el campo y el label de idUsuario
        self.lb_idUsuario = Label(self.raiz, text = "id Usuario:")
        self.lb_idUsuario.place(x = 240, y = 60)
        self.txt_idUsuario = Entry(self.raiz, textvariable=self.personas.idUsuario, justify="right")
        self.txt_idUsuario.place(x = 370, y = 60)

        #coloca en el formulario el campo y el label de nombre
        self.lb_nombreUsuario = Label(self.raiz, text = "Nombre De Usuario:")
        self.lb_nombreUsuario.place(x = 240, y = 90)
        self.txt_nombreUsuario = Entry(self.raiz, textvariable=self.personas.nombreUsuario, justify="right", width=30)
        self.txt_nombreUsuario.place(x = 370, y = 90)

        #coloca en el formulario el campo y el label de contraseña
        self.lb_contrasena = Label(self.raiz, text = "Contraseña:")
        self.lb_contrasena.place(x = 240, y = 120)
        self.txt_contrasena = Entry(self.raiz, textvariable=self.personas.contrasena, justify="right", width=30)
        self.txt_contrasena.place(x = 370, y = 120)


        #coloca en el formulario el campo y el label de correo
        self.lb_correo = Label(self.raiz, text = "Correo:")
        self.lb_correo.place(x = 240, y = 150)
        self.txt_correo = Entry(self.raiz, textvariable=self.personas.correo, justify="right", width=30)
        self.txt_correo.place(x = 370, y = 150)

        #coloca en el formulario el campo y el label de nombre
        self.lb_nombrePersona = Label(self.raiz, text = "Nombre Persona:")
        self.lb_nombrePersona.place(x = 240, y = 180)
        self.txt_nombrePersona = Entry(self.raiz, textvariable=self.personas.nombrePersona, justify="right", width=30)
        self.txt_nombrePersona.place(x = 370, y = 180)

        #coloca en el formulario el campo y el label de apellido
        self.lb_apellidoPersona = Label(self.raiz, text = "Apellido Persona:")
        self.lb_apellidoPersona.place(x = 240, y = 210)
        self.txt_apellidoPersona = Entry(self.raiz, textvariable=self.personas.apellidoPersona, justify="right", width=30)
        self.txt_apellidoPersona.place(x = 370, y = 210)

        #coloca en el formulario el campo y el label de fecha nacimiento
        self.lb_fechaNacimiento = Label(self.raiz, text = "Fecha nacimiento:")
        self.lb_fechaNacimiento.place(x = 240, y = 240)
        self.txt_fechaNacimiento = Entry(self.raiz, textvariable=self.personas.fechaNacimiento, justify="right", width=30, state="readonly")
        self.txt_fechaNacimiento.place(x = 370, y = 240)
        self.bt_mostrarCalendario = Button(self.raiz, text="...", width=3, command = self.mostrarDatePicker)
        self.bt_mostrarCalendario.place(x = 650, y = 240)

        #coloca en el formulario el campo y el label de estado
        self.lb_estado = Label(self.raiz, text = "Estado: ")
        self.lb_estado.place(x = 240, y = 270)
        self.txt_estado = Entry(self.raiz, textvariable=self.personas.estado, justify="right", width=30)
        self.txt_estado.place(x = 370, y = 270)

        #coloca en el formulario el campo y el label de personal
        self.lb_descripcionPersonal = Label(self.raiz, text = "Descripcion Personal")
        self.lb_descripcionPersonal .place(x = 240, y = 300)
        self.txt_descripcionPersonal  = Entry(self.raiz, textvariable=self.personas.descripcionPersona, justify="right", width=30)
        self.txt_descripcionPersonal .place(x = 370, y = 300)


        #coloca los botones enviar y borrar
        self.bt_borrar = Button(self.raiz, text="Limpiar", width=15, command = self.limpiarInformacion)
        self.bt_borrar.place(x = 370, y = 330)

        self.bt_enviar = Button(self.raiz, text="Enviar", width=15, command = self.enviarInformacion)
        self.bt_enviar.place(x = 510, y = 330)

        self.bt_modificar = Button(self.raiz, text="Modificar", width=15, command = self.enviarInformacion)
        self.bt_modificar.place(x = 650, y = 310)

        #Se coloca un label del informacion
        self.lb_tituloPantalla = Label(self.raiz, text = "INFORMACIÓN INCLUIDA", font = self.fuente)
        self.lb_tituloPantalla.place(x = 350, y = 360) #colocar por medio de espacion en pixeles de la parte superior de la pantalla considerando un eje x y un eje y

        #*************************************************************************
        #tabla con informacion
        #*************************************************************************
        
        self.sheet = Sheet(self.raiz,
                           page_up_down_select_row = True,
                           #empty_vertical = 0,
                           column_width = 120,
                           startup_select = (0,1,"rows"),
                           #row_height = "4",
                           #default_row_index = "numbers",
                           #default_header = "both",
                           #empty_horizontal = 0,
                           #show_vertical_grid = False,
                           #show_horizontal_grid = False,
                           #auto_resize_default_row_index = False,
                           #header_height = "3",
                           #row_index_width = 100,
                           #align = "center",
                           #header_align = "w",
                            #row_index_align = "w",
                            #data = [[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(50)] for r in range(1000)], #to set sheet data at startup
                            headers = ['idUsuario', 'nombreUsuario', 'contrasena.', 'correo.','nombrePersona','apellidoPersona', 'Fec. Nacimiento', 'estado','descripcionPersona'],
                            #row_index = [f"Row {r}\nnewline1\nnewline2" for r in range(2000)],
                            #set_all_heights_and_widths = True, #to fit all cell sizes to text at start up
                            #headers = 0, #to set headers as first row at startup
                            #headers = [f"Column {c}\nnewline1\nnewline2" for c in range(30)],
                           #theme = "light green",
                            #row_index = 0, #to set row_index as first column at startup
                            #total_rows = 2000, #if you want to set empty sheet dimensions at startup
                            #total_columns = 30, #if you want to set empty sheet dimensions at startup
                            height = 195, #height and width arguments are optional
                            width = 720 #For full startup arguments see DOCUMENTATION.md
                            )
        #self.sheet.hide("row_index")
        #self.sheet.hide("header")
        #self.sheet.hide("top_left")
        self.sheet.enable_bindings(("single_select", #"single_select" or "toggle_select"
                                        
                                         "column_select",
                                         "row_select",
                                         "column_width_resize",
                                         "double_click_column_resize",
                                         #"row_width_resize",
                                         #"column_height_resize",
                                         "arrowkeys",
                                         "row_height_resize",
                                         "double_click_row_resize",
                                         "right_click_popup_menu",
                                         "rc_select",
                                         "rc_insert_column",
                                         "rc_delete_column",
                                         "rc_insert_row",
                                         "rc_delete_row"))
        #self.sheet.disable_bindings() #uses the same strings
        #self.sheet.enable_bindings()

        self.sheet.place(x = 20, y = 390)
        
        #coloca los botones cargar y eliminar
        self.bt_cargar = Button(self.raiz, text="Cargar", width=15, command = self.cargarInformacion)
        self.bt_cargar.place(x = 750, y = 385)
        self.bt_cargar.place(x = 750, y = 385)

        self.bt_eliminar = Button(self.raiz, text="Eliminar", width=15, command = self.eliminarInformacion)
        self.bt_eliminar.place(x = 750, y = 425)

        self.bt_reporte = Button(self.raiz, text="Reporte", width=15, command = self.generarPDFListado)
        self.bt_reporte.place(x = 750, y = 465)
        
        self.cargarTodaInformacion()


        #*************************************************************************
        #se inicial el main loop de la pantalla
        #*************************************************************************
        self.raiz.mainloop()

    #*************************************************************************
    #Llamadas a otras pantallas
    #*************************************************************************
    def generarPDFListado(self):
        try:
            #Crea un objeto para la creación del PDF
            nombreArchivo = "ListadoPersonas.pdf"
            rep = reportPDF.Canvas(nombreArchivo)

            #Agrega el tipo de fuente Arial
            registerFont(TTFont('Arial','ARIAL.ttf'))
            
        
            #Crea el texto en donde se incluye la información
            textobject = rep.beginText()
            # Coloca el titulo
            textobject.setFont('Arial', 16)
            textobject.setTextOrigin(10, 800)
            textobject.setFillColor(colors.darkorange)
            textobject.textLine(text='LISTA DE PERSONAS')
            #Escribe el titulo en el reportes
            rep.drawText(textobject)

            #consultar la informacion de la base de datos
            self.personaBo = PersonaBO.PersonaBO() #se crea un objeto de logica de negocio
            informacion = self.personaBo.consultar()
            #agrega los titulos de la tabla en la información consultada
            titulos = ["Cédula","Nombre","Primer Apellido","Segundo apellido","Fec. Nacimiento", "Sexo"]
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
            subprocess.Popen(nombreArchivo, shell=True) #Windows
        except IOError:
            msg.showerror("Error",  "El archivo ya se encuentra abierto") 

    #*************************************************************************
    #Llamadas a otras pantallas
    #*************************************************************************
    def mostrar_mant_gustos(self):
        mant_gustos.MantGustos(self.raiz)
    
    def mostrar_mant_amigos(self):
        mant_amigos.MantAmigos(self.raiz)

    def mostrar_referencias_amistad(self):
        referenciasAmistad.ReferenciasAmistad(self.raiz)


    #*************************************************************************
    #Metodo para consultar la información de la base de datos para 
    #cargarla en la tabla
    #*************************************************************************
    def cargarTodaInformacion(self):
        try:
            self.personaBo = PersonaBO.PersonaBO() #se crea un objeto de logica de negocio
            resultado = self.personaBo.consultar()

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
            self.personas.idUsuario.set(idUsuarios)
            self.personaBo = PersonaBO.PersonaBO() #se crea un objeto de logica de negocio
            self.personaBo.consultarPersona(self.personas) #se envia a consultar
            self.insertando = False
            msg.showinfo("Acción: Consultar persona", "La información de la persona ha sido consultada correctamente") # Se muestra el mensaje de que todo esta correcto
            
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Metodo para cargar eliminar la informacion
    #*************************************************************************
    def eliminarInformacion(self):
        try:
            datoSeleccionado = self.sheet.get_currently_selected()
            idUsuarios = (self.sheet.get_cell_data(datoSeleccionado[0],0))
            nombre = (self.sheet.get_cell_data(datoSeleccionado[0],1))

            resultado = msg.askquestion("Eliminar",  "¿Desear eliminar a "+nombre+" de la base de datos?")
            if resultado == "yes":
                self.personas.idUsuario.set(idUsuarios)
                self.personaBo = PersonaBO.PersonaBO() #se crea un objeto de logica de negocio
                self.personaBo.eliminar(self.personas) #se envia a consultar
                self.cargarTodaInformacion()
                self.personas.limpiar()
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error


    #*************************************************************************
    #Metodo para enviar la información a la base de datos
    #*************************************************************************
    def enviarInformacion(self):
        try:
            self.personaBo = PersonaBO.PersonaBO() #se crea un objeto de logica de negocio
            if(self.insertando == True):
                self.personaBo.guardar(self.personas)
            else:
                self.personaBo.modificar(self.personas)
            
            self.cargarTodaInformacion()
            self.personas.limpiar() #se limpia el formulario

            if(self.insertando == True):
                msg.showinfo("Acción: Agregar persona", "La información de la persona ha sido incluida correctamente") # Se muestra el mensaje de que todo esta correcto
            else:
                msg.showinfo("Acción: Agregar modificar", "La información de la persona ha sido modificada correctamente") # Se muestra el mensaje de que todo esta correcto
        except Exception as e: 
            msg.showerror("Error",  str(e)) #si se genera algun tipo de error muestra un mensache con dicho error

    #*************************************************************************
    #Metodo para limpiar el formulario
    #*************************************************************************
    def limpiarInformacion(self):
        self.personas.limpiar() #llama al metodo de la clase persona para limpiar los atritudos de la clase
        self.insertando = True
        msg.showinfo("Acción del sistema", "La información del formulario ha sido eliminada correctamente") # muestra un mensaje indicando que se limpio el formulario


    #*************************************************************************
    #Metodo para mostrar un contro tipo datepicker
    #*************************************************************************
    def mostrarDatePicker(self):
        self.top = Toplevel(self.raiz)
        self.cal = Calendar(self.top, font="Arial 14", selectmode='day', locale='en_US',
                   year=2019, month=6, day=16)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="Seleccionar", command = self.seleccionarFecha).pack()

    #*************************************************************************
    #Evento para obtener la fecha del datepicker
    #*************************************************************************
    def seleccionarFecha(self):
        self.personas.fechaNacimiento.set(self.cal.selection_get())

def main():
    Aplicacion()
    return 0

if __name__ == "__main__":
    main()