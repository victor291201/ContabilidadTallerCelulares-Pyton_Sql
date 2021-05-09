from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
from playsound import playsound
#onClick = "media/onClick.mp3"
import pymysql 
import mysql.connector
import datetime
import random

conection = pymysql.connect(
	host="localhost",
	user="root",
	password="1234",
	db="celulares"
)
cursor = conection.cursor()
cursor.execute(
	"select idtipo_identificacion, nombre from tipo_identificacion"
)
var_tipo = cursor.fetchall()
cursor.execute(
	"select idestado, nombre from estado"
)
var_estados = cursor.fetchall()
def int_str(x):
	for i in range(len(x)):
		if(x[i]!="1" and x[i]!="2" and x[i]!="3" and x[i]!="4" and x[i]!="5" and x[i]!="6" and x[i]!="7" and x[i]!="8" and x[i]!="9" and x[i]!="0"):
			return False
	return True
def src_indx(x,y):
	if(y == "tusuario"):
		for i in range(len(var_usuario)):
			if(var_usuario[i][1]==x):
				return var_usuario[i][0]

	if(y == "tdocument"):
		for i in range(len(var_tipo)):
			if(var_tipo[i][1]==x):
				return var_tipo[i][0]

	if(y == "testado"):
		for i in range(len(var_estados)):
			if(var_estados[i][1]==x):
				return var_estados[i][0]
	

def autenticar_login(x,y):
	if(x.get()!="" and x.get()!=" "):
		if(y.get()!="" and y.get()!=" "):
			cursor.execute(
			"select usuario,contrasena,(select nombre from tipo_usuario where usuario.rol_idrol = idrol) as rol "+
			"from usuario "+
			"where usuario = '" +x.get()+"' and contrasena ='"+y.get()+"'"
			)
			res_log = cursor.fetchall()
			if(len(res_log)==1):
				res_login = res_log[0]
				rol.set(res_login[2])
				login_menu()
			else:
				messagebox.showerror(title = "!Error" , message = "El usuario y contrasela no se encuentran registrados")
		else:
			messagebox.showerror(title = "!Error" , message = "Inserte alguna contraseña")
	else:
		messagebox.showerror(title = "!Error" , message = "Inserte algun nombre")

def limpiar_ord():
	var_id.set("")
	var_cliente.set("")
	var_identificacion.set("")
	var_celular.set("")
	var_estado.set("")
	var_solucion.set("")
	var_tecnico.set("")
def logout():
	rol.set("usuario")

def autenticar_consultar(x):
	if(len(x.get())==10):
		if(int_str(x.get())):
			cursor.execute(
				"select	idservicio,nombre_cliente, "+
				"identifi_cliente, "+
				"telefono,(select nombre from estado where idestado = servicio.estado_idestado) as estado,"+
				"solucion,(select nombre from usuario where idusuario =usuario_idusuario_tecnico) as tecnico "+
				"from servicio "+
				"where telefono = "+x.get()
			)
			res_consulta = cursor.fetchall()
			if(len(res_consulta)==1):
				var_id.set(res_consulta[0][0])
				var_cliente.set(res_consulta[0][1])
				var_identificacion.set(res_consulta[0][2])
				var_celular.set(res_consulta[0][3])
				var_estado.set(res_consulta[0][4])
				var_solucion.set(res_consulta[0][5])
				var_tecnico.set(res_consulta[0][6])
				consultar_consultar()
			else:
				messagebox.showerror(title = "!Error" , message = "El numero telefonico no se encuentra registrado a ningun servicio")

		else:
			messagebox.showerror(title = "!Error" , message = "El numero telefonico no es valido, por que contiene letras")
	else:
			messagebox.showerror(title = "!Error" , message = "El numero telefonico es muy pequeño, ingrese uno con 10 caracteres")

def autenticar_ingresart(nb,us,co,tipoid,idnum):
	if(len(nb.get())>2):
		if(len(us.get())>2):
			if(len(idnum.get())>=5 and len(idnum.get())<=10):
				if(int_str(idnum.get())):
					if(len(co.get())>2):
						cursor.execute(
						"select * "+
						"from usuario "+
						"where usuario='"+us.get()+"'"
						)
						res_exist = cursor.fetchall()
						if(len(res_exist)==0):
							cursor.execute(
								"select max(idusuario) from usuario"
							)
							res_id= cursor.fetchall()
							if(len(res_id)>=1):
								cursor.execute(
									"insert into usuario values ("+str(res_id[0][0]+1)+","+
										idnum.get()+",'"+nb.get()+"','"+us.get()+
										"','"+co.get()+"',2,"+str(src_indx(tipoid.get(), "tdocument"))+
									")"
								)
							else:
								cursor.execute(
									"insert into usuario values (1,"+
										idnum.get()+",'"+nb.get()+"','"+us.get()+
										"','"+co.get()+"',2,"+str(src_indx(tipoid.get(), "tdocument"))+
									")"
								)
							conection.commit()
							messagebox.showinfo(title = "!Exito" , message = "El usuario fue registrado satisfactoriamente")
						else:
							messagebox.showinfo(title = "!Error" , message = "El nombre de usuario fuer registrado anteriormente")
					else:
						messagebox.showerror(title = "!Error" , message = "La contraseña tiene caracteres insuficientes, porfavor ingrese una con mas de 2 caracteres")
				else:
					messagebox.showerror(title = "!Error" , message = "El numero de identificacion no es valido, por que contiene letras, porfavor ingrese solo numeros")
			else:
				messagebox.showerror(title = "!Error" , message = "El numero de identificacion tiene una cantidad de caracteres fuera del rango, porfavor ingrese un numero entre 5 y 10")
		else:
			messagebox.showerror(title = "!Error" , message = "El nombre de usuario tiene caracteres insuficientes, porfavor ingrese uno con mas de 2 caracteres")
	else:
		messagebox.showerror(title = "!Error" , message = "El nombre tiene caracteres insuficientes, porfavor ingrese uno con mas de 2 caracteres")

def autenticar_ingresaro(nb,idcc,tlf,matlf,modtlf,srl,tec,dsc):
	if(len(nb.get())>2):
		if(len(idcc.get())>=5 and len(idcc.get())<=10):
			if(int_str(idcc.get())):
				if(len(tlf.get())==10):
					if(int_str(tlf.get())):
						if(len(matlf.get())>3):
							if(len(modtlf.get())>3):
								if(len(srl.get())>2):
									if(len(dsc.get())>2):
										cursor.execute(
											"select max(idservicio) from servicio"
										)
										res_id= cursor.fetchall()
										if(res_id[0][0]!=None):
											cursor.execute(
												"insert into servicio values ("+str(res_id[0][0]+1)+",'"+nb.get()+"','"+idcc.get()+
												"','"+tlf.get()+"','"+matlf.get()+"','"+modtlf.get()+"','"+srl.get()+"','"+dsc.get()+
												"','formatear','"+str(datetime.datetime.now().strftime("%Y/%m/%d"))+"','"+str((datetime.datetime.now()+ datetime.timedelta(days=(random.randint(1, 3)))).strftime("%Y/%m/%d"))+"','"+str(src_indx(tec.get(),"tusuario"))+"','1')"
											)
										else:
											cursor.execute(
												"insert into servicio values (1,'"+nb.get()+"','"+idcc.get()+
												"','"+tlf.get()+"','"+matlf.get()+"','"+modtlf.get()+"','"+srl.get()+"','"+dsc.get()+
												"','formatear','"+str(datetime.datetime.now().strftime("%Y/%m/%d"))+"','"+str((datetime.datetime.now()+ datetime.timedelta(days=(random.randint(1, 3)))).strftime("%Y/%m/%d"))+"','"+str(src_indx(tec.get(),"tusuario"))+"','1')"
											)
										conection.commit()
										messagebox.showinfo(title = "!Excelente" , message = "La orden fue registrada satisfactoriamente")
									else:
										messagebox.showerror(title = "!Error" , message = "La descripcion del telefono tiene caracteres insuficientes, porfavor ingrese una con mas de 2 caracteres")
								else:
									messagebox.showerror(title = "!Error" , message = "El serial tiene caracteres insuficientes, porfavor ingrese uno con mas de 2 caracteres")
							else:
								messagebox.showerror(title = "!Error" , message = "El modelo tiene caracteres insuficientes, porfavor ingrese uno con mas de 3 caracteres")
						else:
							messagebox.showerror(title = "!Error" , message = "La Marca del telefono tiene caracteres insuficientes, porfavor ingrese una con mas de 3 caracteres")
					else:
						messagebox.showerror(title = "!Error" , message = "El numero de telefono no es valido, por que contiene letras, porfavor ingrese solo numeros")
				else:
						messagebox.showerror(title = "!Error" , message = "El numero de telefono tiene caracteres insuficientes, porfavor ingrese uno con 10 caracteres")
			else:
					messagebox.showerror(title = "!Error" , message = "El numero de identificacion no es valido, por que contiene letras, porfavor ingrese solo numeros")
		else:
			messagebox.showerror(title = "!Error" , message = "El numero de identificacion tiene una cantidad de caracteres fuera del rango, porfavor ingrese un numero entre 5 y 10")
	else:
		messagebox.showerror(title = "!Error" , message = "El nombre tiene caracteres insuficientes, porfavor ingrese uno con mas de 2 caracteres")
def autenticar_eliminar(x):
	cursor.execute(
		"delete "+
		"from servicio "+
		"where telefono = '"+x.get()+"'"
	)
	conection.commit()
	messagebox.showinfo(title = "!Excelente" , message = "Orden eliminada correctamente")
	limpiar_ord()
	consultar_consultar()

def autenticar_editar(x,y,z):
	if(y.get()=="terminado"):
		cursor.execute(
			"update servicio set solucion = '"+z.get()+
			"' ,estado_idestado = '"+str(src_indx(y.get(),"testado"))+"' ,fecha_entrega = '"+str(datetime.datetime.now().strftime("%Y/%m/%d"))+"' "+
			"where telefono = '"+x.get()+"'"
		)
	else:
		cursor.execute(
			"update servicio set solucion = '"+z.get()+"' ,estado_idestado = '"+str(src_indx(y.get(),"testado"))+"' "+
			"where telefono = '"+x.get()+"'"
		)
	conection.commit()
	messagebox.showinfo(title = "!Excelente" , message = "Orden editada correctamente")

def logout():
	rol.set("usuario")
	menu_login()

def limpiar(x):
	#playsound(onClick)
	for i in range(len(x)):
		x[i].set("")

def crear_ventana():
	global ventana
	ventana = Tk()
	ventana.geometry("600x600")
	#ventana.iconbitmap("icon.ico")
	ventana.title("Servicio tecnico de celulares")
	global rol
	rol = StringVar()
	rol.set("usuario")
	global var_id
	var_id = StringVar()
	global var_cliente
	var_cliente = StringVar()
	global var_identificacion
	var_identificacion = StringVar()
	global var_celular
	var_celular = StringVar()
	global var_estado
	var_estado = StringVar()
	global var_solucion
	var_solucion = StringVar()
	global var_tecnico
	var_tecnico = StringVar()
	crear_inicio()

def crear_inicio():
	global frame_inicio
	frame_inicio = Frame(ventana)
	frame_inicio.config(bg="#04111D")
	frame_inicio.place(x=0, y=0, width=600, height=600)
	titulo = Label(frame_inicio, text="Seleccione una opcion") 
	titulo.config(bg="#04111D",fg="white",font=('Verdana', 15))
	titulo.place( x=190,y=10)
	Button(frame_inicio, text ="Iniciar sesion",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=inicio_login).place(x=250, y=200,width=130,height=50)
	Button(frame_inicio, text ="Consultar orden",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=inicio_consultar).place(x=250, y=300,width=130,height=50)


def crear_login():
	global frame_login
	frame_login = Frame(ventana)
	frame_login.config(bg="#04111D")
	frame_login.place(x=0, y=0, width=600, height=600)
	titulo = Label(frame_login, text="Iniciar sesion") 
	titulo.config(bg="#04111D",fg="white",font=('Verdana', 15))
	titulo.place( x=240,y=10)
	lbl_nombre = Label(frame_login, text="Nombre de usuario") 
	lbl_nombre.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_nombre.place( x=250,y=75)
	aux_nombre = StringVar()
	nombre_entry = ttk.Entry(frame_login, textvariable=aux_nombre,width=50)
	nombre_entry.place(x=155, y=100)
	lbl_contraseña = Label(frame_login, text="Contraseña") 
	lbl_contraseña.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_contraseña.place( x=270,y=150)
	aux_contraseña = StringVar()
	contraseña_entry = ttk.Entry(frame_login,show="*", textvariable=aux_contraseña,width=50)
	contraseña_entry.place(x=155, y=175)
	Button(frame_login, text ="Ingresar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:autenticar_login(aux_nombre,aux_contraseña)).place(x=250, y=300,width=130,height=50)
	Button(frame_login, text ="Limpiar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:limpiar([aux_nombre,aux_contraseña])).place(x=250, y=360,width=130,height=50)
	Button(frame_login, text ="Volver",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=login_inicio).place(x=250, y=420,width=130,height=50)

def crear_menu():
	global frame_menu
	frame_menu = Frame(ventana)
	frame_menu.config(bg="#04111D")
	frame_menu.place(x=0, y=0, width=600, height=600)
	if(rol.get() == "administrador"):
		Button(frame_menu, text ="Ingresar tecnicos",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=menu_ingresart).place(x=250, y=120,width=130,height=50)
		Button(frame_menu, text ="Ingresar ordenes",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=menu_ingresaro).place(x=250, y=220,width=130,height=50)
		Button(frame_menu, text ="Consultar ordenes",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:menu_consultar()).place(x=250, y=320,width=130,height=50)
	else:
		Button(frame_menu, text ="Ingresar ordenes",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=menu_ingresaro).place(x=250, y=120,width=130,height=50)
		Button(frame_menu, text ="Consultar ordenes",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:menu_consultar()).place(x=250, y=270,width=130,height=50)
	Button(frame_menu, text ="Volver",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=logout).place(x=250, y=420,width=130,height=50)


def crear_ingresart():
	global frame_ingresart
	frame_ingresart = Frame(ventana)
	frame_ingresart.config(bg="#04111D")
	frame_ingresart.place(x=0, y=0, width=600, height=600)
	titulo = Label(frame_ingresart, text="Ingresar tecnicos") 
	titulo.config(bg="#04111D",fg="white",font=('Verdana', 15))
	titulo.place( x=230,y=10)
	lbl_nombre = Label(frame_ingresart, text="Nombre") 
	lbl_nombre.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_nombre.place( x=293,y=75)
	aux_nombre = StringVar()
	nombre_entry = ttk.Entry(frame_ingresart, textvariable=aux_nombre,width=35)
	nombre_entry.place(x=212, y=100)
	lbl_usuario = Label(frame_ingresart, text="Usuario") 
	lbl_usuario.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_usuario.place( x=133,y=150)
	aux_usuario = StringVar()
	usuario_entry = ttk.Entry(frame_ingresart, textvariable=aux_usuario,width=35)
	usuario_entry.place(x=50, y=175)
	lbl_contraseña = Label(frame_ingresart, text="Contraseña") 
	lbl_contraseña.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_contraseña.place( x=418,y=150)
	aux_contraseña = StringVar()
	contraseña_entry = ttk.Entry(frame_ingresart, textvariable=aux_contraseña,width=35)
	contraseña_entry.place(x=350, y=175)
	lbl_tipoid = Label(frame_ingresart, text="Tipo de documento") 
	lbl_tipoid.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_tipoid.place( x=90,y=225)
	aux_tipoid = StringVar()
	tipoid_entry = ttk.Combobox(frame_ingresart, 
                            values=[
                                    'TI', 
                                    'CC',
                                    'CI'], textvariable=aux_tipoid,width=32)
	tipoid_entry.place(x=50, y=250)
	lbl_idnum = Label(frame_ingresart, text="Numero de documento") 
	lbl_idnum.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_idnum.place( x=388,y=225)
	aux_idnum = StringVar()
	idnum_entry = ttk.Entry(frame_ingresart, textvariable=aux_idnum,width=35)
	idnum_entry.place(x=350, y=250)
	Button(frame_ingresart, text ="Volver",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=ingresart_menu).place(x=100, y=420,width=130,height=50)
	Button(frame_ingresart, text ="Limpiar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:limpiar([aux_nombre,aux_usuario,aux_contraseña,aux_tipoid,aux_idnum])).place(x=250, y=420,width=130,height=50)
	Button(frame_ingresart, text ="Registrar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:autenticar_ingresart(aux_nombre,aux_usuario,aux_contraseña,aux_tipoid,aux_idnum)).place(x=400, y=420,width=130,height=50)

def crear_ingresaro():
	global frame_ingresaro
	global var_usuario
	cursor.execute(
		"select idusuario, nombre "+
		"from usuario "+
		"where rol_idrol = (select idrol from tipo_usuario where nombre != 'administrador')"
	)
	var_usuario= cursor.fetchall()
	frame_ingresaro = Frame(ventana)
	frame_ingresaro.config(bg="#04111D")
	frame_ingresaro.place(x=0, y=0, width=600, height=600)
	titulo = Label(frame_ingresaro, text="Ingresar ordenes") 
	titulo.config(bg="#04111D",fg="white",font=('Verdana', 15))
	titulo.place( x=230,y=10)
	lbl_nombre = Label(frame_ingresaro, text="Nombre cliente") 
	lbl_nombre.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_nombre.place( x=106,y=75)
	aux_nombre = StringVar()
	nombre_entry = ttk.Entry(frame_ingresaro, textvariable=aux_nombre,width=35)
	nombre_entry.place(x=50, y=100)
	lbl_identificacion = Label(frame_ingresaro, text="Identificacion del cliente") 
	lbl_identificacion.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_identificacion.place( x=374,y=75)
	aux_identificacion = StringVar()
	identificacion_entry = ttk.Entry(frame_ingresaro, textvariable=aux_identificacion,width=35)
	identificacion_entry.place(x=350, y=100)
	lbl_telefono = Label(frame_ingresaro, text="Telefono") 
	lbl_telefono.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_telefono.place( x=125,y=150)
	aux_telefono = StringVar()
	telefono_entry = ttk.Entry(frame_ingresaro, textvariable=aux_telefono,width=35)
	telefono_entry.place(x=50, y=175)
	lbl_marca = Label(frame_ingresaro, text="Marca telefono") 
	lbl_marca.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_marca.place( x=408,y=150)
	aux_marca = StringVar()
	marca_entry = ttk.Entry(frame_ingresaro, textvariable=aux_marca,width=35)
	marca_entry.place(x=350, y=175)
	lbl_modelo = Label(frame_ingresaro, text="Modelo telefono") 
	lbl_modelo.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_modelo.place( x=100,y=225)
	aux_modelo = StringVar()
	modelo_entry = ttk.Entry(frame_ingresaro, textvariable=aux_modelo,width=35)
	modelo_entry.place(x=50, y=250)
	lbl_serial = Label(frame_ingresaro, text="Serial") 
	lbl_serial.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_serial.place( x=433,y=225)
	aux_serial = StringVar()
	serial_entry = ttk.Entry(frame_ingresaro, textvariable=aux_serial,width=35)
	serial_entry.place(x=350, y=250)
	lbl_tecnico = Label(frame_ingresaro, text="Tecnico") 
	lbl_tecnico.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_tecnico.place( x=125,y=300)
	aux_tecnico = StringVar()
	var_tecnicos_entry = []
	for i in range(len(var_usuario)):
		var_tecnicos_entry.append(var_usuario[i][1])
	tecnico_entry = ttk.Combobox(frame_ingresaro, 
                            values=var_tecnicos_entry, textvariable=aux_tecnico,width=32)
	tecnico_entry.place(x=50, y=325)
	lbl_descripcion = Label(frame_ingresaro, text="Descripcion del problema") 
	lbl_descripcion.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_descripcion.place( x=373,y=300)
	aux_descripcion = StringVar()
	descripcion_entry = ttk.Entry(frame_ingresaro, textvariable=aux_descripcion,width=35)
	descripcion_entry.place(x=350, y=325)
	Button(frame_ingresaro, text ="Volver",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=ingresaro_menu).place(x=100, y=420,width=130,height=50)
	Button(frame_ingresaro, text ="Limpiar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:limpiar([aux_nombre,aux_identificacion,aux_telefono,aux_marca,aux_modelo,aux_serial,aux_tecnico,aux_descripcion])).place(x=250, y=420,width=130,height=50)
	Button(frame_ingresaro, text ="Registrar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:autenticar_ingresaro(aux_nombre,aux_identificacion,aux_telefono,aux_marca,aux_modelo,aux_serial,aux_tecnico,aux_descripcion)).place(x=400, y=420,width=130,height=50)

def crear_consultar():
	global frame_consultar
	frame_consultar = Frame(ventana)
	frame_consultar.config(bg="#04111D")
	frame_consultar.place(x=0, y=0, width=600, height=600)
	titulo = Label(frame_consultar, text="Consultar ordenes") 
	titulo.config(bg="#04111D",fg="white",font=('Verdana', 15))
	titulo.place( x=210,y=10)
	lbl_celular = Label(frame_consultar, text="Numero de telefono") 
	lbl_celular.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_celular.place( x=240,y=75)
	aux_celular = StringVar() 
	celular_entry = ttk.Entry(frame_consultar, textvariable=aux_celular,width=50)
	celular_entry.place(x=155, y=100)
	if(var_estado.get()!=""):
		aux_idorden = var_id.get()
		lbl_idorden = Label(frame_consultar, text=aux_idorden) 
		lbl_idorden.config(bg="#04111D",fg="white",font=('Verdana', 10))
		lbl_idorden.place( x=275,y=170)
		aux_cliente = "Cliente: "+var_cliente.get()
		lbl_cliente = Label(frame_consultar, text=aux_cliente) 
		lbl_cliente.config(bg="#04111D",fg="white",font=('Verdana', 10))
		lbl_cliente.place( x=100,y=205)
		aux_id = "Identificacion: "+var_identificacion.get()
		lbl_id = Label(frame_consultar, text=aux_id) 
		lbl_id.config(bg="#04111D",fg="white",font=('Verdana', 10))
		lbl_id.place( x=320,y=205)
		aux_celular = "Celular: "+var_celular.get()
		lbl_celular = Label(frame_consultar, text=aux_celular) 
		lbl_celular.config(bg="#04111D",fg="white",font=('Verdana', 10))
		lbl_celular.place( x=100,y=230)
		aux_estado = "Estado: "+var_estado.get()
		lbl_estado = Label(frame_consultar, text=aux_estado) 
		lbl_estado.config(bg="#04111D",fg="white",font=('Verdana', 10))
		lbl_estado.place( x=320,y=230)
		aux_solucion = "Solucion: "+var_solucion.get()
		lbl_solucion = Label(frame_consultar, text=aux_solucion) 
		lbl_solucion.config(bg="#04111D",fg="white",font=('Verdana', 10))
		lbl_solucion.place( x=100,y=255)
		aux_tecnico = "Tecnico: "+var_tecnico.get()
		lbl_tecnico = Label(frame_consultar, text=aux_tecnico) 
		lbl_tecnico.config(bg="#04111D",fg="white",font=('Verdana', 10))
		lbl_tecnico.place( x=320,y=255)
		if(rol.get()!="usuario"):
			Button(frame_consultar, text ="Editar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:consultar_editar(var_celular)).place(x=320, y=420,width=130,height=50)
			Button(frame_consultar, text ="eliminar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:autenticar_eliminar(var_celular)).place(x=320, y=330,width=130,height=50)
			Button(frame_consultar, text ="Consultar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:autenticar_consultar(aux_celular)).place(x=150, y=330,width=130,height=50)
			Button(frame_consultar, text ="Volver",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=consultar_menu).place(x=150, y=420,width=130,height=50)
		else:
			Button(frame_consultar, text ="Consultar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:autenticar_consultar(aux_celular)).place(x=250, y=330,width=130,height=50)
			Button(frame_consultar, text ="Volver",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=consultar_inicio).place(x=250, y=420,width=130,height=50)

	else:
		Button(frame_consultar, text ="Consultar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:autenticar_consultar(aux_celular)).place(x=250, y=330,width=130,height=50)
		Button(frame_consultar, text ="Volver",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=consultar_inicio).place(x=250, y=420,width=130,height=50)

def crear_editar(x):
	global frame_editar
	frame_editar = Frame(ventana)
	frame_editar.config(bg="#04111D")
	frame_editar.place(x=0, y=0, width=600, height=600)
	titulo = Label(frame_editar, text="Editar ordenes") 
	titulo.config(bg="#04111D",fg="white",font=('Verdana', 15))
	titulo.place( x=238,y=10)
	lbl_estado = Label(frame_editar, text="Estado") 
	lbl_estado.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_estado.place( x=287,y=75)
	aux_estado = StringVar() 
	estado_entry = ttk.Combobox(frame_editar, 
                            values=[
								"recibido","terminado","en proceso"
							], textvariable=aux_estado,width=47)
	estado_entry.place(x=155, y=100)
	lbl_solucion = Label(frame_editar, text="Solucion") 
	lbl_solucion.config(bg="#04111D",fg="white",font=('Verdana', 10))
	lbl_solucion.place( x=285,y=175)
	aux_solucion = StringVar() 
	solucion_entry = ttk.Entry(frame_editar, textvariable=aux_solucion,width=50)
	solucion_entry.place(x=155, y=200)
	Button(frame_editar, text ="editar",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=lambda:autenticar_editar(x,aux_estado,aux_solucion)).place(x=250, y=330,width=130,height=50)
	Button(frame_editar, text ="Volver",font=('Verdana', 9, "bold"),overrelief="sunken", cursor="hand2",command=editar_consultar).place(x=250, y=420,width=130,height=50)


def inicio_login():
	#playsound(onClick)
	eliminar(frame_inicio)
	crear_login()

def login_inicio():
	#playsound(onClick)
	eliminar(frame_login)
	crear_inicio()

def inicio_consultar():
	#playsound(onClick)
	eliminar(frame_inicio)
	crear_consultar()

def consultar_inicio():
	limpiar_ord()
	logout()
	#playsound(onClick)
	eliminar(frame_consultar)
	crear_inicio()

def consultar_consultar():
	#playsound(onClick)
	eliminar(frame_consultar)
	crear_consultar()

def login_menu():
	#playsound(onClick)
	eliminar(frame_login)
	crear_menu()

def menu_login():
	#playsound(onClick)
	eliminar(frame_menu)
	crear_login()

def menu_ingresart():
	#playsound(onClick)
	eliminar(frame_menu)
	crear_ingresart()

def ingresart_menu():
	#playsound(onClick)
	eliminar(frame_ingresart)
	crear_menu()

def menu_ingresaro():
	#playsound(onClick)
	eliminar(frame_menu)
	crear_ingresaro()

def ingresaro_menu():
	#playsound(onClick)
	eliminar(frame_ingresaro)
	crear_menu()

def menu_consultar():
	#playsound(onClick)
	eliminar(frame_menu)
	crear_consultar()

def consultar_menu():
	#playsound(onClick)
	limpiar_ord()
	eliminar(frame_consultar)
	crear_menu()

def editar_consultar():
	#playsound(onClick)
	limpiar_ord()
	eliminar(frame_editar)
	crear_consultar()

def consultar_editar(x):
	#playsound(onClick)
	eliminar(frame_consultar)
	crear_editar(x)

def eliminar(x):
	x.destroy()

crear_ventana()
ventana.mainloop()
cursor.close()