import cv2
from cv2 import sepFilter2D
import numpy as np
from tkinter import *
from PIL import ImageTk,Image
import imutils
import logging
import threading
import time
import datetime
from ventana_gestionar_camaras import ventana_gestionar_camaras
from manipular_datos import leer_estado_camaras
import time
from absl import app, flags, logging
from absl.flags import FLAGS
import tensorflow as tf
from yolov3_tf2.models import (YoloV3, YoloV3Tiny)
from yolov3_tf2.dataset import transform_images
from yolov3_tf2.utils import draw_outputs, get_class_colors
import os
from tensorflow.python.client import timeline
import json

class ventana_inicio:
    def __init__(self):
        flags.DEFINE_string('classes', './data/coco.names', 'path to classes file')
        flags.DEFINE_string('weights', './checkpoints/yolov3.tf',
                            'path to weights file')
        flags.DEFINE_boolean('tiny', False, 'yolov3 or yolov3-tiny')
        flags.DEFINE_integer('size', 320, 'resize images to')
        flags.DEFINE_string('video', '0',
                            'path to video file or number for webcam)')
        flags.DEFINE_string('output', None, 'path to output video')
        flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
        flags.DEFINE_integer('num_classes', 80, 'number of classes in the model')
        flags.DEFINE_boolean('trace', False, 'trace each frame')
        flags.DEFINE_boolean('headless', False, 'do not display frames (useful for tracing)')
        flags.DEFINE_integer('max_frames', 0, 'max number of video frames to process (defaults to all)')
        flags.DEFINE_string('colors', './data/colors.json', 'path to class colors file')
        flags.DEFINE_boolean('eager', False, 'enables eager execution (unless tracing)')
        self.captura=None
        self.ventana=None
        self.frameBotones=None
        self.frameCamaras=None
        self.botonGestionCamaras=None
        self.imagen1=None
        self.camara1=None
        self.inice_antes=False
        self.archivo_js=None
        self.sess = tf.keras.backend.get_session()
        self.run_options = None
        self.run_metadata = None
        
        self.physical_devices = tf.config.experimental.list_physical_devices('GPU')
        if len(self.physical_devices) > 0:
            tf.config.experimental.set_memory_growth(self.physical_devices[0], True)
        time.sleep(5)
        if False:
            yolo = YoloV3Tiny(classes=80)
        else:
            yolo = YoloV3(classes=80)


    def pintar(self):
        self.ventana=Tk()
        self.ventana.title("video vigilancia inteligente")
        self.ventana.geometry("1000x600")
        self.ventana.config(bg="#112B3C")

        self.frameBotones=Frame(self.ventana)
        self.frameCamaras=Frame(self.ventana)
        self.frameBotones.config(bg="#293462") 
        self.frameCamaras.config(bg="#293462")
        self.frameBotones.config(width=480,height=500)
        self.frameCamaras.config(width=880,height=590)

        self.botonGestionCamaras=Button(self.frameBotones,text="Administrar camaras",command=ventana_gestionar_camaras)
        self.imagen1=ImageTk.PhotoImage(Image.open('../assets/camera_unavailable.PNG').resize((200,200)))
        self.camara1=Label(self.frameCamaras,image=self.imagen1,bg="black")
        self.frameBotones.grid(row=0,column=0)
        self.botonGestionCamaras.grid(row=0,column=0)
        self.frameCamaras.grid(row=0,column=2)
        self.camara1.grid(row=0,column=0)

        self.archivo_js=leer_estado_camaras()
        if(self.archivo_js["camara_1"]["estado"]=="conectado"):
            self.captura=cv2.VideoCapture(0,cv2.CAP_DSHOW)
            self.visualizar()

        self.ventana.mainloop()
        #self.recuperar_estado_camaras()
        

    # def recuperar_estado_camaras(self):
    #     self.archivo_js=leer_estado_camaras()
    #     if(self.archivo_js["camara_1"]["estado"]=="conectado"):
    #         self.iniciar(0)



    def visualizar(self):
        if self.captura is not None:
            ret,frame=self.captura.read()
            if ret ==True:             
                frame=imutils.resize(frame,width=500)
                frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

                im=Image.fromarray(frame)
                img=ImageTk.PhotoImage(image=im)

                self.camara1.configure(image=img)
                self.camara1.image=img
                self.camara1.after(10,self.visualizar)
            else:
                self.camara1.image=""
                self.captura.release()
        else:
            self.camara1.image=""
            self.captura.release()

    # def vizualizar_2(self):
    #     #vid = cv2.VideoCapture(0)
    #     if(self.captura) is not None:
    #         ret, img = self.captura.read()
    #         if ret:
    #             img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    #             img_in = cv2.resize(img_in, dsize=(FLAGS.size, FLAGS.size))
    #             img_in = np.expand_dims(img_in, 0) / 255.0
    #             t1 = time.time()
    #             if FLAGS.eager:
    #                 boxes, scores, classes, nums = self.yolo.predict(img_in)
    #             else:
    #                 boxes, scores, classes, nums = self.sess.run(
    #                     self.yolo.output, 
    #                     feed_dict={self.yolo.input: img_in},
    #                     options=self.run_options, 
    #                     run_metadata=self.run_metadata)
                        
    #             t2 = time.time()
    #             times.append(t2-t1)
    #             times = times[-20:]

    #             if FLAGS.trace:
    #                 fetched_timeline = timeline.Timeline(self.run_metadata.step_stats)
    #                 chrome_trace = fetched_timeline.generate_chrome_trace_format()
    #                 with open(os.path.join(self.trace_dir, f"{self.trace_basename}_{frame_index}.json"), 'w') as f:
    #                     f.write(chrome_trace)
    #                 # No need to dump graph partitions for every frame; they should be identical.
    #                 if frame_index == 0:
    #                     for i in range(len(self.run_metadata.partition_graphs)):
    #                         with open(os.path.join(self.graphs_dir, f"partition_{i}.pbtxt"), 'w') as f:
    #                             f.write(str(self.run_metadata.partition_graphs[i]))

    #             img = draw_outputs(img, (boxes, scores, classes, nums), self.class_names, self.class_colors)
    #             img = cv2.putText(img, "Time: {:.2f}ms".format(sum(times)/len(times)*1000), (0, 30),
    #                             cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)
    #             if FLAGS.output:
    #                 self.out.write(img)
    #             if not FLAGS.headless:
    #                 im=Image.fromarray(img)
    #                 photo_img=ImageTk.PhotoImage(image=im)

    #                 self.camara1.configure(image=photo_img)
    #                 self.camara1.image=photo_img
    #                 self.camara1.after(10,self.visualizar_2)
    #                 # cv2.imshow('output', img)
    #                 print("hello")
    #             frame_index += 1



            

##
    def cargar_estado_camaras(self):
        while True:
            self.archivo_js=leer_estado_camaras()
            if (self.archivo_js["camara_1"]["estado"]=="conectado"):
                if not(self.inice_antes):
                    self.inice_antes=True
                    self.captura=cv2.VideoCapture(0,cv2.CAP_DSHOW)
                    self.visualizar()
            else:
                if(self.captura!=None):
                    self.captura.release()
                    self.inice_antes=False
                    self.imagen1=ImageTk.PhotoImage(Image.open('../assets/camera_unavailable.PNG').resize((200,200)))
                    self.camara1.config(image=self.imagen1)
            time.sleep(1)
            
def hilos():
    ventana_principal=ventana_inicio()
    canal_1=threading.Thread(name="ventana_principal",target=ventana_principal.pintar,args=())
    canal_2=threading.Thread(name="contador",target=ventana_principal.cargar_estado_camaras,args=())    
    canal_1.start()
    canal_2.start()

    canal_1.join()
    canal_2.join()

hilos()



        
        # capCamera = cv2.VideoCapture(0)
# capVideo  = cv2.VideoCapture("C:/Users/Mirco/Documents/proyecto de grado/vista/minecraft.mp4")

# while True:
#     exitoCamara, imagenCamara = capCamera.read()
#     exitoVideo, imagenVideo = capVideo.read()


#     final = cv2.hconcat([imagenCamara,imagenCamara])
#     cv2.imshow("fina",final)

#     if cv2.waitKey(1) & 0xFF==ord('q'):
#      break

# capCamera.release()
# capVideo.release()
# cv2.destroyAllWindows()

