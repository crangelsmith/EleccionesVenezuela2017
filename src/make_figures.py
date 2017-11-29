import seaborn as sns
import matplotlib.pyplot as plt
import json
import numpy as np


def do_SR_mesa(df_out):
    sns.distplot(df_out[df_out['centro_standardised_residual'] != 0]['parroquia_standardised_residual'],
                 hist_kws={'weights': df_out[df_out['centro_standardised_residual'] != 0]['VOTOS VALIDOS']},
                 kde=True, label="centro == 1 mesa")

    sns.distplot(df_out[df_out['centro_standardised_residual'] == 0]['parroquia_standardised_residual'],
                 hist_kws={'weights': df_out[df_out['centro_standardised_residual'] == 0]['VOTOS VALIDOS']},
                 kde=True, label="centro > 1 mesa")

    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    print(' === centros with only 1 mesa === ')
    print('mean:  %s' % df_out[df_out['centro_standardised_residual'] == 0]['parroquia_standardised_residual'].mean())
    print('std: %s' % df_out[df_out['centro_standardised_residual'] == 0]['parroquia_standardised_residual'].std())

    print('PSUV N Votes: %s' % df_out[df_out['centro_standardised_residual'] == 0]['PSUV_N'].sum())
    print('MUD N Votes: %s' % df_out[df_out['centro_standardised_residual'] == 0]['MUD_N'].sum())

    print(' === centros with more than 1 mesa === ')
    print('mean: %s' % df_out[df_out['centro_standardised_residual'] != 0]['parroquia_standardised_residual'].mean())
    print('std: %s' % df_out[df_out['centro_standardised_residual'] != 0]['parroquia_standardised_residual'].std())
    print('PSUV N Votes: %s' % df_out[df_out['centro_standardised_residual'] != 0]['PSUV_N'].sum())
    print('MUD N Votes: %s' % df_out[df_out['centro_standardised_residual'] != 0]['MUD_N'].sum())


def do_SR(df_out):
    sns.distplot(df_out['parroquia_standardised_residual'], kde=False,
                 hist_kws={'weights': df_out['VOTOS VALIDOS']})

    print(' === inclusive data (all mesas) === ')
    print('mean: %s' % df_out['parroquia_standardised_residual'].mean())
    print('std: %s ' % df_out['parroquia_standardised_residual'].std())


def do_cumulative(df):

    df['turnout'] = 1 - df['Abstencion_%']

    sorted_df = df.sort_values(by='turnout')

    total_psuv = df['PSUV_N'].sum()

    sorted_df['PSUV_cumsum'] = (sorted_df['PSUV_N'].cumsum() / total_psuv) * 100
    sorted_df = sorted_df.reset_index(drop=True)

    plt.xlabel('Voter turnout %')
    plt.ylabel('Cumulative Vote for PSUV %')

    turnout = list(sorted_df['turnout'])
    turnout_50 = np.percentile(turnout, 50)
    turnout_95 = np.percentile(turnout, 95)

    psuv_cumsum = list(sorted_df['PSUV_cumsum'])

    plt.plot(turnout, psuv_cumsum)
    plt.axvline(x=turnout_50)
    plt.axvline(x=turnout_95)
