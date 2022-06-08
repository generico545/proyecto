from tkinter import *
from PIL import Image
from PIL import ImageTk
import cv2
import imutils


def visualizar():
    global cap 
    if cap is not None:
        ret,frame=cap.read()
        if ret ==True:
            frame=imutils.resize(frame,width=640)
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

            im=Image.fromarray(frame)
            img=ImageTk.PhotoImage(image=im)

            camara1.configure(image=img)
            camara1.image=img
            camara1.after(10,visualizar)
        else:
            camara1.image=""
            cap.release()
def iniciar():
    global cap
    cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    visualizar()

# 
cap=None
ventana=Tk()
ventana.title("video vigilancia inteligente")
ventana.geometry("1000x600")
ventana.config(bg="#112B3C")

frameBotones=Frame(ventana)
frameCamaras=Frame(ventana)

frameBotones.config(bg="#293462") 
frameCamaras.config(bg="#293462")

frameBotones.config(width=480,height=500)
frameCamaras.config(width=880,height=590)

botonGestionCamaras=Button(frameBotones,text="Administrar camaras")


camara1=Label(frameCamaras,bg="black")

    
frameBotones.grid(row=0,column=0)
botonGestionCamaras.grid(row=0,column=0)

frameCamaras.grid(row=0,column=2)
camara1.grid(row=0,column=0)

iniciar()

ventana.mainloop()

