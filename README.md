# Practica Computación de alto rendimiento

## Integrantes:
* Juan Pablo Gaviria
* David Alejandro Gomez
* Felipe Montoya

## Manual de usuario

Esta practica tiene como objetivo realizar, por cada documento de un conjunto de documentos, una lista de los documentos más relacionados con este. La explicación del funcionamiento de los algoritmos se encuentra en el archivo Reporte Tecnico.pdf.

### Ejecución del programa serial
Para ejecutar el programa serial descargue el repositorio en formato zip y descomprimalo. En una terminal ubiquese en la carpeta donde quedo el repositorio y ejecute
  `cd RelacionesDocumentos`
Una vez este ubicado en la carpeta del programa ejecute con la siguiente sintaxis:
  `python main.py [-h] PATH`
  Donde la opción -h devuelve la ayuda para la ejecución del programa y el parametro PATH indica la carpeta donde estan ubicados los documentos
  El programa ejecutara y creara un archivo JSON con la lista por cada documento de los documentos más relacionados.
  
### Ejecución del programa paralelo
Para ejecutar el programa paralelo descargue el repositorio en formato zip y descomprimalo. En una terminal ubiquese en la carpeta donde quedo el repositorio y ejecute
  `cd RelacionesDocumentos`
Una vez este ubicado en la carpeta del programa ejecute con la siguiente sintaxis:
  `mpiexec -np NCORES python ./main_paralelo.py [-h] PATH`
  Donde la opción -h devuelve la ayuda para la ejecución del programa, el parametro PATH indica la carpeta donde estan ubicados los documentos y el parametro NCORES el número de cores en el que se ejecutará

