import urllib
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy import types

def cargar_datos(ruta):
    return pd.read_csv(ruta)

def conectar_sql():
    driver='ODBC Driver 17 for SQL Server'
    server='(local)\\SQLEXPRESS'
    database='consumer_analytics'

    connection_str= (
        f'DRIVER={{{driver}}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'Trusted_connection=yes;'
    )

    params= urllib.parse.quote_plus(connection_str)
    engine= sa.create_engine(f'mssql+pyodbc:///?odbc_connect={params}')

    print('Conexión exitosa a SQL!')

    return engine

def cargar_a_sql(df,engine):
    df.to_sql(
        name='consumer_data',
        con= engine,
        schema= 'dbo',
        if_exists='replace',
        index= False,
        dtype= {
            'customer_id': types.Integer(),
            'units': types.Integer(),
            'price': types.Float(),
            'sales': types.Float()
        }
    )

    print('Datos cargados exitosamente.')

def main():
    ruta='PORTAFOLIO_CONSUMER_ANALYTICS/Data/consumer_clean.csv'

    df= cargar_datos(ruta)

    engine= conectar_sql()
    cargar_a_sql(df, engine)

if __name__ == '__main__':
    main()
