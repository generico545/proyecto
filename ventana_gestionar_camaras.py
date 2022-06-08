from tkinter import *
from ventana_registro import ventana_registro_camara
from manipular_datos import *


class ventana_gestionar_camaras:

    def cerrar_editor(self):
        self.campoNombre1.destroy()
        self.menu1.destroy()
        self.modelo1.destroy()
        self.botonAceptarCambios1.destroy()
        self.botonCancelarEditar1.destroy()
        self.iniciar_componentes()

    def abrir_editor(self):
        self.nombre1.destroy()
        self.modelo1.destroy()
        self.estado1.destroy()
        self.botonEditar1.destroy()
        self.botonBorrar1.destroy()

        self.campoNombre1.grid(row=2,column=0)
        self.menu1.grid(row=4,column=0)
        self.botonAceptarCambios1.grid(row=5,column=0)
        self.botonCancelarEditar1.grid(row=5,column=1)

    def eliminar_camara(self):
        self.nombre1.destroy()
        self.modelo1.destroy()
        self.estado1.destroy()
        self.botonEditar1.destroy()
        self.botonBorrar1.destroy()
        desactivar_camara(1)
        self.iniciar_componentes()


    def guardar_cambios():
        print()        

    def actualizar_ventana(self):
        nombre=self.campoNombre1.get()
        modelo="camara 1"
        activar_camara(nombre=nombre,modelo=modelo,numero_slot=1)
        self.cerrar_editor()
        


    def iniciar_componentes(self):
        self.datos_js=leer_estado_camaras()

        self.nombre1=Label(self.frameCamaras,text=self.datos_js["camara_1"]["nombre"])
        self.estado1=Label(self.frameCamaras,text=self.datos_js["camara_1"]["estado"])
        self.modelo1=Label(self.frameCamaras,text=self.datos_js["camara_1"]["modelo"])

        self.campoNombre1=Entry(self.frameCamaras)
        self.variable = StringVar(self.frameCamaras)
        self.variable.set("seleccione una camara") 
        self.menu1 = OptionMenu(self.frameCamaras, self.variable,"camara 1") 

        self.botonEditar1=Button(self.frameCamaras,text="Editar",command=self.abrir_editor)
        self.botonBorrar1=Button(self.frameCamaras,text="Eliminar",command=self.eliminar_camara)

        self.botonAceptarCambios1=Button(self.frameCamaras,text="Aceptar Cambios",command=self.actualizar_ventana)
        self.botonCancelarEditar1=Button(self.frameCamaras,text="Cancelar",command=self.cerrar_editor)
        
        self.nombre1.grid(row=2,column=0)
        self.estado1.grid(row=3,column=0)
        self.modelo1.grid(row=4,column=0)
        self.botonEditar1.grid(row=5,column=0)
        self.botonBorrar1.grid(row=5,column=1)
      

        # self.botonAgregar1.grid(row=5,column=0)
        # self.botonAgregar1=Button(self.frameCamaras,text="agregar camara",command=self.abrir_editor)
       

    def __init__(self):
        self.ventana=Tk(className="Adiministrar camaras")
        self.ventana.geometry("700x500")
        self.titulo=Label(self.ventana,text="Adiministrar camaras")
        self.frameCamaras=LabelFrame(self.ventana)
        self.frameCamaras.config(width=600,height=450)
        self.titulo.grid(row=0,column=2)
        self.frameCamaras.grid(row=2,column=2)

        self.iniciar_componentes()
        self.ventana.mainloop()


    





