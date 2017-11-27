import numpy as np
import pandas as pd
import math
def update_dataframe(df, PSUV, MUD):
    df['Abstencion_%'] = df['ABSTENCION'] / df['ELECTORES INSCRITOS']

    try:
        df['PSUV_%'] = df[PSUV] / df['VOTOS ESCRUTADOS']
    except ZeroDivisionError:
        df['PSUV_%'] = 0

    try:
        df['MUD_%'] = df[MUD] / df['VOTOS ESCRUTADOS']
    except ZeroDivisionError:
        df['MUD_%'] = 0

    df['PSUV_N'] = df[PSUV]
    df['MUD_N'] = df[MUD]

    df['centro'] = df['parroquia']+df['centro']

    df['rescaled_N'] =  math.log((df['VOTOS VALIDOS'].sum()-df[PSUV].sum())/float(df[PSUV].sum()))

    unique_estados = np.unique(df['estado'])
    unique_parroquias = np.unique(df['parroquia'])
    unique_centros = np.unique(df['centro'])
    unique_municipios = np.unique(df['municipio'])

    centro_average = {}
    centro_average_abstention = {}
    for i in unique_centros:
        centro = df[df['centro'] == i]
        try:
            average = centro[PSUV].sum() / float(centro['VOTOS ESCRUTADOS'].sum())

        except ZeroDivisionError:
            average = 0


        centro_average[i] = average
        centro_average_abstention[i] = centro['VOTOS ESCRUTADOS'].sum()/float(centro['ELECTORES INSCRITOS'].sum())

    parroquia_average = {}
    parroquia_average_abstention = {}
    for i in unique_parroquias:
        parroquia = df[df['parroquia'] == i]
        try:
            average = parroquia[PSUV].sum() / float(parroquia['VOTOS ESCRUTADOS'].sum())
        except ZeroDivisionError:
            average = 0

        parroquia_average[i] = average
        parroquia_average_abstention[i] = parroquia['VOTOS ESCRUTADOS'].sum()/float(parroquia['ELECTORES INSCRITOS'].sum())

    municipio_average = {}
    municipio_average_abstention = {}
    for i in unique_municipios:
        municipio = df[df['municipio'] == i]
        try:
            average = municipio[PSUV].sum() / float(municipio['VOTOS ESCRUTADOS'].sum())
        except ZeroDivisionError:
            average = 0

        municipio_average[i] = average
        municipio_average_abstention[i] = municipio['VOTOS ESCRUTADOS'].sum()/float(municipio['ELECTORES INSCRITOS'].sum())


    estado_average = {}
    estado_average_abstention = {}

    for i in unique_estados:
        estado = df[df['estado'] == i]
        try:
            average = estado[PSUV].sum() / float(estado['VOTOS ESCRUTADOS'].sum())
        except ZeroDivisionError:
            average = 0

        estado_average[i] = average
        estado_average_abstention[i] =  estado['VOTOS ESCRUTADOS'].sum()/float(estado['ELECTORES INSCRITOS'].sum())


    parroquia_residual = []
    municipio_residual = []
    centro_residual = []
    estado_residual = []

    abstention_parroquia_residual = []
    abstention_municipio_residual = []
    abstention_centro_residual = []
    abstention_estado_residual = []


    for i in range(0,df.shape[0]):
        psuv_val = df['PSUV_%'].iloc[i]
        centro = df['centro'].iloc[i]
        municipio = df['municipio'].iloc[i]
        estado =  df['estado'].iloc[i]
        parroquia =  df['parroquia'].iloc[i]
        abstention_val = df['Abstencion_%'].iloc[i]


        parroquia_residual.append((1-(psuv_val/float(parroquia_average[parroquia]))))
        municipio_residual.append(1-(psuv_val/float(municipio_average[municipio])))
        centro_residual.append(1-(psuv_val/float(centro_average[centro])))
        estado_residual.append(1-(psuv_val/float(estado_average[estado])))

        abstention_parroquia_residual.append((1 - (abstention_val / float(parroquia_average_abstention[parroquia]))))
        abstention_municipio_residual.append(1 - (abstention_val / float(municipio_average_abstention[municipio])))

        try:
            abstention_centro_residual.append(1 - (abstention_val / float(centro_average_abstention[centro])))
        except ZeroDivisionError:
            abstention_centro_residual.append(0)

        abstention_estado_residual.append(1 - (abstention_val / float(estado_average_abstention[estado])))

    df['parroquia_residual']=pd.Series(parroquia_residual)
    df['municipio_residual']=pd.Series(municipio_residual)
    df['centro_residual']=pd.Series(centro_residual)
    df['estado_residual']=pd.Series(estado_residual)

    df['abstention_parroquia_residual'] = pd.Series(abstention_parroquia_residual)
    df['abstention_municipio_residual'] = pd.Series(abstention_municipio_residual)
    df['abstention_centro_residual'] = pd.Series(abstention_centro_residual)
    df['abstention_estado_residual'] = pd.Series(abstention_estado_residual)


    df['parroquia_standarised_residual'] = df['parroquia_residual']/df['parroquia_residual'].std()
    df['municipio_standarised_residual'] =  df['municipio_residual']/df['municipio_residual'].std()
    df['centro_standarised_residual'] = df['centro_residual']/df[df['centro_residual']!=0]['centro_residual'].std()
    df['estado_standarised_residual'] = df['estado_residual']/df['estado_residual'].std()

    df['parroquia_standarised_residual_abstention'] = df['abstention_parroquia_residual']/df['abstention_parroquia_residual'].std()
    df['municipio_standarised_residual_abstention'] =  df['abstention_municipio_residual']/df['abstention_municipio_residual'].std()
    df['centro_standarised_residual_abstention'] = df['abstention_centro_residual']/df[df['abstention_centro_residual']!=0]['abstention_centro_residual'].std()
    df['estado_standarised_residual_abstention'] = df['abstention_estado_residual']/df['abstention_estado_residual'].std()


    return df




