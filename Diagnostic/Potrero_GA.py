import random
from matplotlib import pyplot as plt
import numpy as np
from random import randint
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
from utils import *


def read_df():
    df = pd.read_csv('potrero.csv',keep_default_na=False,dtype=int)
    print('Cargando Datos: ',len(df))
    return df



def fuzzy_control(genes,df):
    Dpasto = list_pasto(df)
    Dsuelo = list_suelo(df)
    interpretacion_array = []
    
    pasto = ctrl.Antecedent(np.arange(0, 12, 1), 'pasto')
    suelo = ctrl.Antecedent(np.arange(0, 12, 1), 'suelo')
    potrero = ctrl.Consequent(np.arange(0, 100, 1), 'potrero')
    
    mean_pointPt = (genes[3] - genes[0])/2
    mean_pointPt = genes[3]-mean_pointPt
    mean_pointS = (genes[7] - genes[4])/2
    mean_pointS = genes[7] - mean_pointS    
    mean_pointPr = (genes[11] - genes[8])/2
    mean_pointPr = genes[11] - mean_pointPr
    
    pasto['malo'] = fuzz.trimf(pasto.universe, [0, 0, genes[1]])
    pasto['regular'] = fuzz.trimf(pasto.universe, [genes[0], mean_pointPt, genes[3]])
    pasto['bueno'] = fuzz.trimf(pasto.universe, [genes[2], 10, 10])

    suelo['malo'] = fuzz.trapmf(suelo.universe, [0, 0, 0, genes[5]])
    suelo['regular'] = fuzz.trimf(suelo.universe, [genes[4], mean_pointS, genes[7]])
    suelo['bueno'] = fuzz.trapmf(suelo.universe, [genes[6], 10, 10, 10])

    potrero['malo'] = fuzz.trimf(potrero.universe, [0, 0,genes[9]])
    potrero['regular'] = fuzz.trimf(potrero.universe, [genes[8], mean_pointPr, genes[11]])
    potrero['bueno'] = fuzz.trimf(potrero.universe, [genes[10], 100, 100])
    
    #### Reglas difusas
    rule1 = ctrl.Rule(pasto['malo'] & suelo['malo'], potrero['malo'])
    rule2 = ctrl.Rule(pasto['malo'] & suelo['regular'], potrero['malo'])
    rule3 = ctrl.Rule(pasto['malo'] & suelo['bueno'], potrero['regular'])
    rule4 = ctrl.Rule(pasto['regular'] & suelo['malo'], potrero['malo'])
    rule5 = ctrl.Rule(pasto['regular'] & suelo['regular'], potrero['regular'])
    rule6 = ctrl.Rule(pasto['regular'] & suelo['bueno'], potrero['bueno'])
    rule7 = ctrl.Rule(pasto['bueno'] & suelo['malo'], potrero['malo'])
    rule8 = ctrl.Rule(pasto['bueno'] & suelo['regular'], potrero['bueno'])
    rule9 = ctrl.Rule(pasto['bueno'] & suelo['bueno'], potrero['bueno'])

    # Simulacion del controlador difuso
    # control 
    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4,rule5,rule6,rule7,rule8,rule9])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl) 
    
    # generamos una muestra
    #print(genes)
    for i in range(0,len(df)):
        #print('i',i)
        tipping.input['pasto'] = Dpasto[i]
        tipping.input['suelo'] = Dsuelo[i]



        # Crunch the numbers
        try:
            tipping.compute()
        except:
            tam = len(df)
            for i in range(0,tam):
                interpretacion_array.append(0)
            return interpretacion_array    
        #print(tipping)
        #print('-------------------------------------')
        #print(tipping.output['estado'])
        result = tipping.output['potrero']
        imalo = fuzz.interp_membership(potrero.universe, potrero['malo'].mf,result)
        iregular = fuzz.interp_membership(potrero.universe, potrero['regular'].mf,result)
        ibueno = fuzz.interp_membership(potrero.universe, potrero['bueno'].mf,result)
        if float(imalo) > float(iregular) and float(imalo) > float(ibueno):
            interpretacion_array.append(-1)
        elif float(iregular) > float(imalo) and float(iregular) > float(ibueno):
            interpretacion_array.append(0)
        elif float(ibueno) > float(imalo) and float(ibueno) > float(iregular):
            interpretacion_array.append(1)

    return interpretacion_array

def individuo(num_vertices):
    #global genes
    genes = []
    cant = []
    delta_list = [2,2,20]
    min_max = [[0,10],[0,10],[40,100]]
    vertice_inicial = [[3,4,6,8],[3,4,6,8],[40,50,75,90]]
    """
        Crea un individuo
    """
    tam = len(vertice_inicial)
    for i in range(tam):
        pos = vertice_inicial[i]
        cant.append(len(pos))
    genes.clear()   
    #print(cant)
    for i in range(num_vertices):
            #print(i)
            if i < cant[0]:
                if i == 0:
                    genes.append(randint(min_max[0][0], vertice_inicial[0][1]-delta_list[0]//2))
                elif i < (cant[0]-1) and i != 0:
                    genes.append(randint(vertice_inicial[0][i]-delta_list[0]//2, vertice_inicial[0][i+1]-delta_list[0]//2))
                elif i == 3:
                    genes.append(randint(vertice_inicial[0][i]-delta_list[0]//2, min_max[0][1]))
            if (i < cant[1]+cant[0]) and i >= cant[0]:
                j = i- cant[0]
                if i == 4:
                    genes.append(randint(min_max[1][0], vertice_inicial[1][1]-delta_list[1]//2))
                elif i < (cant[0]+cant[1]-1) and i != 4:
                    genes.append(randint(vertice_inicial[1][j]-delta_list[1]//2, vertice_inicial[1][j+1]-delta_list[1]//2))
                elif i == 7:
                    genes.append(randint(vertice_inicial[1][j]-delta_list[1]//2, min_max[1][1])) 
                    
            if (i < cant[2]+cant[0]+cant[1]) and i >= cant[0]+cant[1]:
                j = i - cant[0]-cant[1]
                if i == 8:
                    genes.append(randint(min_max[2][0], vertice_inicial[2][1]-delta_list[2]//2))
                elif i < (num_vertices-1) and i != 8:
                    genes.append(randint(vertice_inicial[2][j]-delta_list[2]//2, vertice_inicial[2][j+1]-delta_list[2]//2))
                elif i == num_vertices-1:
                    genes.append(randint(vertice_inicial[2][j]-delta_list[2]//2, min_max[2][1]))                     
                    
    return genes

def crearPoblacion(num):
    return [individuo(12) for i in range(num)]                    

def get_fitness(genes,df):
    global array_p
    n = fuzzy_control(genes,df)
    score = 0
    #print(str(n)+' '+str(array_p))
    for j in range(len(n)):
        if n[j] == array_p[j]:
            score = score + 1
    return float(score)/len(df)

def fitness(poblacion,df):
    #print('tam poblacion fitness: ',len(poblacion))
    array_p = df['prediccion'].to_list()
    score = 0
    for i in range(0,len(poblacion)):
        interpret_fuzzy = fuzzy_control(poblacion[i],df)
        getfit = get_fitness(poblacion[i],df)
        #print('fit: '+str(getfit)+ ' ' + str(interpret_fuzzy)+' '+str(array_p)+' '+ str(poblacion[i]))
        print('Cromosoma: '+str(poblacion[i]))
        #print('tam poblacion fitness: ',len(poblacion))
        score = 0
        for j in range(0,len(interpret_fuzzy)):
            #print(str(interpret_fuzzy[j])+'======='+str(array_p[j]))
            
            if interpret_fuzzy[j] == array_p[j]:
                score += 1
        if float(score)/float(len(interpret_fuzzy))==1.0:
            return float(score)/float(len(interpret_fuzzy)),poblacion[i] 
            
    return float(score)/float(len(interpret_fuzzy)),poblacion[i]         

def cross(father,mother):
    #print('father',father)
    #print('mother',mother)
    # tres cortes por las funcione de pertenectia
    #children1 = mother[:3]+father[2:]
    #children2 = father[:3]+mother[2:]
    children1 = mother[:2]+father[2:]
    children2 = father[:2]+mother[2:]
    

    #children1 = mother[:4]+father[4:6]+mother[6:]
    #children2 = father[:4]+mother[4:6]+father[6:] 
    
    #children1 = mother[:8]+father[8:]
    #children2 = father[:8]+mother[8:]    
    #print('children1',children1)
    #print('children2',children2)
    return children1,children2


def mutate(genes):
    gen = randint(0,9)
    #print('gen :',gen)
    #print(genes)
    if gen == 0:
        mutate = randint(genes[gen],genes[gen+1])
        #print(mutate)
        #print(genes)
        genes[gen] = mutate
    if gen == 1:
        mutate = randint(genes[gen],genes[gen+1])
        genes[gen] = mutate
        #print(mutate)
        #print(genes)
    if gen == 2:
        mutate = randint(genes[gen],genes[gen+1])
        genes[gen] = mutate
        #print(mutate)
        #print(genes)
        #if gen == 3:
        #mutate = randint(genes[gen],genes[gen]-1)
        #genes[gen] = mutate 
    if gen == 4:
        mutate = randint(genes[gen],genes[gen+1])
        genes[gen] = mutate
        #print(mutate)
        #print(genes)    
    if gen == 5:
        mutate = randint(genes[gen],genes[gen+1])
        genes[gen] = mutate 
        #print(mutate)
        #print(genes)    
    if gen == 6:
        mutate = randint(genes[gen],genes[gen+1])
        genes[gen] = mutate 
        #print(mutate)
        #print(genes)        
    if gen == 7:
        mutate = randint(genes[gen],genes[gen])
        genes[gen] = mutate
    if gen == 8:
        mutate = randint(genes[gen],genes[gen+1])
        genes[gen] = mutate  
        #print(mutate)
        #print(genes)        
    if gen == 9:
        mutate = randint(genes[gen],genes[gen])
        genes[gen] = mutate         
        
        
        
    return genes  


def selectMembersGeneration(poblacion,df):
    global array_p
    parents = []
    parents2 = []
    #parents.clear()
    score = 0
    for i in range(0, len(poblacion)):
        score = get_fitness(poblacion[i],df)
        
        if score >= 0.9:
            parents2.append(poblacion[i])


        if score >= 0.7 and len(parents2)< 2:
            parents.append(poblacion[i])

    if len(parents2) >= 2:
        return parents2  
    
    elif len(parents2) > 0 and len(parents) < 2:
        return parents2
    
    elif len(parents2) < 2 and len(parents) > 1:
        return parents
    elif len(parents) == 0 and len(parents2) == 0:
        return parents  

def reproductionMembersGeneration(parents):
    global df
    #print('reproduccion Parents: ',parents)
    totalParents = len(parents)
    corte = totalParents//2
    nueva_poblacion = []
    nueva_poblacion2 = []

    for i in range(0, corte):
        father = parents[i*2]
        mother = parents[(i*2)+1]
        children1,children2 = cross(father,mother)
        children1 = mutate(children1)

        nueva_poblacion.append(children1)
        nueva_poblacion2.append(children2)
        nueva_poblacion = nueva_poblacion + nueva_poblacion2

    nueva_poblacion = nueva_poblacion[:len(df)]

    return nueva_poblacion  

if __name__ == '__main__':
    df = read_df()
    array_p = df['prediccion'].to_list()
    people = crearPoblacion(len(df))
    print('tam_of_people: ',len(people))

    j = 0

    while True:
        print('Generacion: ',j)
        #print(people)
        score,genes = fitness(people,df)
        #print('score: '+ str(score))

        
        if score == 1.0:# or j == 20:
            #print('Optimo')
            print('Generacion: ',j)
            #print(genes)
            print('Cromosoma: '+ str(genes)+ ' Presicion: '+str(score*100))
            salida = genes
            #print(score*100)
            break         
        
        parents = selectMembersGeneration(people,df)
        if len(parents) > 1:
            people = reproductionMembersGeneration(parents)
        else:
            aux = []
            for i in range(len(people)):
                o = get_fitness(people[i],df)
                aux.append([o,people[i]])
                aux.sort(reverse=True)
            print('Generacion: ',j)
            print('Cromosoma: '+ str(aux[0][1])+ ' Presicion: '+str(o*100))
            
            salida = aux[0][1]
            break
        j = j + 1
    out = pd.DataFrame(salida,columns=['genes'])
    out.to_csv('./fuzzy/potrero.csv',index=0)            