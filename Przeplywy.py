import pandas as pd
import numpy as np


def sumuj_rzad(df):
    sumy = []
    for row in range(len(df.index)):
        suma = 0
        for col in range(len(df.columns)):
            if not isinstance(df.iloc[row, col], str):
                suma += df.iloc[row, col]
        sumy.append(suma)
    return sumy


def wczytaj(isOrdered):
    df = pd.read_csv("dane1.csv")
    if (isOrdered):
        df = df.iloc[:, 1:]
    print(df)
    df['Suma'] = sumuj_rzad(df)
    df = df.sort_values(by='Suma', ascending=False)
    print(df)
    best_perm(df.iloc[:3, :], df.iloc[4,:])


def policz_czasy(df):
    df_calc = df.iloc[:, 1:]
    df_calc=df_calc.reset_index()
    df_calc = df_calc.iloc[:, 1:]
    itr=0
    for col in df_calc.columns:
        for row in df_calc.index:
            aktualny = df_calc.at[row, col]
            if row == 0 and itr == 0:
                df_calc.at[row,col]=aktualny
            elif row == 0:
                df_calc.at[row,col]=aktualny
            elif itr == 0:
                poprzednia_czesc = df_calc.at[row-1, col]
                df_calc.at[row,col]=poprzednia_czesc+aktualny
            else:
                poprzednia_czesc = df_calc.at[row-1, col]
                poprzednie_zadanie = df_calc.at[row, df_calc.columns[itr-1]]
                df_calc.at[row,col]=max(poprzednia_czesc, poprzednie_zadanie) + aktualny
        itr=itr+1
    print(df_calc)
    print(df_calc.iloc[len(df_calc.index)-1,len(df_calc.columns)-2])
    return df_calc.iloc[len(df_calc.index)-1,len(df_calc.columns)-2]

def best_perm(df, new_row):
    minczas = 99999999
    pozycja=0
    df=df.reset_index(drop=True)
    for i in range(0,len(df.index)+1):
        df2=insert_row(df,new_row,i)
        czas=policz_czasy(df2)
        if czas<minczas:
            minczas=czas
            pozycja=i;
    df2=insert_row(df,new_row,pozycja)
    print("Best")
    print(df2)
    return df2

def insert_row(df, row, row_index):
    df.loc[-1]=row
    df = df.reset_index(drop=True)
    c=df.loc[row_index]
    df.loc[row_index]=df.iloc[len(df.index)-1]
    df.loc[len(df.index) - 1]=c
    print(df)
    return df

def wykonaj():
    return 0


wczytaj(True)
