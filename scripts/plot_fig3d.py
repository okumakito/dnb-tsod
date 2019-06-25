def calculate_tsne_pos(clust_sr, dnb_idx, data_df):

  union_arr   = np.union1d(clust_sr.index, dnb_idx)
  subdata_df  = data_df.loc[union_arr, ('TSOD','5')]
  subdata2_df = data_df.loc[union_arr, ('TSNO','5')]

  tsne = TSNE(n_components=2, random_state=0, metric='precomputed',
              verbose=1, perplexity=100, early_exaggeration=10.0)
  
  pos_df = pd.DataFrame(tsne.fit_transform(1 - subdata_df.T.corr().abs() +
                                          subdata2_df.T.corr().abs()),
                        index=subdata_df.index, columns=['x', 'y'])
  pos_df['type'] = 'DEG'
  pos_df.loc[dnb_idx, 'type'] = 'DNB'
  return pos_df

def load_tsne_pos():
  file_name = '../data/tsne_pos.tsv'
  pos_df = pd.read_csv(file_name, sep='\t', index_col=0)
  return pos_df

def plot_fig3d(pos_df):

  pos2_df = pos_df.copy()
  pos2_df.columns = ['t-SNE axis 1', 't-SNE axis 2', 'type']

  with sns.plotting_context('talk'):
    scatter_kws = {'s':30, 'linewidths':0}
    g = sns.lmplot(data    = pos2_df,
                   x       = 't-SNE axis 1',
                   y       = 't-SNE axis 2',
                   hue     = 'type',
                   fit_reg = False,
                   markers = ['o', 'o'],
                   legend  = False,
                   #palette = ['xkcd:greenish grey','xkcd:dark aqua'],
                   #palette = ['xkcd:cool grey','xkcd:rose red'],
                   palette = ['xkcd:beige','xkcd:red orange'],
                   scatter_kws=scatter_kws)
    leg = g.ax.legend(loc='lower left', title=None, markerscale=2.5)
    leg.get_frame().set_linewidth(3)
    min_val = min(g.ax.get_xlim()[0], g.ax.get_ylim()[0])
    max_val = max(g.ax.get_xlim()[1], g.ax.get_ylim()[1])
    g.ax.set_xlim((min_val, max_val))
    g.ax.set_ylim((min_val, max_val))
    g.fig.tight_layout()
    if in_ipython():
      g.fig.show()
      g.fig.savefig('tmp.png') # this doesn't reflect xlim/ylim change :<


if __name__ == '__main__':
  # full computation (time consuming)
  #pos_df = calculate_tsne_pos(clust_sr, dnb_idx, data_df)

  # load a pre-computed result
  pos_df = load_tsne_pos()
  
  plot_fig3d(pos_df)
  
