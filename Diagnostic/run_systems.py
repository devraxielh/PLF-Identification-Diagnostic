from os import system
import sys


print('---\tRendimiento del Potrero')
e = system('python3 rendimiento_potrero.py')
if e == 0:
    print('---\tClasificador difuso')
    system('python3 fuzzy_classificador.py')
    system('python3 metricas.py')
    print('---\tAlgoritmo Estado Animal')
    system('python3 EstadoAnimal_GA.py')
    print('---\tStart end predict')
    system('python3 end_predict.py')
 
 ## Sistema Automatico de los distintos scripts del sistema 