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
    plt.axvline(x=turnout_50,color='red')
    plt.axvline(x=turnout_95,linestyle='dashed')


def do_2dplot(df_out, varX,varY):

    i = round(df_out.shape[0]/20.0)
    print i

    plt.hist2d(df_out[varX], df_out[varY], weights=df_out['VOTOS VALIDOS'], bins=i, cmap=plt.cm.jet)
    plt.xlabel(varX)
    plt.ylabel(varY)
    plt.colorbar()


def do_all(df_out):
    from matplotlib.ticker import NullFormatter  # useful for `logit` scale

    plt.figure(1)
    plt.subplot(221)
    do_SR(df_out)
    plt.subplot(223)
    do_SR_mesa(df_out)
    plt.subplot(222)
    do_cumulative(df_out)
    print 'Inclusive'
    plt.subplot(224)
    do_2dplot(df_out, 'turnout', "PSUV_%")

    df_1 = df_out[df_out['centro_standardised_residual'] == 0]
    df_1plus = df_out[df_out['centro_standardised_residual'] != 0]
    print 'Only 1 table'
    plt.figure(2)
    plt.subplot(2, 1, 1)
    do_2dplot(df_1, 'turnout', "PSUV_%")
    print 'More than 1 table'
    plt.subplot(2, 1, 2)
    do_2dplot(df_1plus, 'turnout', "PSUV_%")
    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                        wspace=0.35)




