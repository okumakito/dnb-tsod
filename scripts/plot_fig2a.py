def plot_fig2a(data_df):
  col_list = list('34567')
  deg_all_list = [calculate_deg(data_df['TSOD',t], data_df['TSNO',t]) \
                  for t in col_list]
  print('total  : {:>5d} genes'.format(
    len(np.unique(np.concatenate(deg_all_list)))))
  
  df = pd.DataFrame(0, index=data_df.index, columns=col_list)
  for week, deg_arr in zip(col_list, deg_all_list):
    print('{} weeks: {:>5d} genes'.format(week, len(deg_arr)))
    df.loc[deg_arr,week] = 1
  df['sum'] = df.sum(axis=1)
  df = df[df['sum'] != 0]
  df.sort_values(by=list(df.columns)[::-1], inplace=True)
  df.drop('sum', axis=1, inplace=True)
  df.index.name   = 'gene'
  df.columns.name = 'week'

  fig, ax = plt.subplots(figsize=(3,4))
  sns.heatmap(df,
              ax=ax,
              yticklabels = False,
              cbar        = False,
              cmap        = ['0.9','0.15'])
  fig.tight_layout()
  if in_ipython():
    fig.show()
    fig.savefig('tmp.png')


if __name__ == '__main__':
  plot_fig2a(data_df)
