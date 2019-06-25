def plot_fig1b(data_df):

  subdata_df = data_df[['TSOD','TSNO']].iloc[:]
  n_comp, eig_orig, eig_rand = parallel_analysis(subdata_df.T,
                                                 output_eig=True,
                                                 method='shuffle')
  df = pd.DataFrame()
  df['original'] = np.log(eig_orig)
  df['shuffled (95 %)'] = np.log(np.percentile(eig_rand, 95, axis=0))
  df['component number'] = np.arange(len(df)) + 1
  df = df[df['component number'] <= 15]
  df = df.melt(id_vars='component number', value_vars=df.columns[:-1],
               value_name='log eigenvalue', var_name='type')
  
  with sns.plotting_context('notebook'):
    fig, ax = plt.subplots(figsize=(4,3))
    sns.pointplot(data   = df,
                  x      = 'component number',
                  y      = 'log eigenvalue',
                  hue    = 'type',
                  ax     = ax,
                  palette = ['xkcd:emerald','xkcd:pale olive green'],
                  legend  = False)
    ax.legend(frameon=False)
    sns.despine()
    fig.tight_layout()
    if in_ipython():
      fig.show()
      fig.savefig('tmp.png')
    
if __name__ == '__main__':
  plot_fig1b(data_df)
