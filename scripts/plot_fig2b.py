def plot_fig2b(data_df):
  col_list = list('34567')
  deg_all_list = [calculate_deg(data_df['TSOD',t], data_df['TSNO',t]) \
                 for t in col_list]

  df = data_df.loc[np.unique(np.concatenate(deg_all_list))]
  df = df.groupby(axis=1, level=[0,1]).mean().loc[:,['TSOD','TSNO']]
  df.index.name = ''
  df.rename(columns={'TSOD-BTS':'BTS'}, inplace=True)

  df          = ((df.T - df.T.mean()) / df.T.std()).T
  dist_arr    = distance.pdist(df, 'correlation')
  linkage_arr = linkage(dist_arr, 'average')
  clust_arr   = fcluster(linkage_arr, t=0.5, criterion='distance')
  pal_arr     = sns.color_palette('Paired', max(clust_arr))
  color_arr   = np.take(pal_arr, clust_arr - 1, axis=0)

  # re-number the cluster numbers (largest is 1)
  clust_sr    = pd.Series(clust_arr, index=df.index)
  freq_sr     = clust_sr.value_counts()
  clust_sr.replace(pd.Series(np.arange(len(freq_sr))+1,
                             index=freq_sr.index), inplace=True)
  
  for i in np.arange(5)+1:
    gene_sr = pd.Series(clust_sr[clust_sr == i].index)
    print('cluster {}: {:>4d} genes'.format(i, len(gene_sr)))
    gene_sr.to_csv('tmp_c{:d}.txt'.format(i), index=False)

  g = sns.clustermap(df,
                     row_linkage = linkage_arr,
                     col_cluster = False,
                     cmap        = plt.cm.RdBu_r,
                     row_colors  = color_arr,
                     figsize     = (10,6))
  g.ax_heatmap.set_yticks([])
  g.ax_heatmap.axvline(x=5, c='w', lw=4)
  if in_ipython():
    g.fig.show()
    g.fig.savefig('tmp1.png')
    cmd1 = ['convert', '-crop', '900x550+50+150', 'tmp1.png', 'tmp2.png']
    #cmd1 = ['convert', '-crop', '950x550+0+150', 'tmp1.png', 'tmp2.png']
    cmd2 = ['convert', '-crop', '100x100+100+50', 'tmp1.png', 'tmp3.png']
    cmd3 = ['convert', 'tmp2.png', 'tmp3.png', '-gravity', 'southwest',
            '-geometry', '+60+60', '-composite', 'tmp.png']
    #        '-geometry', '+0+60', '-composite', 'tmp.png']
    cmd4 = ['rm', 'tmp1.png', 'tmp2.png', 'tmp3.png']
    subprocess.call(cmd1)
    subprocess.call(cmd2)
    subprocess.call(cmd3)
    subprocess.call(cmd4)
    
  return clust_sr

if __name__ == '__main__':
  clust_sr = plot_fig2b(data_df)
