import seaborn as sns
import matplotlib.pyplot as plt


def do_SR_mesa(df_out_MONAGAS):
    sns.distplot(df_out_MONAGAS[df_out_MONAGAS['centro_standarised_residual'] != 0]['parroquia_standarised_residual'],
                 hist_kws={
                     'weights': df_out_MONAGAS[df_out_MONAGAS['centro_standarised_residual'] != 0]['VOTOS VALIDOS']},
                 kde=True, label="centro == 1 mesa");
    sns.distplot(df_out_MONAGAS[df_out_MONAGAS['centro_standarised_residual'] == 0]['parroquia_standarised_residual'],
                 hist_kws={
                     'weights': df_out_MONAGAS[df_out_MONAGAS['centro_standarised_residual'] == 0]['VOTOS VALIDOS']},
                 kde=True, label="centro > 1 mesa");
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    print 'centros with only 1 mesa:'
    print 'mean ', df_out_MONAGAS[df_out_MONAGAS['centro_standarised_residual'] == 0][
        'parroquia_standarised_residual'].mean()
    print 'std ', df_out_MONAGAS[df_out_MONAGAS['centro_standarised_residual'] == 0][
        'parroquia_standarised_residual'].std()
    print

    print 'centros with more than 1 mesa:'
    print 'mean', df_out_MONAGAS[df_out_MONAGAS['centro_standarised_residual'] != 0][
        'parroquia_standarised_residual'].mean()
    print 'std', df_out_MONAGAS[df_out_MONAGAS['centro_standarised_residual'] != 0][
        'parroquia_standarised_residual'].std()


def do_SR(df_out_MONAGAS):
    sns.distplot(df_out_MONAGAS['parroquia_standarised_residual'], kde=False,
                 hist_kws={'weights': df_out_MONAGAS['VOTOS VALIDOS']});

    print 'inclusive data (all mesas)'
    print 'mean ', df_out_MONAGAS['parroquia_standarised_residual'].mean()
    print 'std ', df_out_MONAGAS['parroquia_standarised_residual'].std()