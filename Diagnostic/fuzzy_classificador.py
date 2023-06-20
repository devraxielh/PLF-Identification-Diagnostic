import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D 
import skfuzzy as fuzz
import array as arr
import pandas as pd
from os.path import join
from os import listdir
import re

def extract_info(look_for, text, group):
    if re.search(look_for, text):
        return re.search(look_for, text).group(group)
    else:
        return ''

def NúmeroDeGruposÓptimo (filename,maxConjuntos):
    #print(filename)
    df = pd.read_csv(join('./data/potreros/',file_name),keep_default_na = False,dtype =str)
    #print(df);
    data=np.array([df['peso_inicial'].astype(float),df['peso_final'].astype(float),df['edad'].astype(float)])
    data = data.astype(float)
    #data_in_file = np.loadtxt(NombreDeArchivo).T;
    conjuntos=np.arange(2,maxConjuntos+1)
    FP=np.zeros(np.shape(conjuntos))
    m=2
    error=1e-9
    max_iter=100
    for conj in conjuntos:
        cntr, u, u0, d, jm, p, fpc=fuzz.cmeans(data, conj, m, error, max_iter)
        print(jm)
        FP[conj-2]=fpc
        plt.title("FPC vs número de conjuntos")
        plt.ylabel("FPC")
        plt.xlabel("Número de conjuntos")
        plt.ylim([0,1])
        plt.grid()
        plt.plot(conjuntos,FP,'*')   
    
    return np.argmax(FP)+2


if __name__ == '__main__':
    

    """df2 = pd.DataFrame()        
    for file_name in sorted(listdir('./data/potreros')):
        #print('file----->',file_name)
        df = pd.read_csv(join('./data/potreros/',file_name),keep_default_na = False,dtype = str)    
        df2 = pd.concat([df,df2],axis=0)
    df2.to_csv('./data/test/data_test.csv',index=0)"""   

    for file_name in sorted(listdir('./data/test')):
        df = pd.read_csv(join('./data/test/',file_name),keep_default_na = False,dtype = str)
        df_i = df['peso_inicial']
        df_f = df['peso_final']
        df['ganancia'] = df['ganancia'].astype(float)
        total = df['ganancia'].sum()
        prom = float(total)/len(df)
        print(prom)
        #df['ganancia'] = '{}'.format(prom)
        df2 = df_f.astype(float) - df_i.astype(float)
        data=np.array([df['peso_inicial'].astype(float),df['peso_final'].astype(float),df['ganancia'].astype(float)])
        conjuntos = 2
        m=2
        error=1e-9
        max_iter=100
        cntr, u, u0, d, jm, p, fpc=fuzz.cmeans(data, conjuntos, m, error, max_iter)
        c1 = cntr[0].sum()
        c2 = cntr[1].sum()
        
    if c1 > c2:
        grupo1 = 'enfermos'
        grupo2 = 'estables'
    if c2 > c1:
        grupo2 = 'enfermos'
        grupo1 = 'estables'    
    
    for file_name in sorted(listdir('./data/potreros')):
        #print('file----->',file_name)
        df = pd.read_csv(join('./data/potreros/',file_name),keep_default_na = False,dtype = str)
        #print(df)
        number = extract_info('(\d+)',file_name,1)
        #filename = "../data/muestra2.csv";
        #df = pd.read_csv(filename,keep_default_na = False,dtype = float)
        #print(df);
        df_i = df['peso_inicial']
        df_f = df['peso_final']
        df2 = df_f.astype(float) - df_i.astype(float)
        #print(df_i)
        #df2 = float(df['peso_final']) - float(df['peso_inicial'])
        #df2=np.array([df2]);
        data=np.array([df['peso_inicial'].astype(float),df['peso_final'].astype(float),df['ganancia'].astype(float)])
        #print(df)

        #conjuntos = NúmeroDeGruposÓptimo(file_name,9);
        conjuntos = 2
        m=2
        error=1e-9
        max_iter=100
        #cntr, u, u0, d, jm, p, fpc=fuzz.cmeans(data, conjuntos, m, error, max_iter)
        #print(jm)
        u, u0, d, jm, p, fpc= fuzz.cmeans_predict(data, cntr, m , error , max_iter)

        pertenencia = pd.DataFrame(u.T,columns=['{}'.format(grupo1),'{}'.format(grupo2)])
        pertenencia.to_csv('./data/fuzzy_pertenencias/grados_pertenencia{}.csv'.format(number),index=0)
        #filename2 = "grados_pertenencia.csv";
        #df2 = pd.read_csv(filename2,keep_default_na = False,dtype = float);
        df = pd.concat([df,pertenencia],axis=1)
        prediccion = []
        estado = []
        for i,row in df.iterrows():#df2.iterrows():
            """if (float(row['peso_final'])-float(row['peso_inicial']))/11 > 0.5:
                prediccion.append('1')
                estado.append((float(row['peso_final'])-float(row['peso_inicial']))/11)
            else:
                prediccion.append('0')
                estado.append((float(row['peso_final'])-float(row['peso_inicial']))/11) """      
            if row['estables'] > row['enfermos']:
                prediccion.append('1')
                estado.append(row['estables']*100)
            else:
                prediccion.append('0')
                estado.append(row['enfermos']*100)

        df['prediccion'] = prediccion
        df['grados_pertenencia'] = estado
        #df.drop(['estables','enfermos'],axis=1)
        df.to_csv('./data/info/muestra{}.csv'.format(number),index=0)
    print('END');    