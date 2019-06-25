def plot_figS8():
  file_name = '../data/T-RFLP.tsv'
  df = pd.read_csv(file_name, sep='\t', index_col=0)
  df = df.groupby('Name').sum()

  # original order
  orig_list = ['others',
               'Clostridia cluster XVIII',
               'Clostridia cluster XI',         
               'Clostridia cluster XIVa',
               'Clostridia cluster IV',
               'Prevotella',
               'Bacteroides',
               'Lactobacillales',
               'Bifidobacterium']
  df = df.loc[orig_list[::-1]]

  # sort by abundance
  sr = df.sum(axis=1).sort_values(ascending=False)
  sr = sr[sr != 0]
  df = df.loc[np.r_[sr.index[sr.index!='others'], ['others']]]
  
  with sns.plotting_context('talk'), sns.axes_style('whitegrid'):

    fig, ax = plt.subplots()
    df.T.plot(kind='bar', stacked=True, ax=ax, legend=True)
    handles, labels = ax.get_legend_handles_labels()
    leg = ax.legend(handles[::-1], labels[::-1], bbox_to_anchor=(1,1),
                    frameon=False)
    ax.set_ylim((0,100))
    ax.set_ylabel('Peak area ratio (%)')
    fig.tight_layout()
    if in_ipython():
      fig.show()
      fig.savefig('tmp.png', bbox_extra_artists=(leg,), bbox_inches='tight')

if __name__ == '__main__':
  plot_figS8()
