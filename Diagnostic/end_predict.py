import random
from matplotlib import pyplot as plt
import numpy as np
from random import randint
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
from tqdm import tqdm
from os import listdir
import re
import time


#def fuzzy_control_EAPO(genes)

def extract_info(look_for, text, group):
    if re.search(look_for, text):
        return re.search(look_for, text).group(group)
    else:
        return ''

def conclusion(l_estables,l_enfermos,fila_potrero):
    global df

    tam = len(df)
    tam_estables = len(l_estables)
    tam_enfermos = len(l_enfermos)
    d = 'Diagnostico'+'\n'
    p = 'Potrero {} clima: {}'.format(fila_potrero['mes'].iloc[0],fila_potrero['clima'].iloc[0]) + '\n'
    mensaje = 'Cantidad de animales estables {}, cantidad de animales enfermos {}'.format(tam_estables,tam_enfermos)
    if (tam_estables/tam) > (tam_enfermos/tam):
        mensaje2 = 'El lote de animales que tuvieron un engorde aceptable es alto, animales que esten posiblemente enfermos son: {}'.format(l_enfermos)
    elif (tam_estables/tam) <= (tam_enfermos/tam): 
        mensaje2 = 'Muchos animales no consiguieron un engorde suficiente en el potrero {} que tiene el forraje {}, sugerencia cambiar el forraje. los animales enfermos son: {} '.format(fila_potrero['mes'].iloc[0],fila_potrero['nombre'].iloc[0],l_enfermos)  

    mensaje_final = d + ' '+ p+' '+mensaje+' '+ mensaje2
    print(mensaje_final)


def fuzzy_control_animal(genes,edadd,pi,pf,GA):

    ###################################################

    edad = ctrl.Antecedent(np.arange(0, 31, 2), 'edad')
    dif = ctrl.Antecedent(np.arange(0, 101, 2), 'dif')
    estadoAnimal = ctrl.Consequent(np.arange(0, 101, 1), 'estado')

    #print(genes)
    try:
        edad['ternero'] = fuzz.trapmf(edad.universe, [0, 0, genes[0], genes[1]])
        edad['novillo'] = fuzz.trapmf(edad.universe, [genes[0], genes[1], genes[2],genes[3]])
        edad['adulto'] = fuzz.trapmf(edad.universe, [genes[2], genes[3], 30, 30])
    except:
        print('try1: ',genes)
    try:
        dif['bajo'] = fuzz.trapmf(dif.universe, [0, 0, genes[4], genes[5]])
        dif['medio'] = fuzz.trapmf(dif.universe, [genes[4], genes[5],genes[6], genes[7]])
        dif['alto'] = fuzz.trapmf(dif.universe, [genes[6], genes[7], 100, 100])
    except:
        print('try2: ',genes)
    estadoAnimal['enfermo'] = fuzz.trapmf(estadoAnimal.universe, [0,0, genes[8], genes[9]])
    estadoAnimal['estable'] = fuzz.trapmf(estadoAnimal.universe, [genes[8], genes[9],100, 100])




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
    rule10 = ctrl.Rule(edad['adulto'] & dif['alto'], estadoAnimal['enfermo'])
    # control 
    tipping_ctrl = ctrl.ControlSystem([rule9,rule10,rule4])
    #tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,rule5,rule6,rule7,rule8,rule9])#
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    # generamos una muestra

    if True:
        #print('i',i)
        dife = (float(pf) - float(pi))/11
        #dife = dife*100
        tipping.input['edad'] = float(edadd)
        tipping.input['dif'] = dife

        # Crunch the numbers

        try:
            tipping.compute()
        except:pass
        if float(dife) >= 0.5:
            return 1
        else:
            return 0         

        #print('Error compute')
        #print(tipping)
        #print('-------------------------------------')
        #print(tipping.output['estado'])
        result = tipping.output['estado']
        #print(result)
        #time.sleep(1)
        iEstable = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['estable'].mf,result)
        iEnfermo = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['enfermo'].mf,result)
        #print(str(iEstable)+'======='+str(iEnfermo))
        #time.sleep(1)
        if float(iEstable) > float(iEnfermo):
            return 1
        else:
            return 0


def process_predic(row):
    global genes

    row['predict'] = fuzzy_control_animal(genes,row['edad'],row['peso_inicial'],row['peso_final'],row['ganancia'])
    return row
    
if __name__ == '__main__':
    tqdm.pandas(ncols=100,desc='PREDICT: ')
    genesdf = pd.read_csv('./fuzzy/genes.csv')
    potrerodf = pd.read_csv('./data/potrero_predict.csv',dtype=str,keep_default_na=False)
    genes = []
    potrero = []
    for i,row in genesdf.iterrows():
        genes.append(row['genes'])
        p = row['potrero_act']
    print('Genes Estado Animal: ',genes)

    
    estable = 0
    enfermo = 0
    vector_estables = []
    vector_enfermos = []
    salida =[]
    #for file_name in sorted(listdir('./data/info')):
    #if '.csv' in file_name:
    #print('file-------> ',file_name)
    df = pd.read_csv('./data/info/muestra{}.csv'.format(int(p)),dtype=str,keep_default_na=False)
    df = df.progress_apply(lambda t: process_predic(t),axis=1)
    df.to_csv('./output/loteAnimalPredit.csv',index=0)
    for n,row in df.iterrows():
        if row['predict'] == 1:
            estable = estable + 1
            vector_estables.append(row['id_animal'])
        if row['predict'] == 0:
            enfermo = enfermo + 1
            vector_enfermos.append(row['id_animal'])
                    

    fila_potrero = potrerodf[potrerodf['mes']=='{}'.format(int(p))]
    conclusion(vector_estables,vector_enfermos,fila_potrero)
    vector_estables.clear()
    vector_enfermos.clear()


