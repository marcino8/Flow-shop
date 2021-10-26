import pandas as pd
import numpy as np


def sum_row(df):
    sums = []
    for row in range(len(df.index)):
        sum = 0
        for col in range(len(df.columns)):
            if not isinstance(df.iloc[row, col], str):
                sum += df.iloc[row, col]
        sums.append(sum)
    return sums


def load(isOrdered):
    df = pd.read_csv("dane2.csv")
    if (isOrdered):
        df = df.iloc[:, 1:]
    df['Suma'] = sum_row(df)
    df = df.sort_values(by='Suma', ascending=False)
    start(df)


def calculate_time(df):
    df_calc = df.iloc[:, 1:]
    df_calc = df_calc.reset_index()
    df_calc = df_calc.iloc[:, 1:]
    itr = 0
    for col in df_calc.columns:
        for row in df_calc.index:
            current = df_calc.at[row, col]
            if row == 0 and itr == 0:
                df_calc.at[row, col] = current
            elif row == 0:
                df_calc.at[row, col] = current+df_calc.at[row, df_calc.columns[itr - 1]]
            elif itr == 0:
                previous_job = df_calc.at[row - 1, col]
                df_calc.at[row, col] = previous_job + current
            else:
                previous_job = df_calc.at[row - 1, col]
                previous_task = df_calc.at[row, df_calc.columns[itr - 1]]
                df_calc.at[row, col] = max(previous_job, previous_task) + current
        itr = itr + 1
    return df_calc.iloc[len(df_calc.index) - 1, len(df_calc.columns) - 2]

def hc(df, new_row):
    minczas = 99999999
    pozycja=0
    df=df.reset_index(drop=True)
    for i in range(0,len(df.index)+1):
        df2=insert_row(df,new_row,i)
        czas=calculate_time(df2)
        if czas<minczas:
            minczas=czas
            pozycja=i;
    df2=insert_row(df,new_row,pozycja)
    return df2

def insert_row(df, row, row_index):
    df.loc[-1]=row
    df = df.reset_index(drop=True)
    c=df.loc[row_index]
    df.loc[row_index]=df.iloc[len(df.index)-1]
    df.loc[len(df.index) - 1]=c
    return df

def start(df):
    odf=df.loc[0:1,:]
    print(odf)
    for i in range(1, len(df.index)):
        odf=hc(odf,df.iloc[i-1,:])
        print(calculate_time(odf))
    odf.to_csv("dane2_neh.csv", sep=",")


load(True)
## DLA DRUGIEGO ZBIORU DANYCH 11451