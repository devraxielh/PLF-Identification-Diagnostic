import random
from matplotlib import pyplot as plt
import numpy as np
from random import randint
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
from utils import *
import sys


def read_potrero(n):
    potrero =  pd.read_csv('./data/potrero_predict.csv',keep_default_na=False,dtype=str)
    mini_potrero = potrero[potrero.mes == '{}'.format(n)]
    e_p = mini_potrero['estado'].iloc[0]
    points = mini_potrero['forraje'].iloc[0]
    return e_p,points
def read_df(n):
    df = pd.read_csv('./data/info/muestra{}.csv'.format(n),keep_default_na=False,dtype=str)
    #df = pd.read_csv('datos2.csv',keep_default_na=False,dtype=int)
    print('Cargando Datos: ',len(df))
    return df
 
def fuzzy_control(genes,df,bandera):
    global rules, estado_potrero,puntuacion_potrero
    if estado_potrero != 'bueno':
        try:
            aux = []
            edad_list = list_edad(df)
            pi = list_pi(df)
            GA = list_GA(df)
            pf = list_pf(df)
            interpretacion_array = []
        except:
            print('error de listas')
        try:
            edad = ctrl.Antecedent(np.arange(0, 31, 1), 'edad')
            dif = ctrl.Antecedent(np.arange(0, 101, 1), 'dif')
            estadoAnimal = ctrl.Consequent(np.arange(0, 101, 1), 'estado')
        except:
            print('Error antecendentes y consecuentes')
        try:
            potrero = ctrl.Antecedent(np.arange(0,11,1),'potrero')
            potrero['malo'] = fuzz.trapmf(potrero.universe,[0,0,1,5])
            potrero['regular'] = fuzz.trapmf(potrero.universe,[1,5,7,8])
            potrero['bueno'] = fuzz.trapmf(potrero.universe,[7,8,10,10])
        except:print('potrero fallo')
        
        try:
            #edad.automf(3)
            edad['ternero'] = fuzz.trapmf(edad.universe, [0, 0, genes[0], genes[1]])
            edad['novillo'] = fuzz.trapmf(edad.universe, [genes[0], genes[1], genes[2],genes[3]])
            edad['adulto'] = fuzz.trapmf(edad.universe, [genes[2], genes[3], 30, 30])
        except:
            #print('Try1 ', genes)
            aux.append(genes[0])
            aux.append(genes[1])
            aux.append(genes[2])
            aux.append(genes[3])
            aux = sorted(aux)
            #print('Order Try1:',aux)
            edad['ternero'] = fuzz.trapmf(edad.universe, [0, 0, aux[0], aux[1]])
            edad['novillo'] = fuzz.trapmf(edad.universe, [aux[0], aux[1], aux[2],aux[3]])
            edad['adulto'] = fuzz.trapmf(edad.universe, [aux[2], aux[3], 30, 30])        
            
            aux.clear()
            
        try:    
            #dif.automf(3)
            dif['bajo'] = fuzz.trapmf(dif.universe, [0, 0, genes[4], genes[5]])
            dif['medio'] = fuzz.trapmf(dif.universe, [genes[4], genes[5],genes[6], genes[7]])
            dif['alto'] = fuzz.trapmf(dif.universe, [genes[6], genes[7], 100, 100])
        except:
        #print('Try2 ', genes)
            aux.append(genes[4])
            aux.append(genes[5])
            aux.append(genes[6])
            aux.append(genes[7]) 
            aux = sorted(aux)       
            #print('Order Try2:',aux)
            dif['bajo'] = fuzz.trapmf(dif.universe, [0, 0, aux[0], aux[1]])
            dif['medio'] = fuzz.trapmf(dif.universe, [aux[0], aux[1],aux[2], aux[3]])
            dif['alto'] = fuzz.trapmf(dif.universe, [aux[2], aux[3], 100, 100])
            
            aux.clear()        
            

        try:
            estadoAnimal['enfermo'] = fuzz.trapmf(estadoAnimal.universe, [0,0, genes[8], genes[9]])
            estadoAnimal['estable'] = fuzz.trapmf(estadoAnimal.universe, [genes[8], genes[9],100, 100])
        except:
            #print('Try3 ', genes)
            aux.append(genes[8])
            aux.append(genes[9])
            aux = sorted(aux)
            #print('Order Try3:',aux)
            estadoAnimal['enfermo'] = fuzz.trapmf(estadoAnimal.universe, [0,0, aux[0], aux[1]])
            estadoAnimal['estable'] = fuzz.trapmf(estadoAnimal.universe, [aux[0], aux[1],100, 100])        
            
            aux.clear()      
            

        # para ver las graficas

        #edad.view()
        #dif.view()
        #estadoAnimal.view()


        # Creamos las reglas difusas
        #try:
        if bandera == 1:
            rules = base_reglas_EAEP(genes,df,estado_potrero)
        
        #except:
        #print('Error de reglas')
        """rule1 = ctrl.Rule(edad['ternero'] & dif['bajo'], estadoAnimal['enfermo'])
        rule2 = ctrl.Rule(edad['ternero'] & dif['medio'], estadoAnimal['estable'])
        rule3 = ctrl.Rule(edad['novillo'] & dif['medio'], estadoAnimal['enfermo'])
        rule4 = ctrl.Rule(edad['novillo'] & dif['alto'], estadoAnimal['estable'])
        rule5 = ctrl.Rule(edad['adulto'] & dif['medio'], estadoAnimal['estable'])
        rule6 = ctrl.Rule(edad['adulto'] & dif['alto'], estadoAnimal['estable'])
        rule7 = ctrl.Rule(edad['novillo'] & dif['bajo'], estadoAnimal['enfermo'])
        rule8 = ctrl.Rule(edad['adulto'] & dif['bajo'], estadoAnimal['enfermo'])
        rule9 = ctrl.Rule(edad['ternero'] & dif['alto'], estadoAnimal['estable'])"""
        

        # control 
        try:
            tipping_ctrl = ctrl.ControlSystem(rules)
            tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        except:
            print('error tipping')
        # generamos una muestra

        for i in range(0,len(df)):
            #print('i',i)
            dife = (float(pf[i]) - float(pi[i]))/float(GA[i])
            if dife > 1:
                dife = 1
            dife = dife*100
            tipping.input['edad'] = float(edad_list[i])
            tipping.input['dif'] = dife
            tipping.input['potrero'] = float(puntuacion_potrero)
            #print(dife)

            # Crunch the numbers

            try:
                tipping.compute()
            except:
                print('aquiiiiii')

                interpretacion_array.clear()
                tam = len(df)
                for i in range(0,tam):
                    interpretacion_array.append(0)
                return interpretacion_array 
            #print(tipping)
            #print('-------------------------------------')
            #print(tipping.output['estado'])
            result = tipping.output['estado']
            #print(result)
            iEstable = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['estable'].mf,result)
            iEnfermo = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['enfermo'].mf,result)
            #print(str(iEstable)+'======'+str(iEnfermo))
            #time.sleep(2)
            if float(iEstable) >= float(iEnfermo):
                interpretacion_array.append(1)
            else:
                interpretacion_array.append(0)
                #print(fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['estable'].mf,result))
                #print(fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['enfermo'].mf,result))
                #estadoAnimal.view(sim=tipping)
                #print(edad_list[i])
                #print('------------------------------') 
        return interpretacion_array    
    else:
        try:
            aux = []
            edad_list = list_edad(df)
            pi = list_pi(df)
            GA = 11
            pf = list_pf(df)
            interpretacion_array = []
        except:
            print('error de listas')
        try:
            edad = ctrl.Antecedent(np.arange(0, 31, 1), 'edad')
            dif = ctrl.Antecedent(np.arange(0, 101, 1), 'dif')
            estadoAnimal = ctrl.Consequent(np.arange(0, 101, 1), 'estado')
        except:
            print('Error antecendentes y consecuentes')
        
        try:
            #edad.automf(3)
            edad['ternero'] = fuzz.trapmf(edad.universe, [0, 0, genes[0], genes[1]])
            edad['novillo'] = fuzz.trapmf(edad.universe, [genes[0], genes[1], genes[2],genes[3]])
            edad['adulto'] = fuzz.trapmf(edad.universe, [genes[2], genes[3], 30, 30])
        except:
            #print('Try1 ', genes)
            aux.append(genes[0])
            aux.append(genes[1])
            aux.append(genes[2])
            aux.append(genes[3])
            aux = sorted(aux)
            #print('Order Try1:',aux)
            edad['ternero'] = fuzz.trapmf(edad.universe, [0, 0, aux[0], aux[1]])
            edad['novillo'] = fuzz.trapmf(edad.universe, [aux[0], aux[1], aux[2],aux[3]])
            edad['adulto'] = fuzz.trapmf(edad.universe, [aux[2], aux[3], 30, 30])        
            
            aux.clear()
            
        try:    
            #dif.automf(3)
            dif['bajo'] = fuzz.trapmf(dif.universe, [0, 0, genes[4], genes[5]])
            dif['medio'] = fuzz.trapmf(dif.universe, [genes[4], genes[5],genes[6], genes[7]])
            dif['alto'] = fuzz.trapmf(dif.universe, [genes[6], genes[7], 100, 100])
        except:
        #print('Try2 ', genes)
            aux.append(genes[4])
            aux.append(genes[5])
            aux.append(genes[6])
            aux.append(genes[7]) 
            aux = sorted(aux)       
            #print('Order Try2:',aux)
            dif['bajo'] = fuzz.trapmf(dif.universe, [0, 0, aux[0], aux[1]])
            dif['medio'] = fuzz.trapmf(dif.universe, [aux[0], aux[1],aux[2], aux[3]])
            dif['alto'] = fuzz.trapmf(dif.universe, [aux[2], aux[3], 100, 100])
            
            aux.clear()        
            

        try:
            estadoAnimal['enfermo'] = fuzz.trapmf(estadoAnimal.universe, [0,0, genes[8], genes[9]])
            estadoAnimal['estable'] = fuzz.trapmf(estadoAnimal.universe, [genes[8], genes[9],100, 100])
        except:
            #print('Try3 ', genes)
            aux.append(genes[8])
            aux.append(genes[9])
            aux = sorted(aux)
            #print('Order Try3:',aux)
            estadoAnimal['enfermo'] = fuzz.trapmf(estadoAnimal.universe, [0,0, aux[0], aux[1]])
            estadoAnimal['estable'] = fuzz.trapmf(estadoAnimal.universe, [aux[0], aux[1],100, 100])        
            
            aux.clear()      
            
        if bandera == 1:
            rules = base_reglas_EA(genes,df)
        
        #except:
        #print('Error de reglas')
        """rule1 = ctrl.Rule(edad['ternero'] & dif['bajo'], estadoAnimal['enfermo'])
        rule2 = ctrl.Rule(edad['ternero'] & dif['medio'], estadoAnimal['estable'])
        rule3 = ctrl.Rule(edad['novillo'] & dif['medio'], estadoAnimal['enfermo'])
        rule4 = ctrl.Rule(edad['novillo'] & dif['alto'], estadoAnimal['estable'])
        rule5 = ctrl.Rule(edad['adulto'] & dif['medio'], estadoAnimal['estable'])
        rule6 = ctrl.Rule(edad['adulto'] & dif['alto'], estadoAnimal['estable'])
        rule7 = ctrl.Rule(edad['novillo'] & dif['bajo'], estadoAnimal['enfermo'])
        rule8 = ctrl.Rule(edad['adulto'] & dif['bajo'], estadoAnimal['enfermo'])
        rule9 = ctrl.Rule(edad['ternero'] & dif['alto'], estadoAnimal['estable'])"""
        
        #print(rules)
        # control 
        try:
            tipping_ctrl = ctrl.ControlSystem(rules)
            tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        except:
            print('error tipping')
        # generamos una muestra

        for i in range(0,len(df)):
            #print('i',i)
            dife = (float(pf[i]) - float(pi[i]))/11
            if dife > 1:
                dife = 1
            dife = dife*100
            tipping.input['edad'] = float(edad_list[i])
            tipping.input['dif'] = dife
            #print(dife)

            # Crunch the numbers

            try:
                tipping.compute()
            except:

                interpretacion_array.clear()
                tam = len(df)
                for i in range(0,tam):
                    interpretacion_array.append(0)
                return interpretacion_array 
            #print(tipping)
            #print('-------------------------------------')
            #print(tipping.output['estado'])
            result = tipping.output['estado']
            #print(result)
            iEstable = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['estable'].mf,result)
            iEnfermo = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['enfermo'].mf,result)
            #print(str(iEstable)+'======'+str(iEnfermo))
            #time.sleep(2)
            if float(iEstable) >= float(iEnfermo):
                interpretacion_array.append(1)
            else:
                interpretacion_array.append(0)

        return interpretacion_array

def individuo(num_vertices):
    #global genes
    genes = []
    cant = []
    delta_list = [6,20,10]
    min_max = [[13,30],[30,100],[60,65]]
    vertice_inicial = [[16,20,26,28],[35,40,65,70],[40,70]]
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
    return [individuo(10) for i in range(num)]

def fitness(poblacion,df):
    #print('tam poblacion fitness: ',len(poblacion))
    interpret_fuzzy = [0]
    i = 0
    array_p = df['prediccion'].to_list()
    score = 0
    pos = []
    #try:
    if True:
        for i in range(0,len(poblacion)):
            interpret_fuzzy = fuzzy_control(poblacion[i],df,1)
            #getfit = get_fitness(poblacion[i],df)
            score = 0
            try:
                for j in range(0,len(interpret_fuzzy)):
                    #print(str(interpret_fuzzy[j])+'======='+str(array_p[j]))
                    if float(interpret_fuzzy[j]) == float(array_p[j]):
                        score += 1
                    else:
                        pos.append(j)
                if float(score)/float(len(interpret_fuzzy))==1.0:
                    return float(score)/float(len(interpret_fuzzy)),poblacion[i] 
            except:
                print('error en el for interpret')
            #print(pos)
            #sys.exit(1)
        try:
            return float(score)/float(len(interpret_fuzzy)),poblacion[i] 
        except:
            pass
    #except:
        #print('error Poblacion Fitness: ')


def get_fitness(genes,df):
    global array_p
    try:
        n = fuzzy_control(genes,df,0)
        score = 0
        #print(str(n)+' '+str(array_p))
        for j in range(len(n)):
            if float(n[j]) == float(array_p[j]):
                score = score + 1
        return float(score)/len(df)         
    except:
        print(n)
def cross(father,mother):
    #children1 = mother[:3]+father[2:]
    #children2 = father[:3]+mother[2:]
    children1 = mother[:1]+father[1:]
    children2 = father[:1]+mother[1:]
    

    children1 = mother[:4]+father[4:5]+mother[5:]
    children2 = father[:4]+mother[4:5]+father[5:] 
    
    #children1 = mother[:8]+father[8:]
    #children2 = father[:8]+mother[8:]    
    #print('children1',children1)
    #print('children2',children2)
    return children1,children2 

def mutate(genes):
    gen = randint(0,9)
    #print('gen :',gen)
    #print(genes)
    try:
        if gen == 0:
            mutate = randint(14,18)
            genes[gen] = mutate

        if gen == 1:
            mutate = randint(18,21)
            genes[gen]= mutate

        if gen == 2:
            mutate = randint(22,26)
            genes[gen]= mutate

        if gen == 3:
            mutate = randint(27,30)
            genes[gen]= mutate

        if gen == 4:
            mutate = randint(30,35)
            genes[gen]= mutate 

        if gen == 5:
            mutate = randint(36,50)
            genes[gen]= mutate

        if gen == 6:
            mutate = randint(60,65)
            genes[gen]= mutate 

        if gen == 7:
            mutate = randint(66,71)
            genes[gen]= mutate

        if gen == 8:
            mutate = randint(50,60)
            genes[gen]= mutate   
                     
        if gen == 9:
            mutate = randint(61,65)
            genes[gen]= mutate    
            
        return genes         
    except:
        print('Error mutacion: ',genes)
        print('gen: ',gen)
        #print('mutate: ',mutate)

def selectMembersGeneration(poblacion,df):
    global array_p
    parents = []
    parents2 = []
    #parents.clear()
    score = 0
    #print('Select Generacion')


    for i in range(0, len(poblacion)):
        score = get_fitness(poblacion[i],df)
        #print('Genes: '+str(poblacion[i])+' Score: '+str(score))
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
        return poblacion    

def reproductionMembersGeneration(parents):
    global df
    #print('reproduccion Parents: ',parents)
    totalParents = len(parents)
    corte = totalParents//2
    nueva_poblacion = []
    nueva_poblacion2 = []
    #print(len(nueva_poblacion))
    #print("Padres seleccionados: ", totalParents)
    for i in range(0, corte):
        #print(i)
        #a = int(randint(0, corte))
        #b = int(randint(corte, (totalParents-1)))
        father = parents[i*2]
        mother = parents[(i*2)+1]
        children1,children2 = cross(father,mother)
        children1 = mutate(children1)
        children2 = mutate(children2)
        nueva_poblacion.append(children1)
        nueva_poblacion2.append(children2)
        nueva_poblacion = nueva_poblacion + nueva_poblacion2

    nueva_poblacion = nueva_poblacion[:len(df)]

    return nueva_poblacion  


if __name__ == '__main__':
    
    numeroP = input(str('Cual Potrero desea estudiar?   '))
    df = read_df(numeroP)
    estado_potrero,puntuacion_potrero = read_potrero(numeroP)
    #print(len(df))
    array_p = df['prediccion'].to_list()
    people = crearPoblacion(len(df))

    j = 0
    #else:
    score,genes = fitness(people,df)
    while True:
        
        #print('score: '+ str(score))
        
        if  j == 5:
            #print('Optimo')
            print('Generacion: ',5*j)
            
            #print(genes)
            print('Cromosoma: '+ str(genes)+ 'FA: '+str(score*100))
            salida = genes
            #print(score)
            break         
        
        parents = selectMembersGeneration(people,df)
        if len(parents) > 1:
            people = reproductionMembersGeneration(parents)
            aux2 = []
            for i in range(len(people)):
                #print('people ',people)
                o = get_fitness(people[i],df)
                aux2.append([o,people[i]])
                #print(o)
                aux2.sort(reverse=True)
            print('Generacion: ',5*j)
            print('Cromosoma: '+ str(aux2[0][1]) + ' FA: '+str(o*100))            
        else:
            aux = []
            for i in range(len(people)):
                #print('people ',people)
                o = get_fitness(people[i],df)
                aux.append([o,people[i]])
                #print(o)
                aux.sort(reverse=True)
            print('Generacion: ',5*j)
            #print(aux[0][1])
            salida = aux[0][1]
            print('Cromosoma: '+ str(aux[0][1]) + ' FA: '+str(o*100))
            break
        j = j + 1

l = []
l.append(numeroP)
lout = pd.DataFrame(l,columns=['potrero_act'])
out = pd.DataFrame(salida,columns=['genes'])
out = pd.concat([out,lout],axis=0)
out.to_csv('./fuzzy/genes.csv',index=0)             