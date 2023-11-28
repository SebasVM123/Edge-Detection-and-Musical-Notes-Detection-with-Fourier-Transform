# Edge-Detection-and-Musical-Notes-Detection-with-Fourier-Transform
Este es un proyecto que explora dos áreas fundamentales del procesamiento de señales: la detección de bordes en imágenes mediante la convolución y la identificación de notas musicales utilizando la transformada de Fourier.

## Descripción
El proyecto se enfoca en dos tareas principales:

### Detección de Bordes
Utilizando técnicas de convolución, el programa identifica los bordes en imágenes. Se exploran operadores de gradiente como Sobel y Prewitt, así como otros métodos como la diferencia de Gaussianas y operadores laplacianos.
![imagen](https://github.com/SebasVM123/Edge-Detection-and-Musical-Notes-Detection-with-Fourier-Transform/assets/42723025/5c182af1-1984-4d50-b53d-b8b32ef57ecf)

### Identificación de Notas Musicales
Se aplica la Transformada Rápida de Fourier (FFT) a señales de audio para analizar su contenido de frecuencia. A partir del espectro de frecuencia resultante, se determina la frecuencia dominante para identificar la nota musical correspondiente.
![imagen](https://github.com/SebasVM123/Edge-Detection-and-Musical-Notes-Detection-with-Fourier-Transform/assets/42723025/57d21696-71e7-4953-95bd-3d6fb1c0f232)

## Tecnologías Utilizadas
* Python para el procesamiento de imágenes y señales de audio con el Framework Django 4.2.7
* HTML 5
* CSS 3

### Dependencias
Se usan las siguientes librerías y paquetes externos.
* Django
* opencv-python
* scipy
* matplotlib
* numpy

## Instrucciones de Uso
Instala los requisitos del proyecto:
`pip install -r requirements.txt`

Corre el servidor:
`python FourierImageEdgeDetection/manage.py runserver`

## Créditos
Este proyecto fue creado por Sebastián Velásquez Múnera y Julián Esteban Collazos.

## Licencia
Este proyecto está bajo la licencia MIT License.
