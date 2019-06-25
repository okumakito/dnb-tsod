import numpy as np
import pandas as pd

def quantile_normalization(data_df, method='min'):
  """
  Perform quantile normalization.
  
  Parameters
  ----------
  data_df : DataFrame

  method : {'min', 'max', 'first'}
    When the same value appears more than once in a column, the 
    corresponding rank is calculated based on this option.
    * min: lowest rank in group (default)
    * max: highest rank in group
    * first: ranks assigned in order they appear in the array

  Returns
  -------
  normed_df : DataFrame

  """
  mean_arr  = np.sort(data_df, axis=0).mean(axis=1)
  rank_arr  = data_df.rank(method=method).astype(int).values - 1
  normed_df = pd.DataFrame(mean_arr[rank_arr], 
                           index=data_df.index,
                           columns=data_df.columns)
  return normed_df

if __name__ == '__main__':
  data_df = pd.DataFrame(np.random.randint(10, size=(5,3)), 
                         index=list('abcde'), 
                         columns=list('xyz')).astype(float)
  normed_df = quantile_normalization(data_df)
  print('original data')
  print(data_df)
  print('normalized data')
  print(normed_df)
