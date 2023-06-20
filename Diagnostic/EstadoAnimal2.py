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



edad = ctrl.Antecedent(np.arange(0, 11, 1), 'edad')
dif = ctrl.Antecedent(np.arange(0, 11, 1), 'dif')
estadoAnimal = ctrl.Consequent(np.arange(0, 26, 1), 'estado')
print(edad)
print(dif)
print(estadoAnimal)
# Auto-membership function population is possible with .automf(3, 5, or 7)
edad['ternero'] = fuzz.trapmf(edad.universe, [1, 1, 16, 20])
edad['novillo'] = fuzz.trimf(edad.universe, [16, 22, 28])
edad['adulto'] = fuzz.trapmf(edad.universe, [26, 28, 30, 30])

dif['bajo'] = fuzz.trapmf(dif.universe, [0, 0, 15, 40])
dif['medio'] = fuzz.trimf(dif.universe, [35, 52.5, 70])
dif['alto'] = fuzz.trapmf(dif.universe, [65, 80, 100, 100])

estadoAnimal['enfermo'] = fuzz.trimf(estadoAnimal.universe, [0, 0, 60])
estadoAnimal['estable'] = fuzz.trimf(estadoAnimal.universe, [40, 40, 100])

# para ver las graficas

#edad.view()
#dif.view()
#estadoAnimal.view()


# Creamos las reglas difusas
rule1 = ctrl.Rule(edad['ternero'] & dif['bajo'], estadoAnimal['enfermo'])
rule2 = ctrl.Rule(edad['ternero'] & dif['medio'], estadoAnimal['estable'])
rule3 = ctrl.Rule(edad['novillo'] & dif['medio'], estadoAnimal['enfermo'])
rule4 = ctrl.Rule(edad['novillo'] & dif['alto'], estadoAnimal['estable'])
rule5 = ctrl.Rule(edad['adulto'] & dif['medio'], estadoAnimal['estable'])
rule6 = ctrl.Rule(edad['adulto'] & dif['alto'], estadoAnimal['estable'])
rule7 = ctrl.Rule(edad['novillo'] & dif['bajo'], estadoAnimal['enfermo'])
rule8 = ctrl.Rule(edad['adulto'] & dif['bajo'], estadoAnimal['enfermo'])
rule9 = ctrl.Rule(edad['ternero'] & dif['alto'], estadoAnimal['estable'])

# control 
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,rule5,rule6,rule7,rule8,rule9])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

# generamos una muestra

tipping.input['edad'] = 18
tipping.input['dif'] = 90

# Crunch the numbers
tipping.compute()

print (tipping.output['estado'])
estadoAnimal.view(sim=tipping)

