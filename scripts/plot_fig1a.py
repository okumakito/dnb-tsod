def plot_fig1a(info_df, type_str):
  with sns.plotting_context('talk'):
      
    df = info_df[info_df['condition'] == 'TSOD']

    type_dict = {'w':'body weight (g)',
                 's':'blood sugar concentration (mg/dL)',
                 'f':'testicular fat mass (g)'}

    g  = sns.factorplot(data      = df,
                        x         = 'week',
                        y         = type_dict[type_str],
                        hue       = 'condition',
                        legend    = False,
                        aspect    = 0.75,
                        palette   = ['xkcd:windows blue', 'xkcd:amber'])
    if type_str == 'w':
      g.ax.axhline(y=40, ls='--', c='xkcd:coral')
      g.ax.scatter(0, 49, s=0) # adjust ylim and ticks
    if type_str == 's':
      g.ax.axhline(y=200, ls='--', c='xkcd:coral')
    if in_ipython():
      g.fig.show()
      g.fig.savefig('tmp_{}.png'.format(type_str))


if __name__ == '__main__':
  plot_fig1a(info_df, 'w') # body weight
  plot_fig1a(info_df, 's') # blood sugar level
  #plot_fig1a(info_df, 'f') # fat mass
