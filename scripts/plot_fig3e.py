import warnings
warnings.filterwarnings('ignore', 'This figure includes Axes that are not compatible')

def plot_fig3e(pos_df, data_df):
  cmap = 'YlOrRd' # 'RdYlGn_r', 'PiYG_r'

  idx = pos_df.sort_values(by='type').index
  std_df = data_df.loc[idx, 'TSOD'].groupby(axis=1,level=0).std()

  # descritization
  cutoff = 2.0  # above this will be assigned the same color
  n_pal  = 10
  std_df = (std_df / cutoff * n_pal // 1).astype(int)
  std_df[std_df >= n_pal] = n_pal - 1

  std_df = pd.concat([std_df, pos_df], axis=1).reset_index()

  df = pd.melt(std_df,
               id_vars=['gene_symbol', 'x', 'y' , 'type'],
               value_vars=list('34567'),
               var_name='week',
               value_name='std')
  
  with sns.axes_style('white'), sns.plotting_context('talk'):
    scatter_kws = {'s':30, 'linewidths':0}
    g = sns.lmplot(data    = df,
                   x       = 'x',
                   y       = 'y',
                   hue     = 'std',
                   col     = 'week',
                   col_wrap = 3,
                   fit_reg = False,
                   legend  = False,
                   size    = 2.5,
                   markers = '.',
                   palette = sns.color_palette(cmap, n_pal),
                   scatter_kws=scatter_kws)
    for ax in g.axes:
      sns.despine(bottom=True, left=True)
      ax.set_xlabel('')
      ax.set_ylabel('')
      ax.set_xticks([])
      ax.set_yticks([])
    g.set_titles('{col_name} weeks')

    # legend
    fig_null, ax_null = plt.subplots()
    ax5 = g.fig.add_axes([0.68,0.2,0.3,0.1])
    sns.heatmap(np.linspace(0, cutoff, 100).reshape(-1,1),
                cmap = cmap,
                cbar_ax=ax5,
                ax=ax_null,
                cbar_kws={'label':'standard deviation',
                          'orientation':'horizontal'})
    
    g.fig.tight_layout(pad=0, h_pad=2)
    if in_ipython():
      g.fig.show()
      g.fig.savefig('tmp.png')
    else:
      plt.close(fig_null)


if __name__ == '__main__':
  plot_fig3e(pos_df, data_df)
