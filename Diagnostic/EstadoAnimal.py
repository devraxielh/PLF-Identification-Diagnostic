# Librerías requeridas
import numpy as np
from matplotlib import pyplot as plt
from fuzzy import *
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# funciones de pertenencia de entrada y universo de discurso
#
# Edad [0,30] en meses
# diferencial [0,100] unidad
# pf = peso final
# pi = peso inicial
# ganancia en 30 dias
# dif = pf - pi/GA

# funciones de pertenencia de salida y universo de discurso
# Estado animal [0,1] probabilidad
#(enfermo,estable)


###################################################

# funciones de pertenencia para la variable Edad
e = np.linspace(1,30)
ternero = trapmf(e, [1, 1, 16, 20])
novillo = trimf(e, [16, 22, 28])
adulto = trapmf(e, [26, 28, 30, 30])

# funciones de pertenencia para la variable dif

d = np.linspace(0,100)
bajo = trapmf(d, [0, 0, 15, 40])
medio = trimf(d, [35, 52.5, 70])
alto = trapmf(d, [65, 80, 100, 100])

# graficos Edad
"""plt.plot(e, ternero, label="TER")
plt.plot(e, novillo, label="NOV")
plt.plot(e, adulto, label="ADUL")
plt.legend(loc='best')
plt.xlabel('Edad')
plt.ylabel('F(x)')
plt.show()

# grafios dif
plt.plot(d, bajo, label="BAJO")
plt.plot(d, medio, label="MEDIO")
plt.plot(d, alto, label="ALTO")
plt.legend(loc='best')
plt.xlabel('DIFERENCIAL')
plt.ylabel('F(x)')
plt.show()"""


##### Difuzzificacion
# tomamos una una edad cualquiera por ejemplo 18 para la edad
# 
#

edad_input = 18
valor_ternero = trapmf(edad_input, [1, 1, 16, 20])
valor_novillo = trimf(edad_input, [16, 22, 28])
valor_adulto = trapmf(edad_input, [26, 28, 30, 30])

print('valor_ternero = ',valor_ternero)
print('valor_novillo = ',valor_novillo)
print('valor_adulto  = ',valor_adulto)

plt.plot(e, ternero, label="TER")
plt.plot(e, novillo, label="NOV")
plt.plot(e, adulto, label="ADUL")
plt.legend(loc='best')


plt.plot([edad_input, edad_input], [0.0, 1.0], linestyle="--")
plt.plot(edad_input, valor_ternero, 'x')
plt.plot(edad_input, valor_novillo, 'x')
plt.plot(edad_input, valor_adulto, 'x')
plt.xlabel('Edad')
plt.ylabel('F(x)')
plt.show()


# Inferencia
# Se calculan las funciones cortadas



print('END')
