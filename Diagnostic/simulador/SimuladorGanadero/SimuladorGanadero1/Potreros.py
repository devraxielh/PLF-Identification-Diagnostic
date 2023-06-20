import math
import random
import warnings
import numpy as np
import pandas as pd
from ast import literal_eval
from scipy.spatial import distance

warnings.filterwarnings('ignore')



def Datos_del_Pasto(ruta):
  df = pd.read_excel(ruta+'DataIn/Pasto.xlsx')
  df = df.iloc[[11,14,0,2,3]]
  return df.drop(['Unnamed: 0'], axis=1)

def Potreros(Cantidad_de_Potreros, Area_potreros_min, Area_potreros_max, Max_x, Max_y, Min_y, Min_x, ruta):
  potreros = []
  for i in range(Cantidad_de_Potreros):
      pasto = Datos_del_Pasto(ruta).sample()
      Seleccion_Cantidad_hojas_planta = literal_eval(pasto['Cantidad_hojas_p_d'].values[0])
      area_potrero = random.randrange(Area_potreros_min, Area_potreros_max)
      x,y = random.randrange(Min_x,Max_x),random.randrange(Min_y,Max_y)
      potreros.append([
                          i,
                          area_potrero,
                          x,
                          y,
                          pasto['Nombre_Pasto'].values[0],
                          pasto['Tolerancia_sequia'].values[0],
                          pasto['Epoca_floracion'].values[0],
                          literal_eval(pasto['Ganancia_diaria_lluvia'].values[0]),
                          literal_eval(pasto['Ganancia_diaria_seca'].values[0]),
                      ])
  for i in range(Cantidad_de_Potreros):
    temp = []
    for j in range(Cantidad_de_Potreros):
      temp.append([round(distance.euclidean((potreros[i][2],potreros[i][3]),(potreros[j][2],potreros[j][3])),2)])
      potreros[i].append(temp)
  df = pd.DataFrame(potreros)
  df.rename(columns={0:'Potreros',1:'Area_mt2',2:'Pos_x',3:'Pos_y',4:'Pasto',5:'Tolerancia_sequia',6:'Epoca_floracion',7:'Ganancia_diaria_lluvia',8:'Ganancia_diaria_seca',9:'Distancias_mt2'},inplace=True)
  for i in range(len(df)):
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Enero','01')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Febrero','02')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Marzo','03')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Abril','04')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Mayo','05')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Junio','06')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Julio','07')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Agosto','08')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Septiembre','09')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Octubre','10')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Noviembre','11')
    df['Epoca_floracion'][i]=df['Epoca_floracion'][i].replace('Diciembre','12')

  #df = df.drop([11:100], axis=1)
  df = df[['Potreros','Area_mt2','Pos_x','Pos_y','Pasto','Tolerancia_sequia','Epoca_floracion','Ganancia_diaria_lluvia','Ganancia_diaria_seca','Distancias_mt2']]
  df.to_excel(ruta+'/DataIn/Potreros.xlsx')
