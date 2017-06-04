import argparse
from pathlib import Path

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

#Funcion para determinar el numero de veces que aparece una palabra en un documento.
def frecuencia_termino(documento):
    frec_term = {}
    for linea in documento:
        palabras = linea.split(" ")
        for palabra in palabras:
            palabra = palabra.replace("\n", '')
            if palabra not in frec_term:
                frec_term[palabra] = 1
            else:
                frec_term[palabra] += 1
    return frec_term

def main():
    #Se define el parser para tomar parametros por terminal
    parser = argparse.ArgumentParser(description='Programa para hacer relaciones entre documentos '
                                                'y sacar un listado de los mas cercanos a cada uno')
    parser.add_argument('PATH', help='Carpeta de donde se tomaran todos los documentos')
    argumentos = parser.parse_args()
    if argumentos.PATH:
        listaArchivos = ls(argumentos.PATH) #Tomar todos los archivos de la carpeta
        for nombreArchivo in listaArchivos:
            ruta = ruta_completa(argumentos.PATH, nombreArchivo) #Tomar la ruta a cada archivo
            documento = open(ruta, 'r') #Abrir el archivo
            print frecuencia_termino(documento)
            #print documento.read() #Imprimir su contenido

if __name__ == '__main__':
    main()
