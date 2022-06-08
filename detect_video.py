from traceback import print_tb
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

vid=None
sess=None
yolo=None
run_options=None
run_metadata=None
class_names=None
class_colors=None
times=None
frame_index=None
camara1=None
inice_antes=False
frame_index=0

def visualizar():
    global vid
    global sess
    global yolo
    global run_options
    global run_metadata
    global class_names
    global class_colors
    global times
    global frame_index
    global camara1
    global inice_antes
    frame_index=0
    if vid is not None:
        ret, img = vid.read()
        if ret ==True:
                img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                img_in = cv2.resize(img_in, dsize=(FLAGS.size, FLAGS.size))
                img_in = np.expand_dims(img_in, 0) / 255.0

                t1 = time.time()
                boxes, scores, classes, nums = sess.run(yolo.output,feed_dict={yolo.input: img_in}, 
                                                        options=run_options,run_metadata=run_metadata)
                t2 = time.time()
                times.append(t2-t1)
                times = times[-20:]
                img = draw_outputs(img, (boxes, scores, classes, nums), class_names, class_colors)
                img = cv2.putText(img, "Time: {:.2f}ms".format(sum(times)/len(times)*1000), (0, 30),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)  

                im=Image.fromarray(img)
                imagen1=ImageTk.PhotoImage(image=im)

                camara1.configure(image=imagen1)
                camara1.image=imagen1
                camara1.after(10,ciclo1)
        else:
                camara1.image=""
                vid.release()


def main(_argv):
    global vid
    global sess
    global yolo
    global run_options
    global run_metadata
    global class_names
    global class_colors
    global times
    global frame_index
    global camara1
    global inice_antes

    if FLAGS.eager and not FLAGS.trace:
        tf.compat.v1.enable_eager_execution()
    else:
        sess = tf.keras.backend.get_session()
        run_options = None
        run_metadata = None

    physical_devices = tf.config.experimental.list_physical_devices('GPU')

    if len(physical_devices) > 0:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    yolo = YoloV3(classes=FLAGS.num_classes)

    yolo.load_weights(FLAGS.weights)
    logging.info('weights loaded')
    class_names = [c.strip() for c in open(FLAGS.classes).readlines()]
    class_colors = get_class_colors(FLAGS.colors, class_names)
    logging.info('classes loaded')
    times = []

    out = None
    frame_index=0

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

    botonGestionCamaras=Button(frameBotones,text="Administrar camaras",command=ventana_gestionar_camaras)
    imagen1=ImageTk.PhotoImage(Image.open('../assets/camera_unavailable.PNG').resize((200,200)))
    camara1=Label(frameCamaras,image=imagen1,bg="black")
    frameBotones.grid(row=0,column=0)
    botonGestionCamaras.grid(row=0,column=0)
    frameCamaras.grid(row=0,column=2)
    camara1.grid(row=0,column=0)

    
    archivo_js=leer_estado_camaras()
    if(archivo_js["camara_1"]["estado"]=="conectado"):
        vid=cv2.VideoCapture(0)
        ciclo1()

    ventana.mainloop()
    # cargar_frame_pricipal()
    # cargar_espacio1()
    # cargar_espacio2()
    # cargar_espacio3()
    # cargar_espacio4()

    
    cv2.destroyAllWindows()

def ciclo1():
        global vid
        global sess
        global yolo
        global run_options
        global run_metadata
        global class_names
        global class_colors
        global times
        global frame_index
        global camara1
        global inice_antes

        if vid is not None:
            ret, img = vid.read()
            if ret ==True:
                img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                img_in = cv2.resize(img_in, dsize=(FLAGS.size, FLAGS.size))
                img_in = np.expand_dims(img_in, 0) / 255.0

                t1 = time.time()
                boxes, scores, classes, nums = sess.run(yolo.output,feed_dict={yolo.input: img_in}, 
                                                        options=run_options,run_metadata=run_metadata)
                t2 = time.time()
                times.append(t2-t1)
                times = times[-20:]
                img = draw_outputs(img, (boxes, scores, classes, nums), class_names, class_colors)
                img = cv2.putText(img, "Time: {:.2f}ms".format(sum(times)/len(times)*1000), (0, 30),
                                cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 2)  

                im=Image.fromarray(img)
                imagen1=ImageTk.PhotoImage(image=im)

                camara1.configure(image=imagen1)
                camara1.image=imagen1
                camara1.after(10,ciclo1)
            else:
                camara1.image=""
                vid.release()
        else:
            camara1.image=""
            vid.release()

        ###
def cargar_estado_camaras(self):
    global vid
    global sess
    global yolo
    global run_options
    global run_metadata
    global class_names
    global class_colors
    global times
    global frame_index
    global camara1
    global inice_antes

    while True:
        archivo_js=leer_estado_camaras()
        if (archivo_js["camara_1"]["estado"]=="conectado"):
            if not(inice_antes):
                inice_antes=True
                captura=cv2.VideoCapture(0)
                ciclo1()
        else:
            if(vid!=None):
                vid.release()
                inice_antes=False
                imagen1=ImageTk.PhotoImage(Image.open('../assets/camera_unavailable.PNG').resize((200,200)))
                camara1.config(image=imagen1)
        time.sleep(1)      

def iniciar():
     app.run(main)





if __name__ == '__main__':
    try:
        canal_1=threading.Thread(name="ventana_principal",target=iniciar,args=())
        canal_2=threading.Thread(name="contador",target=cargar_estado_camaras,args=())    
        canal_1.start()
        canal_2.start()

        canal_1.join()
        canal_2.join()
    except SystemExit:
        pass
