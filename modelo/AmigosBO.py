import mysql.connector # para instalarlo -> pip3 install mysql-connector 



class AmigosBO:

    #*************************************************************************
    #El constructor de la clase amigos BO crea un objeto de conexion a la base de datos
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
    #Metodo que guarda un amigo en la base de datos
    #*************************************************************************
    def guardar(self, amigos):
        try:
            if(self.validar(amigos)):#se valida que tenga la información

                if(not self.exist(amigos)): #si no existe lo agrega
                    
                    insertSQL = "INSERT INTO amigos (`nivelAmistad`, `FK_idUsuario`, `FK_idAmigo`) VALUES (%s, %s, %s)"
                    insertValores =  (amigos.nivelAmistad.get(),amigos.idUsuario.get(),amigos.idAmigo.get())
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(insertSQL, insertValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('El amigo indicado en el formulario existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    
    #*************************************************************************
    #Metodo que verifica en la base de datos si la persona existe por cédula
    #*************************************************************************
    def exist(self , amigos):
        try:
            existe = False
            selectSQL = "Select * from Amigos where FK_idUsuario = " + amigos.idUsuario.get() + " and FK_idAmigo = " + amigos.idAmigo.get()
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
    def validar (self, amigos):
        valido = True
        amigos.printInfo()
        if amigos.nivelAmistad.get() == "" :
            valido = False
        
        if amigos.idUsuario.get() == "" :
            valido = False

        if amigos.idAmigo.get() == "" :
            valido = False

        return valido

    #*************************************************************************
    #Metodo para consultar toda la información de la base de datos
    #*************************************************************************
    def consultar(self ):
        try:
            selectSQL = 'select a.Fk_idUsuario as idUsuario, \
                            CONCAT( p.nombrePersona, " ", p.apellidoPersona) as nombrePersona, \
                            a.fk_idAmigo as idAmigo, \
                            a.nivelAmistad as amigos \
                        from amigos a inner join personas p on a.FK_idUsuario = p.idUsuario'
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
    def consultarAmigos(self, amigos):
        try:
            selectSQL = "Select * from Amigos where FK_idUsuario = " + amigos.idUsuario.get() + " and FK_idAmigo = " + amigos.idAmigo.get()
            print(f"SQL{selectSQL}")
            cursor = self.db.cursor()
            cursor.execute(selectSQL)
            personaDB = cursor.fetchone()
            if (personaDB) : #Metodo obtiene un solo registro o none si no existe información
                amigos.idUsuario.set(personaDB[2])
                amigos.idAmigo.set(personaDB[1])
                amigos.nivelAmistad.set(personaDB[0])
            else:
                raise Exception("La idUsuario consultada no existe en la base de datos") 
            
        except mysql.connector.Error as e:
            print("Something went wrong: {}".format(e))
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 

    #*************************************************************************
    #Metodo para eliminar a una persona de la base de datos
    #*************************************************************************
    def eliminar(self, amigos):
        try:
            deleteSQL = "delete  from amigos where FK_idUsuario = " + amigos.idUsuario.get() + " and FK_idAmigo = " + amigos.idAmigo.get()
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
    def modificar(self, amigos):
        try:
            if(self.validar(amigos)):#se valida que tenga la información

                if(self.exist(amigos)): #si  existe lo modifica
                    updateSQL = "UPDATE amigos  set `FK_idAmigo` = %s, `nivelAmistad` = %s WHERE `FK_idUsuario` =  %s"
                    updateValores =  (amigos.idAmigo.get(),amigos.nivelAmistad.get(),amigos.idUsuario.get())
                    #print(insertValores)
                    cursor = self.db.cursor() #crea un cursos con la conexión lo que nos permite conectarnos a la base de datos
                    cursor.execute(updateSQL, updateValores) #ejecuta el SQL con las valores
                    self.db.commit() #crea un commit en la base de datos
                else:
                    raise Exception('La idUsuario indicada en el formulario no existe en la base de datos')  # si existe el registro con la misma cedual genera el error
            else:
                raise Exception('Los datos no fueron digitados por favor validar la información')  # si no tiene todos los valores de genera un error
        except mysql.connector.Error as e:
            raise Exception(str(e)) 
        except Exception as e: 
            raise Exception(str(e)) 
    


        
        