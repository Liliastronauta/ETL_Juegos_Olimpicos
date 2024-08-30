import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import os 
 

#Path de mi archivo 
file = "all_data.csv"

#Lectura de datos
df_olimpycs = pd.read_csv(file)
print(df_olimpycs)

#Análisis exploratorio de datos previo a su transformación:
def exploratory_analysis(dataframes):

    separador = "-"*15
    print(f"{separador } Información {separador} ")
    print(dataframes.info())

    print(f"{separador } Descripción {separador} ")
    print(dataframes.describe())

exploratory_analysis(df_olimpycs)


#Transformación de datos.
def transform_data(df):

    #Eliminar Columnas que no queremos:
    df = df.drop('long2', axis = 1)

    #Renombrar columnas:
    df = df.rename(columns={
        'Unnamed: 0': 'id',
        'short': 'Abreviatura',
        'long': 'Pais',
        'gold': 'Oro',
        'silver': 'Plata',
        'bronze': 'Bronce',
        'total': 'Total',
        'yr': 'Año'
    })

    #Colocar a la columna nueva id como el indice:
    df = df.set_index('id')

    #Reemplazar los guiones por ceros.
    df['Oro'] = df['Oro'].replace('-','0')
    df['Plata'] = df['Plata'].replace('-','0')
    df['Bronce'] = df['Bronce'].replace('-','0')

    #Convertir columnas a tipo entero
    df['Oro'] = df['Oro'].astype(int)
    df['Plata'] = df['Plata'].astype(int)
    df['Bronce'] = df['Bronce'].astype(int)
    
    #Separar los elementos de la columna año en dos columnas: ciudad y año.
    df[['Ciudad', 'Año']] = df.Año.str.rsplit(pat='-', n=1, expand = True)

    #Eliminar datos inconsistentes.
    df = df.drop(df[df.Año < '1960'].index)


    print(df.info())
    print(df)
    return df


df_tranform = transform_data(df_olimpycs)

#Tenemos mezclados los datos de los juegos de verano e invierno asi que los separamos en dos dataframes
#diferentes.

verano_df = df_tranform[df_tranform['Ciudad'].isin(['athens', 'london', 'los-angeles', 'rome','tokyo', 'mexico-city','munich',
                                                    'montreal', 'moscow', 'seoul', 'barcelona', 'atlanta','sydney', 'beijing', 'rio'])]

invierno_df = df_tranform[df_tranform['Ciudad'].isin(['squaw-valley','innsbruck', 'grenoble', 'sapporo', 'sarajevo', 'calgary',
                                                      'albertville', 'lillehammer', 'nagano', 'salt-lake-city', 'turin',
                                                      'vancouver', 'sochi', 'pyeongchang', 'lake-placid' ])] 

#Reseteamos sus indices.
verano_df.reset_index(drop=True, inplace=True)
verano_df.index = verano_df.index+1

invierno_df.reset_index(drop=True, inplace=True)
invierno_df.index = invierno_df.index+1


print(verano_df)
print(invierno_df)

#Queremos un nuevo dataframe que contenga solo los datos de los paises que han sido sede.
verano_filt = verano_df[verano_df['Abreviatura'].isin(['ITA', 'JPN', 'MEX', 'GER', 'FRG', 'GDR', 'CAN', 'RUS', 
                                                       'URS', 'USA', 'KOR', 'ESP', 'AUS','GRE', 'CHN', 'GBR', 'BRA' ])]

invierno_filt = invierno_df[invierno_df['Abreviatura'].isin(['USA', 'AUT', 'FRA', 'JPN', 'YUG', 'CAN', 'NOR', 'ITA', 'RUS', 'KOR'])]

#Reseteamos sus indices.
verano_filt.reset_index(drop=True, inplace=True)
verano_filt.index = verano_filt.index+1

invierno_filt.reset_index(drop=True, inplace=True)
invierno_filt.index = invierno_filt.index+1

print(verano_filt)
print(invierno_filt)

#Análisis exploratorio de datos (graficas) de los dos dataframes despues de su transformación:
def graficas(dframe):
    #Medallas ganadas desde 1960 hasta 2018
    dframe.plot(kind='line', x='Año', y= 'Total')
    plt.title('Evolución de medallas ganadas a lo largo del tiempo')
    plt.ylabel('Número de medallas')
    plt.show()

graficas(verano_filt)

#Cargar datos.

def load_final_data(df, output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    df.to_csv(output_path, index=False)

load_final_data(verano_filt, 'datos_procesados/verano.csv')
load_final_data(invierno_filt, 'datos_procesados/invierno.csv')

