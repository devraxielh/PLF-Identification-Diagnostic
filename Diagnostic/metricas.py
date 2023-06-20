import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# roc curve and auc score
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from os.path import join
from os import listdir
import re

def plot_roc_curve(fpr, tpr):
    plt.plot(fpr, tpr, color="orange", label="ROC")
    plt.plot([0, 1], [0, 1], color="darkblue", linestyle="--")
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()


df2 = pd.DataFrame()        
for file_name in sorted(listdir('./data/info')):
    print('file----->',file_name)
    df = pd.read_csv(join('./data/info/',file_name),keep_default_na = False,dtype = str)    
    df2 = pd.concat([df,df2],axis=0)
df2.to_csv('./data/test/data_test.csv',index=0)

df = pd.read_csv('./data/test/data_test.csv',keep_default_na = False,dtype = str)

df_i = df['peso_inicial']
df_f = df['peso_final']
df['ganancia'] = df['ganancia'].astype(float)
total = df['ganancia'].sum()
prom = float(total)/len(df)
#print(prom)
df['ganancia'] = '{}'.format(prom)
df2 = df_f.astype(float) - df_i.astype(float)
data_X=np.array([df['peso_inicial'].astype(float),df['peso_final'].astype(float),df['ganancia'].astype(float)])
#print(data_X.T)
#data_X = data_X.reshape(data_X.shape[1:])
class_label = np.array(df['prediccion'].astype(int))
#class_label = class_label.reshape(class_label.shape[1:])
#print(class_label)
#data_X, class_label = make_classification(n_samples=1000, n_classes=2, weights=[1,1], random_state=1)
#print(data_X)
#print(type(data_X))
#print(class_label)
#print(type(class_label))


trainX, testX, trainy, testy = train_test_split(data_X.T, class_label, test_size=0.3, random_state=1)


model = RandomForestClassifier()
model.fit(trainX, trainy)

probs = model.predict_proba(testX)

#print(probs)
probs = probs[:, 1]

lr_auc = roc_auc_score(testy, probs)
print('AUC: ',lr_auc)
#AUC: 0.95

fpr, tpr, thresholds = roc_curve(testy, probs)

plot_roc_curve(fpr, tpr)