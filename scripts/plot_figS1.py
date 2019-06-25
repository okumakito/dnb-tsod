def plot_figS1(data_df):
  n_comp = 8

  pca        = PCA(n_components=n_comp)
  subdata_df = data_df.loc[:,['TSOD','TSNO']].iloc[:]
  df  = pd.DataFrame(pca.fit_transform(subdata_df.T),
                     columns=['PC'+str(i+1) for i in range(n_comp)])
  df = -df   # reverse drections for consistency with fig2.
  print('explained variance ratios (%) = ',
        np.round(100*pca.explained_variance_ratio_,1))
  
  color_df = subdata_df.T.reset_index()[['condition','week']]

  color1_sr  = color_df['condition'].replace(dict(TSOD='xkcd:windows blue',
                                                  TSNO='xkcd:amber'))
  pal_arr = np.array(sns.color_palette('Spectral_r', 5))
  color2_arr = pal_arr[color_df['week'].astype(int)-3]

  with sns.plotting_context('notebook'):
    g = sns.PairGrid(data=df, vars=df.columns[:n_comp], size=1)
    g.map_upper(plt.scatter, color=color1_sr, marker='.')
    g.map_diag(sns.kdeplot, lw=3, legend=False, shade=True, color='k')
    g.map_lower(plt.scatter, color=color2_arr, marker='.')

    #[ax.set_ylim((0,0.04))for ax in g.diag_axes]
    max_val = df.abs().max().max() * 1.05
    for ax in g.axes.flatten():
      ax.set_xlim((-max_val, max_val))
      ax.set_ylim((-max_val, max_val))

    g.fig.subplots_adjust(wspace=0.1, hspace=0.1)
    if in_ipython():
      g.fig.show()
      g.fig.savefig('tmp.png')

if __name__ == '__main__':
  plot_figS1(data_df)
