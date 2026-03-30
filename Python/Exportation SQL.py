import urllib
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import types

df=pd.read_csv('PORTAFOLIO_CONSUMER_ANALYTICS/Data/consumer_clean.csv')

params= urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=(local)\\SQLEXPRESS;"
    "DATABASE=consumer_analytics;"
    "Trusted_Connection=yes;"
)

engine= create_engine(f'mssql+pyodbc:///?odbc_connect={params}')
print('Conexión exitosa')

df.to_sql(
    name= 'consumer_data',
    con= engine,
    schema= 'dbo',
    if_exists= 'replace',
    index= False,
    dtype={
        "customer_id": types.Integer(),
        "units": types.Integer(),
        "price": types.Float(),
        'sales': types.Float()
    }
)

print('Exportado correctamente')