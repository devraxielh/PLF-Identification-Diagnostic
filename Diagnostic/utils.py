import random
from matplotlib import pyplot as plt
import numpy as np
from random import randint
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd



def save_SBR(rules):
    with open ("SBR.txt", "w") as f: #Abrimos de modo write (w)
        contenido = f.write('Reglas: '+'\n')
        contenido = f.write('------------------------------------------\n')
        contenido = f.write(str(rules)+'\n')
        contenido = f.write('------------------------------------------\n')
        f.close()


def list_estado(df):
    Array = df['grados_pertenencia'].to_numpy(copy=True)
    list_z = list(Array)
    #print('Datos Peso Inicial: ',len(list_z))
    return list_z

def list_pi(df):
    Array = df['peso_inicial'].to_numpy(copy=True)
    list_z = list(Array)
    #print('Datos Peso Inicial: ',len(list_z))
    return list_z

def list_pf(df):
    zipArray = df['peso_final'].to_numpy(copy=True)
    list_z = list(zipArray)
    #print('Datos Peso Final: ',len(list_z))
    return list_z

def list_GA(df):
    zipArray = df['ganancia'].to_numpy(copy=True)
    list_z = list(zipArray)
    #print('Datos Ganancia mensual: ',len(list_z))
    return list_z

def list_edad(df):
    zipArray = df['edad'].to_numpy(copy=True)
    list_z = list(zipArray)
    #print('Datos edad: ',len(list_z))
    return list_z    

def list_pasto(df):
    Array = df['rating_pasto'].to_numpy(copy=True)
    list_z = list(Array)
    #print('Datos Peso Inicial: ',len(list_z))
    return list_z

def list_suelo(df):
    zipArray = df['rating_suelo'].to_numpy(copy=True)
    list_z = list(zipArray)
    #print('Datos Peso Final: ',len(list_z))
    return list_z 

def base_reglas_EA(genes,df):
    try:
        edad_list = list_edad(df)
        pi = list_pi(df)
        Ga = list_GA(df)
        pf = list_pf(df)
        es = list_estado(df)
        candidatas = []
        aux = [] 

    except:
        print('error de datos')
        edad_list = list_edad(df)
        pi = list_pi(df)
        Ga = list_GA(df)
        pf = list_pf(df)
        es = list_estado(df)
        candidatas = []
        aux = []            
    
    try:
        edad = ctrl.Antecedent(np.arange(0, 31, 1), 'edad')
        dif = ctrl.Antecedent(np.arange(0, 101, 1), 'dif')
        estadoAnimal = ctrl.Consequent(np.arange(0, 101, 1), 'estado')

    except:
        print('error ante y conse')
        edad = ctrl.Antecedent(np.arange(0, 31, 1), 'edad')
        dif = ctrl.Antecedent(np.arange(0, 101, 1), 'dif')
        estadoAnimal = ctrl.Consequent(np.arange(0, 101, 1), 'estado')        

    try:
        edad['ternero'] = fuzz.trapmf(edad.universe, [0, 0, genes[0], genes[1]])
        edad['novillo'] = fuzz.trapmf(edad.universe, [genes[0], genes[1], genes[2],genes[3]])
        edad['adulto'] = fuzz.trapmf(edad.universe, [genes[2], genes[3], 30, 30])   
    except:
        #print('Try1 utils', genes)
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
    #edad.view()
    #dif.view()
    #estadoAnimal.view()
    for j in range(len(df)):
        try:
            dife = (float(pf[j]) - float(pi[j]))/11
            if dife > 1:
                dife = 1
            dife = dife*100

        except:
            print('aqui error')
            dife = (pf[j] - pi[j])/11
            if dife > 1:
                dife = 1
            dife = dife*100            
        try:
            p = 'regular'
            #print(fuzz.interp_membership(edad.universe, edad['ternero'].mf,edad_list[i]))
            x1_1 = fuzz.interp_membership(edad.universe, edad['ternero'].mf,float(edad_list[j]))
            #print('---------------------------------------')
            #print(x1_1)
            #print(fuzz.interp_membership(edad.universe, edad['novillo'].mf,edad_list[i]))
            x1_2 = fuzz.interp_membership(edad.universe, edad['novillo'].mf,float(edad_list[j]))
            #print(x1_2)
            #print(fuzz.interp_membership(edad.universe, edad['adulto'].mf,edad_list[i]))
            x1_3 = fuzz.interp_membership(edad.universe, edad['adulto'].mf,float(edad_list[j]))
            #print(x1_3)
            #print('---------------------------------------')
            #print('dife',dife)
            #print(fuzz.interp_membership(dif.universe, dif['bajo'].mf,dife))
            x2_1 = fuzz.interp_membership(dif.universe, dif['bajo'].mf,dife)
            #print(x2_1)
            #print(fuzz.interp_membership(dif.universe, dif['medio'].mf,dife))
            x2_2 = fuzz.interp_membership(dif.universe, dif['medio'].mf,dife)
            #print(x2_2)
            #print(fuzz.interp_membership(dif.universe, dif['alto'].mf,dife)) 
            x2_3 = fuzz.interp_membership(dif.universe, dif['alto'].mf,dife) 
            #print(x2_3)
            #y1_1 = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['estable'].mf,float(es[j]))
            #y1_2 = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['enfermo'].mf,float(es[j]))
            #print(es[i])
            #print('---------------------------------------')
            #print('Las Y '+ str(y1_1)+' '+str(y1_2))
            
            if x1_1 >= x1_2 and x1_1 >= x1_3:
                x1 = x1_1
                fp = 'ternero'
            elif x1_2 >= x1_1 and x1_2 >= x1_3:
                x1 = x1_2
                fp = 'novillo'
            elif x1_3 >= x1_1 and x1_3 >= x1_2:
                x1 = x1_3
                fp = 'adulto'
        
            if x2_1 >= x2_2 and x2_1 >= x2_3:
                x2 = x2_1
                fp2 = 'bajo'
            elif x2_2 >= x2_1 and x2_2 >= x2_3:
                x2 = x2_2
                fp2 = 'medio'
            elif x2_3 >= x2_1 and x2_3 >= x2_2:
                x2 = x2_3
                fp2 = 'alto'
    
            if dife >= 60.0:
                y = 'estable'
            else:
                y = 'enfermo'    
            #if y1_1 >= y1_2:
            #y = 'estable'
            #else:
            #y = 'enfermo'
            #print('dife',dife)
            #print('Compatibilidad: '+ str(x1)+ ' '+str(x2))
            #print('Regla candidata: '+ str(fp)+ ' '+str(fp2)+ ' '+str(y))
            #time.sleep(5)

        except:
            print('error compatibilidad')           
        
        count = 0
        regla_aux = str(fp)+ ' '+str(fp2)+ ' '+str(y)
        if len(candidatas) == 0:
            candidatas.append([fp,fp2,y,x1,x2])
        #array.append([fp,fp2,y])
        else:
            for i in range(len(candidatas)):
                regla_candidata = str(candidatas[i][0]) + ' '+ str(candidatas[i][1]) + ' '+ str(candidatas[i][2])
                if regla_aux != regla_candidata:
                    if fp == candidatas[i][0] and fp2 == candidatas[i][1]:
                        certeza_regla_candidata = candidatas[i][3]*candidatas[i][4]
                        certeza_regla_evaluar = x1*x2
                    
                        if certeza_regla_evaluar > certeza_regla_candidata:
                            candidatas.pop(i)
                            candidatas.append([fp,fp2,y,x1,x2])
                            count=0 
                            break
                        else:
                            count = 0
                            break
                    else:
                        count = count + 1
                        if count == len(candidatas):
                            candidatas.append([fp,fp2,y,x1,x2])
                            count = 0
                else:
                    count = 0
                    break
        #print(j+1)
        #print(candidatas)
    #print('Longitud de la Base de reglas: ',len(candidatas))
    #print('Base de reglas: ',candidatas)
    #array = candidatas
    #print('Final Base de reglas')
    #print('reglas candidatas: ',candidatas)
    #return candidatas
    rules = []
    array = candidatas
    for i in range(len(array)):
        ed = array[i][0]
        diff = array[i][1]
        state = array[i][2]
        rule = ctrl.Rule(edad['{}'.format(ed)] & dif['{}'.format(diff)], estadoAnimal['{}'.format(state)])
        rules.append(rule)        
    
    save_SBR(rules)
    return rules

def base_reglas_EAEP(genes,df,estado_potrero):
    try:
        edad_list = list_edad(df)
        pi = list_pi(df)
        Ga = list_GA(df)
        pf = list_pf(df)
        es = list_estado(df)
        candidatas = []
        aux = [] 

    except:
        print('error de datos')
        edad_list = list_edad(df)
        pi = list_pi(df)
        Ga = list_GA(df)
        pf = list_pf(df)
        es = list_estado(df)
        candidatas = []
        aux = []            
    
    try:
        edad = ctrl.Antecedent(np.arange(0, 31, 1), 'edad')
        dif = ctrl.Antecedent(np.arange(0, 101, 1), 'dif')
        estadoAnimal = ctrl.Consequent(np.arange(0, 101, 1), 'estado')

    except:
        print('error ante y conse')
        edad = ctrl.Antecedent(np.arange(0, 31, 1), 'edad')
        dif = ctrl.Antecedent(np.arange(0, 101, 1), 'dif')
        estadoAnimal = ctrl.Consequent(np.arange(0, 101, 1), 'estado')        

    try:
        edad['ternero'] = fuzz.trapmf(edad.universe, [0, 0, genes[0], genes[1]])
        edad['novillo'] = fuzz.trapmf(edad.universe, [genes[0], genes[1], genes[2],genes[3]])
        edad['adulto'] = fuzz.trapmf(edad.universe, [genes[2], genes[3], 30, 30])   
    except:
        #print('Try1 utils', genes)
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
        potrero = ctrl.Antecedent(np.arange(0,11,1),'potrero')
        potrero['malo'] = fuzz.trapmf(potrero.universe,[0,0,1,5])
        potrero['regular'] = fuzz.trapmf(potrero.universe,[1,5,7,8])
        potrero['bueno'] = fuzz.trapmf(potrero.universe,[7,8,10,10])
    except:print('aqui fallo el potrero utils.py')


    try:    
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
    #edad.view()
    #dif.view()
    #estadoAnimal.view()
    for j in range(len(df)):
        try:
            dife = (float(pf[j]) - float(pi[j]))/float(Ga[j])
            if dife > 1:
                dife = 1
            dife = dife*100

        except:
            print('aqui error')
            dife = (pf[j] - pi[j])/Ga[j]
            if dife > 1:
                dife = 1
            dife = dife*100            
        try:

            #print(fuzz.interp_membership(edad.universe, edad['ternero'].mf,edad_list[i]))
            x1_1 = fuzz.interp_membership(edad.universe, edad['ternero'].mf,float(edad_list[j]))
            #print('---------------------------------------')
            #print(x1_1)
            #print(fuzz.interp_membership(edad.universe, edad['novillo'].mf,edad_list[i]))
            x1_2 = fuzz.interp_membership(edad.universe, edad['novillo'].mf,float(edad_list[j]))
            #print(x1_2)
            #print(fuzz.interp_membership(edad.universe, edad['adulto'].mf,edad_list[i]))
            x1_3 = fuzz.interp_membership(edad.universe, edad['adulto'].mf,float(edad_list[j]))
            #print(x1_3)
            #print('---------------------------------------')
            #print('dife',dife)
            #print(fuzz.interp_membership(dif.universe, dif['bajo'].mf,dife))
            x2_1 = fuzz.interp_membership(dif.universe, dif['bajo'].mf,dife)
            #print(x2_1)
            #print(fuzz.interp_membership(dif.universe, dif['medio'].mf,dife))
            x2_2 = fuzz.interp_membership(dif.universe, dif['medio'].mf,dife)
            #print(x2_2)
            #print(fuzz.interp_membership(dif.universe, dif['alto'].mf,dife)) 
            x2_3 = fuzz.interp_membership(dif.universe, dif['alto'].mf,dife) 
            #print(x2_3)
            #y1_1 = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['estable'].mf,float(es[j]))
            #y1_2 = fuzz.interp_membership(estadoAnimal.universe, estadoAnimal['enfermo'].mf,float(es[j]))
            #print(es[i])
            #print('---------------------------------------')
            #print('Las Y '+ str(y1_1)+' '+str(y1_2))
            es_p = estado_potrero 
            #print(es_p)
            if x1_1 >= x1_2 and x1_1 >= x1_3:
                x1 = x1_1
                fp = 'ternero'
            elif x1_2 >= x1_1 and x1_2 >= x1_3:
                x1 = x1_2
                fp = 'novillo'
            elif x1_3 >= x1_1 and x1_3 >= x1_2:
                x1 = x1_3
                fp = 'adulto'
        
            if x2_1 >= x2_2 and x2_1 >= x2_3:
                x2 = x2_1
                fp2 = 'bajo'
            elif x2_2 >= x2_1 and x2_2 >= x2_3:
                x2 = x2_2
                fp2 = 'medio'
            elif x2_3 >= x2_1 and x2_3 >= x2_2:
                x2 = x2_3
                fp2 = 'alto'
    
            if dife >= 60.0:
                y = 'estable'
            else:
                y = 'enfermo'    
            #if y1_1 >= y1_2:
            #y = 'estable'
            #else:
            #y = 'enfermo'
            #print('dife',dife)
            #print('Compatibilidad: '+ str(x1)+ ' '+str(x2))
            #print('Regla candidata: '+ str(fp)+ ' '+str(fp2)+ ' '+str(y))
            #time.sleep(5)

        except:
            print('error compatibilidad')           
        
        count = 0
        regla_aux = str(fp)+ ' '+str(fp2)+' '+str(es_p)+' '+str(y)
        if len(candidatas) == 0:
            candidatas.append([fp,fp2,es_p,y,x1,x2])
        #array.append([fp,fp2,y])
        else:
            for i in range(len(candidatas)):
                regla_candidata = str(candidatas[i][0]) + ' '+ str(candidatas[i][1]) + ' '+ str(candidatas[i][2]) + ' '+str(candidatas[i][3])
                if regla_aux != regla_candidata:
                    if fp == candidatas[i][0] and fp2 == candidatas[i][1]:
                        certeza_regla_candidata = candidatas[i][4]*candidatas[i][5]
                        certeza_regla_evaluar = x1*x2
                    
                        if certeza_regla_evaluar > certeza_regla_candidata:
                            candidatas.pop(i)
                            candidatas.append([fp,fp2,es_p,y,x1,x2])
                            count=0 
                            break
                        else:
                            count = 0
                            break
                    else:
                        count = count + 1
                        if count == len(candidatas):
                            candidatas.append([fp,fp2,es_p,y,x1,x2])
                            count = 0
                else:
                    count = 0
                    break

    rules = []
    array = candidatas
    #print(array)
    for i in range(len(array)):
        ed = array[i][0]
        diff = array[i][1]
        state = array[i][3]
        rule = ctrl.Rule((edad['{}'.format(ed)] & dif['{}'.format(diff)]) & potrero['{}'.format(es_p)], estadoAnimal['{}'.format(state)])
        rules.append(rule)        
    
    save_SBR(rules)
    return rules    


