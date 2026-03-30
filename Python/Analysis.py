
import pandas as pd

df= pd.read_csv("PORTAFOLIO_CONSUMER_ANALYTICS/Data/consumer_data.csv")

print(df.describe())
# Penetración de los productos

clientes_por_producto= (
    df
    .groupby('product')['customer_id']
    .nunique()
    .reset_index()
    .rename(columns={'customer_id':'clientes_unicos'})
)

print(f'Los clientes que compraron un producto unico fueron: \n\n{clientes_por_producto}\n')

total_clientes= (
    df['customer_id']
    .nunique()
)

print(f'El total de clientes unicos: {total_clientes}\n')

 # AQUI CREAMOS UNA TABLA TEMPORAL / RESUMEN - IMPORTANTE se usa la variable CLIENTES_POR_PRODUCTO porque
 # crearemos una tabla temporal dentro de este "DF"

clientes_por_producto['penetracion_%'] = (
    clientes_por_producto['clientes_unicos'] / total_clientes 
) * 100

print(clientes_por_producto,'\n')

# Vamos a calcular la frecuencia con la que compran los clientes

'''
WITH clientes AS (
    SELECT
        customer_id,
        count(*) AS total clientes
    FROM
    GROUP BY customer_id 
)
SELECT
    customer_id,
    AVG(total clientes) AS Promedio por cliente
FROM clientes
;
'''

frecuencia= (
    df.groupby('customer_id')
    .size()
    .mean()
)

print(f'La frecuencia con la que se compran un promedio de clientes es de: {frecuencia}\n')

# Esta es la encadenación mas eficiente a la hora de agrupar por columnas, podemos hacer 
# todo desde un mismo parrafo de codigo

"""resumen_final = (df.groupby('customer_id')
                 .agg({'sales': ['sum', 'skew'], 'profit': 'sum'})
                 .set_axis(['sales_total', 'sales_skew', 'profit_total'], axis=1) # Renombrar directo
                 .reset_index()
                 .sort_values(by='sales_total', ascending=False))

print(resumen_final.head())"""

# Gasto promedio por cliente y en general.
gasto_cliente= (
    df
    .groupby('customer_id')['sales']
    .sum()
    .reset_index()
    .rename(columns={'sales':'Total_Gasto'})
)

gasto_promedio= gasto_cliente['Total_Gasto'].mean() # Siempre debemos ser especificos a que columna se hara la agregación, si dejamos toda la tabla puede haber un erro grande.

print(f'El promedio Global de los clientes es: {gasto_promedio}','\n')

# Outliers con Z-Core

# 1. Media y Desviación
mean_sales= df['sales'].mean()
std_sales= df['sales'].std()

# 2. Calculo con Z_SCORE
df['z_score']= (df['sales']- mean_sales)/ std_sales

# 3. Detectar OUTLIERS
outliers_z= df[df['z_score'].abs()> 3]

print('Outliers con Z_Score: ', outliers_z.shape[0])

# Metodo IQR mas fiable

Q1= df['sales'].quantile(0.25)
Q3= df['sales'].quantile(0.75)

IQR= Q3 - Q1

lower= Q1 - 1.5 * IQR
upper= Q3 + 1.5 * IQR

print(df.shape[0])

outliers_iqr= df[(df['sales'] < lower) | (df['sales'] > upper)]

print(lower)
print(upper)
print(f'Outliers con IQR: {outliers_iqr.shape[0]}\n')

df['sales'].skew()

"""gasto_cliente1= (
    df.groupby('customer_id')['sales'].sum()
)
threshold= gasto_cliente1.quantile(0.95)

cliente_vip= gasto_cliente1[gasto_cliente1>threshold] 

print(cliente_vip)""" # Para crear una segmentación de cliente VIP

df_clean= df[(df['sales']>= lower) & (df['sales']<= upper)]

df_clean.to_csv('PORTAFOLIO_CONSUMER_ANALYTICS/Data/consumer_clean.csv',index=False)

print(f'Tabla sucia: {df.shape[0]}')
print(f'Tabla limpia: {df_clean.shape[0]}')
print(df_clean.describe())




