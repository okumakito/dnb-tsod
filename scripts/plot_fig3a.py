def plot_fig3a(data_df, dnb_idx):

  bg_idx     = np.setdiff1d(data_df.index, dnb_idx)
  shift_dic = {3:0.64, 4:0.50, 5:0.42}

  stat_df = pd.DataFrame(index=['condition',
                                'week',
                                'average standard deviation $I_s$',
                                'average correlation strength $I_r$',
                                'ave. corr. strength bw. DNB and non-DNB'])
  for i, (col, df) in enumerate(data_df.groupby(axis=1, level=[0,1])):

    shift   = shift_dic[df.shape[1]]
    std_val = df.loc[dnb_idx].std(axis=1).mean()
    corr_df = df.loc[dnb_idx].T.corr().abs()
    np.fill_diagonal(corr_df.values, None)
    corr_val = corr_df.mean().mean() - shift
    bg_val   = np.mean(np.abs(corr_inter(df.loc[dnb_idx].T,
                                         df.loc[bg_idx].T))) - shift
    stat_df[i] = [col[0], col[1], std_val, corr_val, bg_val]

  stat_df = stat_df.T
  stat_df = stat_df[stat_df['condition'] == 'TSOD']
  #stat_df = stat_df[stat_df['condition'] != 'TSNO']
  
  with sns.plotting_context('talk'):

    kws = dict(data=stat_df,
               x='week',
               hue='condition', 
               legend=False,
               #hue_order = ['TSOD', 'TSOD-BTS'], 
               palette   = ['xkcd:windows blue', 'xkcd:rose'])
    w, h = (4,5)
    w2, h2 = (6,5)
    kws2 = dict(aspect=w/h, size=h)
    kws3 = dict(aspect=w2/h2, size=h2)
    g1 = sns.factorplot(y=stat_df.columns[2], **kws, **kws2)
    g2 = sns.factorplot(y=stat_df.columns[3], **kws, **kws2)
    g3 = sns.factorplot(y=stat_df.columns[4], **kws, **kws3)
    g3.ax.set_ylim(g2.ax.get_ylim())
    for i, g in enumerate([g1, g2, g3]):
      #g.ax.legend(frameon=False, loc='upper left')
      if in_ipython():
        g.fig.show()
        g.fig.savefig('tmp{}.png'.format(i))

      
if __name__ == '__main__':
  plot_fig3a(data_df, dnb_idx)
