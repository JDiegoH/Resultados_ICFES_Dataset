import re
from flask import Flask, request, render_template

import pandas as pd
import matplotlib.pyplot as plt
import base64
import io

from PIL import Image, ImageOps

from pandas.core import base

app = Flask(__name__)
@app.route('/cargador',methods=['POST','GET']) #el link de la app
def cargador():
    if request.method == 'GET': # IF no hay archivo seleccionado
        return render_template('Carga.html') #Muestra la página para seleccionar archivo
    else:
        archivo = request.files['file'] #Obtiene y guarda el archivo
        archivo.save(archivo.filename)

        df = pd.read_csv(archivo.filename) #Lee el archivo

        #Agrupamiento de datos/tabla

        puntaje_departamento = df.groupby(['ESTU_DEPTO_RESIDE'])['PUNT_GLOBAL'].median().reset_index()

        conteo_departamento = df.groupby(['ESTU_DEPTO_RESIDE'])['PUNT_GLOBAL'].count().reset_index()

        puntaje_competencias = df.groupby(['ESTU_DEPTO_RESIDE'])['PUNT_LECTURA_CRITICA','PUNT_MATEMATICAS','PUNT_C_NATURALES','PUNT_SOCIALES_CIUDADANAS','PUNT_INGLES'].median().reset_index()

        #Puntajes Máximos

        puntaje_maximo = df.groupby(['ESTU_DEPTO_RESIDE'])['PUNT_GLOBAL'].max().reset_index()

        puntaje_maximo_bogota = puntaje_maximo[(puntaje_maximo.ESTU_DEPTO_RESIDE == 'BOGOTÁ')].reset_index(drop = True)

        puntaje_maximo_bogota = puntaje_maximo_bogota['PUNT_GLOBAL']

        puntaje_maximo_antioquia = puntaje_maximo[(puntaje_maximo.ESTU_DEPTO_RESIDE == 'ANTIOQUIA')].reset_index(drop = True)

        puntaje_maximo_antioquia = puntaje_maximo_antioquia['PUNT_GLOBAL']

        puntaje_maximo_bolivar = puntaje_maximo[(puntaje_maximo.ESTU_DEPTO_RESIDE == 'BOLIVAR')].reset_index(drop = True)

        puntaje_maximo_bolivar = puntaje_maximo_bolivar['PUNT_GLOBAL']

        puntaje_maximo_meta = puntaje_maximo[(puntaje_maximo.ESTU_DEPTO_RESIDE == 'META')].reset_index(drop = True)

        puntaje_maximo_meta = puntaje_maximo_meta['PUNT_GLOBAL']

        puntaje_maximo_boyaca = puntaje_maximo[(puntaje_maximo.ESTU_DEPTO_RESIDE == 'BOYACA')].reset_index(drop = True)

        puntaje_maximo_boyaca = puntaje_maximo_boyaca['PUNT_GLOBAL']

        #Puntajes Mínimos

        puntaje_minimo = df.groupby(['ESTU_DEPTO_RESIDE'])['PUNT_GLOBAL'].min().reset_index()

        puntaje_minimo = puntaje_minimo[(puntaje_minimo.PUNT_GLOBAL <= 30)]

        puntaje_minimo_antioquia = puntaje_minimo[(puntaje_minimo.ESTU_DEPTO_RESIDE == 'ANTIOQUIA')].reset_index(drop = True)

        puntaje_minimo_antioquia = puntaje_minimo_antioquia['PUNT_GLOBAL']

        puntaje_minimo_arauca = puntaje_minimo[(puntaje_minimo.ESTU_DEPTO_RESIDE == 'ARAUCA')].reset_index(drop = True)

        puntaje_minimo_arauca = puntaje_minimo_arauca['PUNT_GLOBAL']

        puntaje_minimo_cauca = puntaje_minimo[(puntaje_minimo.ESTU_DEPTO_RESIDE == 'CAUCA')].reset_index(drop = True)

        puntaje_minimo_cauca = puntaje_minimo_cauca['PUNT_GLOBAL']

        puntaje_minimo_guajira = puntaje_minimo[(puntaje_minimo.ESTU_DEPTO_RESIDE == 'LA GUAJIRA')].reset_index(drop = True)

        puntaje_minimo_guajira = puntaje_minimo_guajira['PUNT_GLOBAL']

        puntaje_minimo_valle = puntaje_minimo[(puntaje_minimo.ESTU_DEPTO_RESIDE == 'VALLE')].reset_index(drop = True)

        puntaje_minimo_valle = puntaje_minimo_valle['PUNT_GLOBAL']

        

        #Puntaje género

        conteo_genero = df.groupby(['ESTU_GENERO'])['PUNT_GLOBAL'].count().reset_index()

        cant_mujeres = conteo_genero[(conteo_genero['ESTU_GENERO'] == 'F')].reset_index(drop = True)

        cant_mujeres = cant_mujeres['PUNT_GLOBAL']

        cant_hombres = conteo_genero[(conteo_genero['ESTU_GENERO'] == 'M')].reset_index(drop = True)

        cant_hombres = cant_hombres['PUNT_GLOBAL']

        puntaje_genero = df.groupby(['ESTU_GENERO'])['PUNT_GLOBAL'].median().reset_index()

        punt_mujeres = puntaje_genero[(puntaje_genero['ESTU_GENERO'] == 'F')].reset_index(drop = True)

        punt_mujeres = punt_mujeres['PUNT_GLOBAL']

        punt_hombres = puntaje_genero[(puntaje_genero['ESTU_GENERO'] == 'M')].reset_index(drop = True)

        punt_hombres = punt_hombres['PUNT_GLOBAL']



        puntaje_estrato = df.groupby(['FAMI_ESTRATOVIVIENDA'])['PUNT_GLOBAL'].median().reset_index()

        puntaje_estrato = puntaje_estrato[(puntaje_estrato.FAMI_ESTRATOVIVIENDA != '-')]

        puntaje_dedicacion_lectura = df.groupby(['ESTU_DEDICACIONLECTURADIARIA'])['PUNT_LECTURA_CRITICA'].median().reset_index()

        puntaje_dedicacion_lectura = puntaje_dedicacion_lectura[(puntaje_dedicacion_lectura.ESTU_DEDICACIONLECTURADIARIA != '-')]

        puntaje_jornada = df.groupby(['COLE_JORNADA'])['PUNT_GLOBAL'].median().reset_index()

        puntaje_internet = df.groupby(['FAMI_TIENEINTERNET'])['PUNT_GLOBAL'].median().reset_index()

        puntaje_internet = puntaje_internet[(puntaje_internet.FAMI_TIENEINTERNET != '-')]

        puntaje_bilingue = df.groupby(['COLE_BILINGUE'])['PUNT_INGLES'].median().reset_index()

        puntaje_bilingue = puntaje_bilingue[(puntaje_bilingue.COLE_BILINGUE != '-')]

        #Gráfico

        #Puntaje total

        puntaje_departamento.plot(figsize = (15,15),
                title = "PUNTAJE TOTAL POR DEPARTAMENTOS",
                kind = 'bar',
                x = 'ESTU_DEPTO_RESIDE'
                ,color = "mediumpurple"
        )

        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plot_url1 = base64.b64encode(img.getvalue()).decode()

        #Conteo por departamento

        conteo_departamento.plot(figsize = (14,7),
                title = "CANTIDAD ESTUDIANTES POR DEPARTAMENTOS",
                kind = 'barh',   
                x = 'ESTU_DEPTO_RESIDE'
        )

        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plot_url0 = base64.b64encode(img.getvalue()).decode()

        #Puntaje competencias

        puntaje_competencias.plot(figsize = (15,15),
                title = "PUNTAJE DE LAS COMPETENCIAS POR DEPARTAMENTOS",
                kind = 'bar',
                x = 'ESTU_DEPTO_RESIDE',
                stacked = True
        )

        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plot_url2 = base64.b64encode(img.getvalue()).decode()

        #Puntaje total por estratos

        puntaje_estrato.plot(figsize = (7,7),
                title = "PUNTAJE TOTAL POR ESTRATOS",
                kind = 'barh',
                x = 'FAMI_ESTRATOVIVIENDA'
                ,color = "yellowgreen"
        )

        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plot_url5 = base64.b64encode(img.getvalue()).decode()

        #Puntaje segun cantidad de lectura

        puntaje_dedicacion_lectura.plot(figsize = (18,9),
                title = "PUNTAJE LECTURA CRÍTICA POR DEDICACIÓN A LA LECTURA",
                kind = 'barh',
                x = 'ESTU_DEDICACIONLECTURADIARIA'
                ,color = "darksalmon"
        )

        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plot_url7 = base64.b64encode(img.getvalue()).decode()

        #Puntaje total por jornada


        puntaje_jornada.plot(figsize = (7,7),
                title = "PUNTAJE TOTAL POR JORNADA ACADÉMICA",
                kind = 'pie',
                x = 'COLE_JORNADA',
                y = 'PUNT_GLOBAL',
                autopct = "%.2f",
                labels = ["COMPLETA","MAÑANA","NOCHE","SABATICA","TARDE","ÚNICA"]
        )

        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plot_url8 = base64.b64encode(img.getvalue()).decode()

        #Puntaje total por estudiantes que tienen o no tienen internet

        puntaje_internet.plot(figsize = (7,7),
                title = "PUNTAJE TOTAL POR ESTUDIANTES QUE TENGAN Y NO TENGAN INTERNET",
                kind = 'bar',
                x = 'FAMI_TIENEINTERNET'
                ,color = "orange"
        )

        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plot_url9 = base64.b64encode(img.getvalue()).decode()

        #Puntaje ingles por colegio bilingüe

        puntaje_bilingue.plot(figsize = (7,7),
                title = "PUNTAJE INGLÉS POR ESTUDIANTES QUE ESTUDIAN O NO EN COLEGIO BILINGÜE",
                kind = 'bar',
                x = 'COLE_BILINGUE'
                ,color = "darkgreen"
        )

        img = io.BytesIO()
        plt.savefig(img,format='png')
        img.seek(0)
        plot_url10 = base64.b64encode(img.getvalue()).decode()

        return render_template('Resultados.html',imagen_puntaje_departamento = plot_url1
                                                ,imagen_conteo_departamento = plot_url0
                                                ,imagen_puntaje_competencias = plot_url2
                                                ,imagen_puntaje_estrato = plot_url5
                                                ,tabla_puntaje_estrato = puntaje_estrato.to_html(classes='data',header=True,index=False)
                                                ,imagen_puntaje_dedicacion_lectura = plot_url7
                                                ,imagen_puntaje_jornada = plot_url8
                                                ,tabla_puntaje_jornada = puntaje_jornada.to_html(classes='data',header=True,index=False)
                                                ,imagen_puntaje_internet = plot_url9
                                                ,imagen_puntaje_bilingue = plot_url10     
                                                ,antioquia = puntaje_maximo_antioquia[0]
                                                ,bogota = puntaje_maximo_bogota[0]
                                                ,boyaca = puntaje_maximo_boyaca[0]
                                                ,bolivar = puntaje_maximo_bolivar[0]
                                                ,meta = puntaje_maximo_meta[0]
                                                ,m_antioquia = puntaje_minimo_antioquia[0]
                                                ,arauca = puntaje_minimo_arauca[0]
                                                ,cauca = puntaje_minimo_cauca[0]
                                                ,guajira = puntaje_minimo_guajira[0]
                                                ,valle = puntaje_minimo_valle[0]
                                                ,mujeres = cant_mujeres[0]
                                                ,hombres = cant_hombres[0]
                                                ,p_hombre = punt_hombres[0]
                                                ,p_mujer = punt_mujeres[0]
                                        
        ) #Muestra la página 'resultados',envia la img y tabla

if __name__ == '__main__':
    app.run()