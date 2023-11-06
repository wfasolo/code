import pandas as pd

a=pd.read_csv('2020.csv')
b=pd.read_csv('2021.csv')
c=pd.read_csv('2022.csv')
d=pd.read_csv('2023.csv')

e=pd.concat([a,b,c,d])
print(e)
e.to_csv('forca.csv')