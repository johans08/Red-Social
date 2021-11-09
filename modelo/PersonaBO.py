import mysql.connector # para instalarlo -> pip3 install mysql-connector 



class PersonaBO:

    #*************************************************************************
    #El constructor de la clase persona BO crea un objeto de conexion a la base de datos
    #*************************************************************************
    def __init__(self):
        #se crea la conexión con la base de datos
        self.db = mysql.connector.connect(host ="localhost", 
                                     user = "root", 
                                     password = "root", 
                                     db ="red_social") 

    #*************************************************************************
    #Cuando el objeto es destruido por el interprete realiza la desconexion con la base de datos
    #*************************************************************************
    def __del__(self):
        self.db.close() #al destriurse el objeto cierra la conexion 
  
    #*************************************************************************
    #Metodo que guarda una persona en la base de datos
    #*************************************************************************
    def guardar(self, personas):
        try:
            if(self.validar(personas)):#se valida que tenga la información

                if(not self.exist(personas)): #si no existe lo agrega
                    
                    insertSQL = "INSERT INTO personas (`idUsuario`, `nombreUsuario`, `contrasena`, `correo`, `nombrePersona`, `apellidoPersona`, `fechaNacimiento`, `estado`, `descripcionPersona`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    insertValores =  (personas.idUsuario.get(),personas.nombreUsuario.get(),personas.contrasena.get(), personas.correo.get(), personas.nombrePersona.get(), personas.apellidoPersona.get(), personas.fechaNacimiento.get(), personas.estado.get(), personas.descripcionPersona.get())
                    #print(insertValores)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('El idUsuario indicado en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    #*************************************************************************
    #Metodo que verifica en la base de datos si la persona existe por cédula
    #*************************************************************************
    def exist(self , personas):
        try:
            existe = False
            selectSQL = "Select * from personas where idUsuario = " + personas.idUsuario.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            if (cursor.fetchone()) : #Metodo obtiene un solo registro o none si no existe información
                existe  = True

            return existe
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 


    #*************************************************************************
    #Metodo para validar al información que proviene de la vista
    #*************************************************************************
    def validar (self, personas):
        valido = True
        personas.printInfo()
        if personas.idUsuario.get() == "" :
            valido = False
        
        if personas.nombreUsuario.get() == "" :
            valido = False

        if personas.contrasena.get() == "" :
            valido = False

        if personas.correo.get() == "" :
            valido = False

        if personas.nombrePersona.get() == "" :
            valido = False

        if personas.apellidoPersona.get() == "" :
            valido = False

        if personas.fechaNacimiento.get() == "" :
            valido = False
        
        if personas.estado.get() == "" :
            valido = False
        
        if personas.descripcionPersona.get() == "" :
            valido = False

        return valido

    #*************************************************************************
    #Metodo para consultar toda la información de la base de datos
    #*************************************************************************
    def consultar(self ):
        try:
            selectSQL = "select idUsuario as idUsuario, \
                            nombreUsuario, contrasena, correo, \
                            nombrePersona, apellidoPersona, fechaNacimiento, estado, descripcionPersona \
                            from personas" 
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            myresult = cursor.fetchall()
            final_result = [list(i) for i in myresult]
            return final_result
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 


    #*************************************************************************
    #Metodo para consultar la información de una persona
    #*************************************************************************
    def consultarPersona(self, personas):
        try:
            selectSQL = "Select * from personas where idUsuario = " + personas.idUsuario.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            personaDB = cursor.fetchone()
            if (personaDB) : #Metodo obtiene un solo registro o none si no existe información
                personas.idUsuario.set(personaDB[0]),
                personas.nombreUsuario.set(personaDB[1])
                personas.contrasena.set(personaDB[2])
                personas.correo.set(personaDB[3])
                personas.nombrePersona.set(personaDB[4])
                personas.apellidoPersona.set(personaDB[5])
                personas.fechaNacimiento.set(personaDB[6])
                personas.estado.set(personaDB[7])
                personas.descripcionPersona.set(personaDB[8])
            else:
                raise Exception("El idUsuario consultado no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #*************************************************************************
    #Metodo para eliminar a una persona de la base de datos
    #*************************************************************************
    def eliminar(self, personas):
        try:
            deleteSQL = "delete  from personas where idUsuario = " + personas.idUsuario.get()
            cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
            cursor.execute(deleteSQL) #ejecuta el SQL con las valores
            self.db.commit() #crea un commit en la base de datos
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 



    #*************************************************************************
    #Metodo que guarda una persona en la base de datos
    #*************************************************************************
    def modificar(self, personas):
        try:
            if(self.validar(personas)):#se valida que tenga la información

                if(self.exist(personas)): #si  existe lo modifica
                    
                    updateSQL = "UPDATE Personas  set `nombreUsuario` = %s, `contrasena` = %s, `correo` = %s, `nombrePersona` = %s, `apellidoPersona` = %s, `fechaNacimiento` = %s, `estado` = %s, `descripcionPersona` = %s WHERE `idUsuario` =  %s"
                    updateValores =  (personas.nombreUsuario.get(),personas.contrasena.get(), personas.correo.get(), personas.nombrePersona.get(), personas.apellidoPersona.get(), personas.fechaNacimiento.get(), personas.estado.get(), personas.descripcionPersona.get(), personas.idUsuario.get())
                    #print(insertValores)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(updateSQL, updateValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('El id Usuario indicado en el formulario no existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    