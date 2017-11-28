import seaborn as sns
import matplotlib.pyplot as plt


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
    
#def do_cumulative(df_out):
