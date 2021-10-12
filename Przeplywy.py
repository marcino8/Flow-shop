import pandas as pd
import numpy as np


def sumuj_rzad(df):
    sumy=[]
    for row in range(len(df.index)):
        suma = 0
        for col in range(len(df.columns)):
            if not isinstance(df.iloc[row,col], str):
                suma+=df.iloc[row,col]
        sumy.append(suma)
    return sumy

def wczytaj(isOrdered):
    df = pd.read_csv("dane1.csv")
    if(isOrdered):
        df=df.iloc[:,1:]
        print(df.iloc[0,0])
    print(df)
    df['Suma'] = sumuj_rzad(df)
    df=df.sort_values(by='Suma', ascending=False)
    print(df)


def policz_czasy():
    return 0


def wykonaj():
    return 0


wczytaj(True)