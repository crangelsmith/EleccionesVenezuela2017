import numpy as np
import pandas as pd
import math


def add_residual_to_df(df, level, residual, abstention_residual):
    resid_name = level+'_residual'
    abstention_resid = 'abstention_'+level+'_residual'
    df[resid_name]=pd.Series(residual)
    df[abstention_resid] = pd.Series(abstention_residual)
    df[level+'_standardised_residual'] = df[resid_name] / df[resid_name].std()
    df[level+'_standardised_residual_abstention'] = df[abstention_resid] / df[abstention_resid].std()

    return df


def update_dataframe(df,PSUV,MUD):
    df['Abstencion_%'] = df['ABSTENCION'] / df['ELECTORES INSCRITOS']
    df['turnout'] = 1 - df['Abstencion_%']
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
        if centro['VOTOS ESCRUTADOS'].sum()!=0:
            average = centro[PSUV].sum() / float(centro['VOTOS ESCRUTADOS'].sum())

        else:
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

    for i in range(len(df)):
        psuv_val = df['PSUV_%'].iloc[i]
        centro = df['centro'].iloc[i]
        municipio = df['municipio'].iloc[i]
        estado =  df['estado'].iloc[i]
        parroquia =  df['parroquia'].iloc[i]
        abstention_val = df['Abstencion_%'].iloc[i]


        parroquia_residual.append((1-(psuv_val/float(parroquia_average[parroquia]))))
        municipio_residual.append(1-(psuv_val/float(municipio_average[municipio])))

        if float(centro_average[centro])!=0:
            centro_residual.append(1-(psuv_val/float(centro_average[centro])))
        else:
            centro_residual.append(1)

        estado_residual.append(1-(psuv_val/float(estado_average[estado])))

        abstention_parroquia_residual.append((1 - (abstention_val / float(parroquia_average_abstention[parroquia]))))
        abstention_municipio_residual.append(1 - (abstention_val / float(municipio_average_abstention[municipio])))

        if centro_average_abstention[centro]!=0:
            abstention_centro_residual.append(1 - (abstention_val / float(centro_average_abstention[centro])))
        else:
            abstention_centro_residual.append(1)

        abstention_estado_residual.append(1 - (abstention_val / float(estado_average_abstention[estado])))

    add_residual_to_df(df, 'centro', centro_residual, abstention_centro_residual)
    add_residual_to_df(df, 'parroquia', parroquia_residual, abstention_parroquia_residual)
    add_residual_to_df(df, 'municipio', municipio_residual, abstention_municipio_residual)
    add_residual_to_df(df, 'estado', estado_residual, abstention_estado_residual)

    return df


def update_all(df):

    unique_estados = np.unique(df['estado'])

    df_estados = []
    for i in unique_estados:
        print i
        estado = df[df['estado'] == i]
        PSUV = PSUV_MUD_dic[i][0]
        MUD = PSUV_MUD_dic[i][1]
        df_out = update_dataframe(estado,PSUV,MUD)
        df_estados.append(df_out)


    df_final = pd.concat(df_estados)

    return df_final



PSUV_MUD_dic={
   "EDO. ANZOATEGUI":[
      "ARISTOBULO IZTURIZ",
      "ANTONIO BARRETO SIRA"
   ],
   "EDO. APURE":[
      "RAMON CARRIZALEZ",
      "JOSE MONTILLA"
   ],
   "EDO. ARAGUA":[
      "RODOLFO MARCO TORRES",
      "ISMAEL GARCIA"
   ],
   "EDO. BARINAS":[
      "ARGENIS CHAVEZ",
      "FREDDY SUPERLANO"
   ],
   "EDO. BOLIVAR":[
      "JUSTO NOGUERA PIETRI",
      "ANDRES VELASQUEZ"
   ],
   "EDO. CARABOBO":[
      "RAFAEL LACAVA",
      "ALEJANDRO FEO LA CRUZ"
   ],
   "EDO. COJEDES":[
      "MARGAUD GODOY",
      "ALBERTO GALINDEZ"
   ],
   "EDO. FALCON":[
      "VICTOR CLARK",
      "ELIEZER SIRIT"
   ],
   "EDO. GUARICO":[
      "JOSE VASQUEZ",
      "PEDRO LORETO"
   ],
   "EDO. LARA":[
      "CARMEN MELENDEZ",
      "HENRI FALCON"
   ],
   "EDO. MERIDA":[
      "JEHYSON GUZMAN",
      "RAMON GUEVARA"
   ],
   "EDO. MIRANDA":[
      "HECTOR RODRIGUEZ",
      "CARLOS OCARIZ"
   ],
   "EDO. MONAGAS":[
      "YELITZE SANTAELLA",
      "GUILLERMO CALL"
   ],
   "EDO. NVA.ESPARTA":[
      "CARLOS MATA FIGUEROA",
      "ALFREDO DIAZ"
   ],
   "EDO. PORTUGUESA":[
      "MARIA BEATRIZ MARTINEZ",
      "RAFAEL CALLES"
   ],
   "EDO. SUCRE":[
      "EDWIN ROJAS",
      "ROBERT ALCALA"
   ],
   "EDO. TACHIRA":[
      "JOSE VIELMA MORA",
      "LAIDY GOMEZ"
   ],
   "EDO. TRUJILLO":[
      "HENRY RANGEL SILVA",
      "CARLOS GONZALEZ"
   ],
   "EDO. YARACUY":[
      "JULIO LEON HEREDIA",
      "LUIS PARRA"
   ],
   "EDO. ZULIA":[
      "ARIAS CARDENAS",
      "JUAN PABLO GUANIPA"
   ],
   "EDO. AMAZONAS":[
      "MIGUEL RODRIGUEZ",
      "BERNABE GUTIERREZ"
   ],
   "EDO. DELTA AMACURO":[
      "LIZETA HERNANDEZ",
      "LARISSA GONZALEZ"
   ],
   "EDO. VARGAS":[
      "JORGE GARCIA CARNEIRO",
      "JOSE MANUEL OLIVARES"
   ]
}
