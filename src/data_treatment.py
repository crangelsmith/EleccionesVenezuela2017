import numpy as np
import pandas as pd

def update_dataframe(df, PSUV, MUD):
    df['Abstencion_%'] = df['ABSTENCION'] / df['ELECTORES INSCRITOS']
    df['PSUV_%'] = df[PSUV] / df['VOTOS ESCRUTADOS']
    df['PSUV_N'] = df[PSUV]
    df['MUD_%'] = df[MUD] / df['VOTOS ESCRUTADOS']
    df['MUD_N'] = df[MUD]

    unique_estados = np.unique(df['estado'])
    unique_parroquias = np.unique(df['parroquia'])
    unique_centros = np.unique(df['centro'])
    unique_municipios = np.unique(df['municipio'])

    centro_average = {}
    for i in unique_centros:
        centro = df[df['centro'] == i]
        try:
            average = centro[PSUV].sum() / float(centro['VOTOS ESCRUTADOS'].sum())
        except ZeroDivisionError:
            average = 0


        centro_average[i] = average

    parroquia_average = {}
    for i in unique_parroquias:
        parroquia = df[df['parroquia'] == i]
        try:
            average = parroquia[PSUV].sum() / float(parroquia['VOTOS ESCRUTADOS'].sum())
        except ZeroDivisionError:
            average = 0

        parroquia_average[i] = average

    municipio_average = {}
    for i in unique_municipios:
        municipio = df[df['municipio'] == i]
        try:
            average = municipio[PSUV].sum() / float(municipio['VOTOS ESCRUTADOS'].sum())
        except ZeroDivisionError:
            average = 0

        municipio_average[i] = average

    estado_average = {}
    for i in unique_estados:
        estado = df[df['estado'] == i]
        try:
            average = estado[PSUV].sum() / float(estado['VOTOS ESCRUTADOS'].sum())
        except ZeroDivisionError:
            average = 0

        estado_average[i] = average

    parroquia_residual = []
    municipio_residual = []
    centro_residual = []
    estado_residual = []

    for i in range(0,df.shape[0]):
        psuv_val = df['PSUV_%'].iloc[i]
        centro = df['centro'].iloc[i]
        municipio = df['municipio'].iloc[i]
        estado =  df['estado'].iloc[i]
        parroquia =  df['parroquia'].iloc[i]

        parroquia_residual.append((1-(psuv_val/float(parroquia_average[parroquia]))))
        municipio_residual.append(1-(psuv_val/float(municipio_average[municipio])))
        centro_residual.append(1-(psuv_val/float(centro_average[centro])))
        estado_residual.append(1-(psuv_val/float(estado_average[estado])))

    df['parroquia_residual']=pd.Series(parroquia_residual)
    df['municipio_residual']=pd.Series(municipio_residual)
    df['centro_residual']=pd.Series(centro_residual)
    df['estado_residual']=pd.Series(estado_residual)

    df['parroquia_standarised_residual'] = df['parroquia_residual']/df['parroquia_residual'].var()
    df['municipio_standarised_residual'] =  df['municipio_residual']/df['municipio_residual'].var()
    df['centro_standarised_residual'] = df['centro_residual']/df['centro_residual'].var()
    df['estado_standarised_residual'] = df['estado_residual']/df['estado_residual'].var()


    return df




