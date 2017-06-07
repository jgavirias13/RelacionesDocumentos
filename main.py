from __future__ import division
import argparse
from pathlib import Path
from nltk.corpus import stopwords
from nltk.stem.snowball import EnglishStemmer
from string import punctuation
import unicodedata
import math
import numpy as np
import json

stemmer = EnglishStemmer()

#Tomado de https://es.stackoverflow.com/questions/24278/c%C3%B3mo-listar-todos-los-archivos-de-una-carpeta-usando-python
#Creada por el usuario Mariano de Stackoverflow
#La funcion lista todos los archivos de una carpeta y los retorna en una lista
def ls(ruta):
    return [arch.name for arch in Path(ruta).iterdir() if arch.is_file()]


#Funcion para crear la ruta completa a un archivo
def ruta_completa(ruta, nombreArchivo):
    if(not ruta.endswith('/')):
        strRuta = ruta + '/' + nombreArchivo
    else:
        strRuta = ruta + nombreArchivo
    return strRuta


#Tomado de http://www.leccionespracticas.com/uncategorized/eliminar-tildes-con-python-solucionado
#Funcion para eliminar las tildes de una palabra
def eliminar_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


#Funcion para limpiar una palabra de signos de puntuacion y mayusculas
def limpiar_palabra(word):
    palabraLimpia = word.lower() #Se pasa la palabra a minuscuals
    palabraLimpia = palabraLimpia.strip() #Se quitan los \n y \t
    palabraLimpia = eliminar_tildes(palabraLimpia) #Se deben quitar las tildes de las palabras por la libreria usada
    for p in list(punctuation):
        palabraLimpia = palabraLimpia.replace(p,'') #Se limpia de todos los signos de puntuacion
    return palabraLimpia


#Funcion para determinar el numero de veces que aparece una palabra en un documento.
def frecuencia_termino(documento):
    frec_term = {}
    for linea in documento:
        palabras = linea.split(" ")
        for palabra in palabras:
            palabraLimpia = limpiar_palabra(palabra.decode('utf-8'))
            palabraLimpia = stemmer.stem(palabraLimpia) #Se sacan las raices de las palabras
            if palabraLimpia not in frec_term:
                if palabraLimpia not in stopwords.words('english'): #Se eliminan las stopwords
                    frec_term[palabraLimpia] = 1
            else:
                frec_term[palabraLimpia] += 1
    return frec_term


#Funcion para sacar el coeficiente de jaccard
def jaccard(tf1, tf2):
    ta = np.array(tf1.values())
    tb = np.array(tf2.values())
    magnitud_ta = np.linalg.norm(ta)
    magnitud_tb = np.linalg.norm(tb)
    ppunto = np.dot(ta,tb)
    jaccard_cof = ppunto/((magnitud_ta**2 + magnitud_tb**2)- ppunto)
    return jaccard_cof

#Funcion para sacar el top de las relaciones entre documentos
def top(matriz_correlacion, cantidad_documentos, lista_documentos):
    top_dic = {}
    i = j = 0
    for nombre_Documento in lista_documentos:
        lista_tuplas = []
        j = 0
        while j < cantidad_documentos:
            if(i == j):
                j += 1
                continue
            else:
                lista_tuplas.append((matriz_correlacion[i][j],j))
                j +=1
        lista_tuplas = sorted(lista_tuplas, reverse=True)
        documentos_relacionados = []
        for tupla in lista_tuplas:
            documentos_relacionados.append(lista_documentos[tupla[1]])
        top_dic[nombre_Documento] = documentos_relacionados
        i += 1
    return json.dumps(top_dic, indent=4)


def main():
    #Se define el parser para tomar parametros por terminal
    parser = argparse.ArgumentParser(description='Programa para hacer relaciones entre documentos '
                                                'y sacar un listado de los mas cercanos a cada uno')
    parser.add_argument('PATH', help='Carpeta de donde se tomaran todos los documentos')
    argumentos = parser.parse_args()
    if argumentos.PATH:
        listaArchivos = ls(argumentos.PATH) #Tomar todos los archivos de la carpeta
        cantidadDocumentos = len(listaArchivos) #Cantidad de archivos en la carpeta
        vectores_tf = {} #Vector que guarda los vectores de frecuencia termino de los documentos
        vector_terminos = {} #Vector que guarda todas las palabras y la cantidad de documentos en los que aparece
        for nombreArchivo in listaArchivos:
            ruta = ruta_completa(argumentos.PATH, nombreArchivo) #Tomar la ruta a cada archivo
            documento = open(ruta, 'r') #Abrir el archivo
            vectores_tf[nombreArchivo] = frecuencia_termino(documento) #Se saca el vector tf de cada documento
            for palabra in vectores_tf[nombreArchivo]: #Se recorre las palabras del documento para construir vt
                if palabra not in vector_terminos: #Se aumenta la frecuencia de la palabra
                    vector_terminos[palabra] = 1
                else:
                    vector_terminos[palabra] += 1
        vectores_tfidf = {} #Vector que guarda los vectores tfidf de cada documento
        for documento in listaArchivos: #Se saca el vector tfidf de cada documento
            vector_tfidf = {} #Vector tfidf del documento
            for palabra in vector_terminos: #tfidf de cada palabra
                if palabra not in vectores_tf[documento]:
                    vector_tfidf[palabra] = 0
                else: #Aplicacion de la formula de tfidf mostrada en el documento
                    vector_tfidf[palabra] = vectores_tf[documento][palabra]*math.log(cantidadDocumentos/vector_terminos[palabra])
            vectores_tfidf[documento] = vector_tfidf
        correlacion = np.zeros(shape=(cantidadDocumentos, cantidadDocumentos))
        i = 0
        while i < cantidadDocumentos:
            j = i
            while j < cantidadDocumentos:
                correlacion[i][j] = jaccard(vectores_tfidf[listaArchivos[i]], vectores_tfidf[listaArchivos[j]])
                correlacion[j][i] = correlacion[i][j]
                j+=1
            i+=1
        #print correlacion
        #print listaArchivos
        #print vector_terminos
        archivoSalida = open('Resultados.json', 'w')
        archivoSalida.write(top(correlacion,cantidadDocumentos,listaArchivos))
        archivoSalida.close()




if __name__ == '__main__':
    main()
