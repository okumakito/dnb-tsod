def load_gene_name():
  file_name = '../data/gene_name_list.tsv'
  df = pd.read_csv(file_name, sep='\t', usecols=['GeneSymbol','GeneName']). \
       dropna().drop_duplicates()
  return pd.Series(df['GeneName'].values, index=df['GeneSymbol'])

def plot_figS6():
  gene_name_sr =  load_gene_name()
  gene_sr = pd.Series(['Tnf', 'Il6', 'Adipoq', 'Slc2a4', 'Pparg', 'Ppargc1a'])
  gene_sr2 = '$' + gene_sr + '$ - ' + \
             gene_sr.apply(gene_name_sr.get).str.wrap(30)
               
  df = data_df.loc[gene_sr].T.loc[['TSOD','TSNO']]
  df -= df.loc['TSNO','3'].mean()
  df.columns = gene_sr2
  df.reset_index(inplace=True)
  df = df.melt(id_vars=['condition', 'week'], value_vars=gene_sr2,
               var_name='gene', value_name='gene expression')

  with sns.plotting_context('notebook'):
    g = sns.factorplot(data      = df,
                       x         = 'week',
                       y         = 'gene expression',
                       hue       = 'condition',
                       col       = 'gene',
                       col_wrap  = 3,
                       dodge     = True,
                       hue_order = ['TSOD', 'TSNO'], 
                       palette   = ['xkcd:windows blue', 'xkcd:amber'],
                       legend    = False)
    g.axes[0].legend(frameon=False, loc='lower right')
    g.set_titles('{col_name}')
    g.fig.tight_layout(h_pad=3)
    if in_ipython():
      g.fig.show()
      g.fig.savefig('tmp.png')

if __name__ == '__main__':
  plot_figS6()
