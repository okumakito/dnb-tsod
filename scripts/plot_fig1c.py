def plot_fig1c(data_df):

  pca        = PCA(n_components=2)
  subdata_df = data_df.loc[:,['TSOD','TSNO']]
  trans_arr  = pca.fit_transform(subdata_df.T)
  trans_arr  = trans_arr * [-1, -1]  # reverse PC1 and PC2 directions

  x_label, y_label = ['PC{:d} ({:.1f} %)'.format(i+1, 100 * v)
                      for i, v in enumerate(pca.explained_variance_ratio_)]
  df  = pd.DataFrame(trans_arr,
                     index=subdata_df.columns, 
                     columns=[x_label, y_label]).reset_index()
  df1 = df[df['condition'] == 'TSOD']
  df2 = df[df['condition'] == 'TSNO'].set_index('week')

  with sns.plotting_context('notebook'), \
       sns.color_palette('Spectral_r', 5):

    # TSOD
    scatter_kws = {'edgecolors':'0.2', 's':100, 'linewidths':1}
    g = sns.lmplot(data        = df1,
                   x           = x_label,
                   y           = y_label,
                   hue         = 'week',
                   fit_reg     = False,
                   markers     = 'o',
                   legend      = False,
                   size        = 4,
                   scatter_kws = scatter_kws)
    g.ax.legend(loc='lower right',
                title='week',
                facecolor='xkcd:light grey')

    # TSNO
    g.ax.set_prop_cycle(None)
    scatter_kws['s'] = 70
    for week in list('34567'):
      g.ax.scatter(df2.loc[week, x_label],
                   df2.loc[week, y_label],
                   marker='D',
                   **scatter_kws)

    if in_ipython():
      g.fig.show()
      g.fig.savefig('tmp.png')

if __name__ == '__main__':
  plot_fig1c(data_df)
