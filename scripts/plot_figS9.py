def plot_figS9(data_df, dnb_idx):

  df_trans = data_df.loc[dnb_idx, 'TSOD'].T
  df_trans = (df_trans - df_trans.mean()) / df_trans.std()
  df = df_trans.T

  model = PCA(n_components=1)
  score_sr = df.groupby(axis=1, level=0).\
             apply(lambda df2: model.fit(df2.T).explained_variance_[0])
  score_sr = 1 / score_sr
  score_sr /= score_sr.max()
  print(score_sr)

  df = pd.DataFrame()
  df['week'] = score_sr.index
  df['estimated relative recovery rate'] = score_sr.values

  with sns.plotting_context('talk'):
    g = sns.factorplot(data=df, x='week',
                       y='estimated relative recovery rate',
                       aspect=6/5, size=5, 
                       color  = 'xkcd:windows blue')
    if in_ipython():
      g.fig.show()
      g.fig.savefig('tmp.png')
    
    

if __name__ == '__main__':
  plot_figS9(data_df, dnb_idx)
