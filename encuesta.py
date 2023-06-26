#PROGRAMA PRINCIPAL - CATDOG


from contextlib import nullcontext


import os
from flask import Flask, send_from_directory, redirect, url_for ,render_template, request
from werkzeug.utils import secure_filename

from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
import pymongo

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO


app = Flask(__name__)

CONNECTION_STRING ="mongodb+srv://Zahir:ocH56Zt0eFAyY576@cluster0.ympcfrg.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(CONNECTION_STRING)

db = client.Software

coleccion = db.Registro


#app.config['UPLOAD_FOLDER'] = 'static/images'
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


no_encuesta = 0
encuestas = {}



@app.route("/")
def home():
    return render_template("base.html")


@app.route('/encuesta', methods = ['POST', 'GET'])
def encuesta():
    
    if request.method == 'POST':
        
        plataforma = request.form['plataforma']
        contenido = request.form['contenido']
        genero = request.form['genero']
        videoseducativos = request.form['videoseducativos']
        duracion = request.form['duracion']
        nombre = request.form['nombre']
       
        """
        ESTA PARTE DEL CÓDIGO ES PARA SUBIR IMÁGENES AL SERVIDOR
        file = request.files['archivo']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        filename = 'images/' + filename
        """

        global no_encuesta
        no_encuesta += 1
        id_encuesta = (str(no_encuesta))
        nueva_encuesta = {
            
           
            "plataforma" : plataforma,
            "contenido" : contenido,
            "genero" : genero,
            "videoseducativos" : videoseducativos,
            "duracion" : duracion,
            "nombre" : nombre
            
        }

        encuestas.update({id_encuesta : nueva_encuesta})

       
        coleccion.insert_one(nueva_encuesta)
        
        #datos = (nombre, raza, sexo, caracter, color, edad, tamanio, salud, sociable, contacto, filename)
        #return redirect(url_for("lista", data=datos))
        return resultados(data=encuestas)
        
        
    
    else:
        pass
        return render_template("encuesta.html")
     

@app.route('/resultados', methods = ['POST', 'GET'])
def resultados(data={}):
    def resultados(data={}):
        df = pd.DataFrame.from_dict(data, orient='index')

    # Obtener los conteos de cada plataforma
        plataforma_counts = df['plataforma'].value_counts()

    # Obtener los conteos de cada género
        genero_counts = df['genero'].value_counts()

    # Crear la figura y los ejes de la gráfica
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))

    # Gráfica de barras para los conteos de plataforma
        ax[0].bar(plataforma_counts.index, plataforma_counts.values)
        ax[0].set_title('Conteos de Plataforma')
        ax[0].set_xlabel('Plataforma')
        ax[0].set_ylabel('Conteo')

    # Gráfica de barras para los conteos de género
        ax[1].bar(genero_counts.index, genero_counts.values)
        ax[1].set_title('Conteos de Género')
        ax[1].set_xlabel('Género')
        ax[1].set_ylabel('Conteo')

    # Ajustar el espaciado entre las subgráficas
        plt.tight_layout()

    # Guardar la gráfica en un archivo (opcional)
    # plt.savefig('grafica.png')

    # Convertir la gráfica en una imagen y mostrarla en el template
    
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        return render_template("resultados.html", dic=data, image_png=image_png.decode('utf-8'))
    
    print(data)
    return render_template("resultados.html", dic = data)
    
    
    
if __name__ == '__main__':   
    app.run(threaded= True, debug = True) 
    




