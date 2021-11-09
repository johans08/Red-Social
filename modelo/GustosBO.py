import mysql.connector # para instalarlo -> pip3 install mysql-connector 



class GustosBO:

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
    def guardar(self, gustos):
        try:
            if(self.validar(gustos)):#se valida que tenga la información

                if(not self.exist(gustos)): #si no existe lo agrega
                    
                    insertSQL = "INSERT INTO gustos (`idGustos`, `FK_FK_idUsuario`, `nombreGustos`, `descripcionGustos`, `idUsuarios`) VALUES (%s, %s, %s, %s,0)"
                    insertValores =  (gustos.idGustos.get(), gustos.idUsuarios.get(), gustos.nombreGustos.get(),gustos.descripcionGustos.get())
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('El Gusto indicado en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    #*************************************************************************
    #Metodo que verifica en la base de datos si la persona existe por cédula
    #*************************************************************************
    def exist(self , gustos):
        try:
            existe = False
            selectSQL = "Select * from gustos where idGustos = " + gustos.idGustos.get()
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
    def validar (self, gustos):
        valido = True
        gustos.printInfo()
        if gustos.idGustos.get() == "" :
            valido = False

        if gustos.idUsuarios.get() == "" :
            valido = False
        
        if gustos.nombreGustos.get() == "" :
            valido = False

        if gustos.descripcionGustos.get() == "" :
            valido = False

        return valido

    #*************************************************************************
    #Metodo para consultar toda la información de la base de datos
    #*************************************************************************
    def consultar(self ):
        try:
            selectSQL = 'select g.idGustos as gustos, \
                            g.FK_FK_idUsuario as idUsuarios, \
                            CONCAT( p.nombrePersona, " ", p.apellidoPersona) as nombrePersona, \
                            g.nombreGustos as gustos, \
                            g.descripcionGustos as gustos\
                        from gustos g inner join personas p on g.FK_FK_idUsuario = p.idUsuario'
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
    def consultarGustos(self, gustos):
        try:
            selectSQL = "Select * from gustos where idGustos = " + gustos.idGustos.get()
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            personaDB = cursor.fetchone()
            if (personaDB) : #Metodo obtiene un solo registro o none si no existe información
                gustos.idGustos.set(personaDB[0])
                gustos.idUsuarios.set(personaDB[1])
                gustos.nombreGustos.set(personaDB[2])
                gustos.descripcionGustos.set(personaDB[3])
            else:
                raise Exception("El idGusto consultado no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #*************************************************************************
    #Metodo para eliminar a una persona de la base de datos
    #*************************************************************************
    def eliminar(self, gustos):
        try:
            deleteSQL = "delete  from gustos where idGustos = " + gustos.idGustos.get()
            cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
            cursor.execute(deleteSQL) #ejecuta el SQL con las valores
            self.db.commit() #crea un commit en la base de datos
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            if str(e) == "tiene FK":
                raise Exception("El dato no se puede eliminar por que tiene datos asociados, por favor eliminarlos primero")     
            else:
                raise Exception(str(e)) 



    #*************************************************************************
    #Metodo que guarda una persona en la base de datos
    #*************************************************************************
    def modificar(self, gustos):
        try:
            if(self.validar(gustos)):#se valida que tenga la información

                if(self.exist(gustos)): #si  existe lo modifica
                    updateSQL = "UPDATE gustos set `FK_FK_idUsuario` = %s, `nombreGustos` = %s,`descripcionGustos` = %s WHERE `idGustos` =  %s"
                    updateValores =  (gustos.idUsuarios.get(), gustos.nombreGustos.get(),gustos.descripcionGustos.get(), gustos.idGustos.get())
                    #print(insertValores)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(updateSQL, updateValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('El Gusto indicada en el formulario no existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    