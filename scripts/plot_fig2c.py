def plot_fig2c(clust_sr, data_dfdf):

  df = data_df.loc[clust_sr.index]
  df = df.groupby(axis=1, level=[0,1]).mean().loc[:,['TSOD','TSNO']]
  df = ((df.T - df.T.mean()) / df.T.std()).T
  df['clust'] = clust_sr
  df = df.groupby('clust').mean().iloc[:5]
  df = df.T.reset_index().melt(id_vars=['condition','week'],
                               value_vars=np.arange(5)+1,
                               value_name='average Z-score')
  
  with sns.plotting_context('talk'), sns.axes_style('whitegrid'):

    g  = sns.factorplot(data      = df,
                        x         = 'week',
                        y         = 'average Z-score',
                        hue       = 'condition',
                        col       = 'clust',
                        legend    = False,
                        aspect    = 0.6,
                        hue_order = ['TSOD', 'TSNO'], 
                        palette   = ['xkcd:windows blue', 'xkcd:amber'])
    g.set_titles('cluster {col_name}')
    if in_ipython():
      g.fig.show()
      g.fig.savefig('tmp1.png')


def plot_fig2c_legend():
  fig, ax = plt.subplots(figsize=(1,2.0))
  
  ax.plot([], 'o', label='metabo\n(TSOD)', color='xkcd:windows blue')
  ax.plot([], 'o', label='control\n(TSNO)', color='xkcd:amber')
  ax.legend(frameon=True, loc='upper left', labelspacing=1,
            borderpad=1,
            handletextpad=None, markerscale=2, fontsize=11,
            facecolor='xkcd:light grey')
  sns.despine(bottom=True, left=True)
  ax.set_xlabel('')
  ax.set_ylabel('')
  ax.set_xticks([])
  ax.set_yticks([])
  if in_ipython():
    fig.show()
    fig.tight_layout()
    fig.savefig('tmp2.png')
    cmd1 = ['convert', '-crop', '120x100+35+30', 'tmp2.png', 'tmp3.png']
    cmd2 = ['convert', 'tmp1.png', 'tmp3.png', '-gravity', 'northwest',
            '-geometry', '+180+50', '-composite', 'tmp.png']
    cmd3 = ['rm', 'tmp1.png', 'tmp2.png', 'tmp3.png']
    subprocess.call(cmd1)
    subprocess.call(cmd2)
    subprocess.call(cmd3)

      
if __name__ == '__main__':
  plot_fig2c(clust_sr, data_df)
  plot_fig2c_legend()
