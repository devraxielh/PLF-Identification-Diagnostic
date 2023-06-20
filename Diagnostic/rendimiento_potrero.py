import re
import string
from os.path import join
from os import listdir
import pandas as pd
import time
import csv
from pandas import read_csv
import string
from datetime import datetime 
from random import randint
from tqdm import tqdm


Data_Dictionary = {
    'peso_inicial' : [],
    'peso_final' : [],
    'ganancia_mensual' : [],
    'edad': [],
    #'prediccion': [],
}


#def clima_process(row):





def process(row):

    e = (row['edad_list'] * 12)/365
    row['edad_list'] = int(e)
    lista1.append(int(e))
    return row

if __name__ == '__main__':
    lista_clima = []
    ## generar entrada potrero
    
    
    clima_df =  pd.read_csv('./data/clima.csv',keep_default_na=False,dtype=str)
    #print(clima_df)
    #r= clima_df.iloc[0]
    #print(r['mes'])
    
    for i in range(12):
        count_s = 0
        count_t = 0
        count_l = 0

        df = clima_df['mes'] == '{}'.format(i+1)
        df = clima_df[df]
        for n,row in df.iterrows():
            if row['temporada'].lower() == 'seca':
                count_s = count_s +1
            if row['temporada'].lower() == 'transicion':
                count_t = count_t + 1
            if row['temporada'].lower() == 'lluvia':
                count_l = count_l + 1
        if count_s > count_t and count_s > count_l:
            lista_clima.append([i+1,'seca'])
        if count_t > count_s and count_t > count_l:
            lista_clima.append([i+1,'transicion'])
        if count_l > count_t and count_l > count_s:
            lista_clima.append([i+1,'lluvia'])
    df = pd.DataFrame(lista_clima,columns=['mes','clima'])
    #df.to_csv('./data/clima_por_mes.csv',index=0)

    
    pastos_df =  pd.read_csv('./data/pastos.csv',keep_default_na=False,dtype=str)
    lista_pastos = []
    for i in range(12):
        n = randint(0,14)
        fila = pastos_df.iloc[n]
        #print(fila)
        tipo = fila['codigo']
        nombre = fila['nombre']
        tolerancia = fila['tolerancia']
        lista_pastos.append([tipo,nombre,tolerancia])
    df_pastos = pd.DataFrame(lista_pastos,columns=['tipo','nombre','tolerancia'])

    df1 = pd.concat([df,df_pastos],axis=1)
    #print(df1)
    p = []
    status = []
    for n,row in df1.iterrows():
        temp = randint(20,31)
        if str(row['clima']) == 'seca' and str(row['tolerancia']) == 'Media':
            p.append(randint(5,7))
        if str(row['clima']) == 'seca' and str(row['tolerancia']) == 'Baja':
            p.append(randint(1,2))
        if str(row['clima']) == 'seca' and str(row['tolerancia']) == 'Media/Baja':
            p.append(randint(2,5))
        if str(row['clima']) == 'seca' and str(row['tolerancia']) == 'Alta':
            p.append(randint(8,10))
        
        if str(row['clima']) == 'lluvia':
            p.append(randint(6,8))
        if str(row['clima']) == 'transicion':
            p.append(randint(4,5))                         
        
    puntuacion = pd.DataFrame(p,columns=['forraje'])
    for i in range(len(p)):
        if p[i] >= 1 and p[i] <=3:
            status.append('malo')
        if p[i] >= 4 and p[i] <=6:
            status.append('regular')
        if p[i] >= 7 and p[i] <=10:
            status.append('bueno')
    estado = pd.DataFrame(status,columns=['estado'])

    pre = pd.concat([puntuacion,estado],axis=1)
    aux = df1.loc[:,['nombre','clima','mes']]                
    aux = pd.concat([aux,pre],axis=1)
    aux.to_csv('./data/potrero_predict.csv',index=0)


    tqdm.pandas(ncols=100,desc='check: ')
    lista1 = []
    pesos_animales = pd.read_csv('./data/pesos.csv',keep_default_na=False,dtype=float)
    edad = pd.read_csv('./data/edad.csv',keep_default_na=False,dtype=int)
    
    lista = []
    edad = edad.progress_apply(lambda t: process(t),axis = 1)
    a = list(pesos_animales.columns)
    for j in range(12):
        for i in range(len(a)):#print(a[i])
            #print(str(j)+'='+str(i))
            #time.sleep(1)
            if str(aux['mes'][j]) == '1': 
                peso_i = pesos_animales[a[i]].iloc[0]
                peso_f = pesos_animales[a[i]].iloc[30]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
            if str(aux['mes'][j]) == '2':
                peso_i = pesos_animales[a[i]].iloc[31]
                peso_f = pesos_animales[a[i]].iloc[59]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])               
                #mini_df = pesos_animales[a[i]].iloc[31:59]
            if str(aux['mes'][j]) == '3':
                peso_i = pesos_animales[a[i]].iloc[59]
                peso_f = pesos_animales[a[i]].iloc[90]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[59:90] 
            if str(aux['mes'][j]) == '4':
                peso_i = pesos_animales[a[i]].iloc[90]
                peso_f = pesos_animales[a[i]].iloc[120]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[90:120]  
            if str(aux['mes'][j]) == '5':
                peso_i = pesos_animales[a[i]].iloc[120]
                peso_f = pesos_animales[a[i]].iloc[151]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[120:151]  #desde:hasta
            if str(aux['mes'][j]) == '6':
                peso_i = pesos_animales[a[i]].iloc[151]
                peso_f = pesos_animales[a[i]].iloc[181]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[151:181]
            if str(aux['mes'][j]) == '7':
                peso_i = pesos_animales[a[i]].iloc[181]
                peso_f = pesos_animales[a[i]].iloc[212]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[181:212] 
            if str(aux['mes'][j]) == '8':
                peso_i = pesos_animales[a[i]].iloc[212]
                peso_f = pesos_animales[a[i]].iloc[243]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[212:243] 
            if str(aux['mes'][j]) == '9':
                peso_i = pesos_animales[a[i]].iloc[243]
                peso_f = pesos_animales[a[i]].iloc[273]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[243:273]  #desde:hasta
            if str(aux['mes'][j]) == '10':
                peso_i = pesos_animales[a[i]].iloc[273]
                peso_f = pesos_animales[a[i]].iloc[304]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[273:304]
            if str(aux['mes'][j]) == '11':
                peso_i = pesos_animales[a[i]].iloc[304]
                peso_f = pesos_animales[a[i]].iloc[334]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[304:334] 
            if str(aux['mes'][j]) == '12':
                peso_i = pesos_animales[a[i]].iloc[334]
                peso_f = pesos_animales[a[i]].iloc[365]
                g = peso_f - peso_i
                lista.append([lista1[i],peso_i,peso_f,g,a[i]])
                #mini_df = pesos_animales[a[i]].iloc[334:365]            
        out =pd.DataFrame(lista,columns=['edad','peso_inicial','peso_final','ganancia','id_animal'])
        lista.clear()
        out.to_csv('./data/potreros/potrero{}.csv'.format(j+1),index=0)

       

    """peso_i = list(pesos_animales.iloc[0])
    peso_f = list(pesos_animales.iloc[-1])


    for i in range(len(peso_i)):
        n = randint(30,80)
        lista.append([lista1[i],peso_i[i],peso_f[i]-n,109.5])
    df = pd.DataFrame(lista,columns=['edad','peso_inicial','peso_final','ganancia'])
    print(df)
    df.to_csv('./data/muestra2.csv',index=0)"""
    print('END')