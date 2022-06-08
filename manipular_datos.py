import json

def leer_estado_camaras():
    archivo=open("../registros/estado_camaras.json","r")
    camaras_js=json.loads(archivo.read())
    archivo.close()
    return camaras_js

def guardar_estado_camaras(archivo_js):
    archivo=open("../registros/estado_camaras.json","w")
    camaras_js=json.dumps(archivo_js,indent=4)
    archivo.write(camaras_js)
    archivo.close()
    return camaras_js

def leer_camara(numero_slot):
    return leer_estado_camaras()["camara_"+str(numero_slot)]


def desactivar_camara(numero_slot):
    archivo_js=leer_estado_camaras()
    if( archivo_js["camara_"+str(numero_slot)]["estado"]=="conectado"):
        archivo_js["camara_"+str(numero_slot)]["nombre"]=""
        archivo_js["camara_"+str(numero_slot)]["modelo"]=""
        archivo_js["camara_"+str(numero_slot)]["estado"]="desconectado"
    guardar_estado_camaras(archivo_js)


def activar_camara(nombre,modelo,numero_slot):
    archivo_js=leer_estado_camaras()
    if( archivo_js["camara_"+str(numero_slot)]["estado"]=="desconectado"):
        archivo_js["camara_"+str(numero_slot)]["nombre"]=nombre
        archivo_js["camara_"+str(numero_slot)]["modelo"]=modelo
        archivo_js["camara_"+str(numero_slot)]["estado"]="conectado"
    print(nombre)
    print(numero_slot)
    guardar_estado_camaras(archivo_js)




