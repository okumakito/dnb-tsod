import numpy as np
import pandas as pd

def parallel_analysis(data, n=100, alpha=0.05, centered=True,
                      method='normal', output_eig=False):

  """
  This function determines the number of meaningful principal 
  components.

  Parameters
  ----------
  data : array_like
    data matrix (row: observations, columns: variables)
  n : integer, optional
    number of random/randomized matrices. Default is 100.
  alpha : float, optional
    significance level. Default is 0.05.
  centered : bool, optional
    If True, centering is performend. Default is True.
  method : {'normal', 'shuffle', 'boot', }, optional
    Method for generating uncorrelated matrices. 'normal' is 
    sampling from N(0,sigma_i), where sigma_i is the standard 
    deviation of the ith variable in the original data. 
    'shuffle' is  sampling from the original data without 
    replacement. 'boot' is sampling with replacement. Default 
    is 'normal'.
  output_eig : bool, optional
    If True, eigenvalues are returned. Default is False.

  Returns
  -------
  n_component : integer
    number of meaningful principal components
  eig_orig : ndarray
    eigenvalues of original data
  eig_rand : ndarray
    eigenvalues of random data

  """
  X = np.asarray(data)
  n_row, n_col = X.shape

  # original data
  def calc_eig(Z):
    Z2    = Z - Z.mean(axis=0) if centered else Z
    s_arr = np.linalg.svd(Z2, compute_uv=False)
    return s_arr**2 / (Z.shape[0] - 1)
  eig_orig = calc_eig(X)
  
  # generate random/randomized matrices
  col_arr  = np.ones_like(X).astype(int) * np.arange(n_col)
  if method == 'normal':
    eig_rand = [calc_eig(np.random.randn(*X.shape) * X.std(axis=0, ddof=1))
                for _ in range(n)]
  elif method == 'shuffle':
    eig_rand = [calc_eig(X[pd.DataFrame(np.random.randn(*X.shape)).\
                           rank().astype(int) -1, col_arr]) \
                for _ in range(n)]
  elif method == 'boot':
    eig_rand = [calc_eig(X[np.random.randint(n_row, size=X.shape), col_arr])
                for _ in range(n)]
  else:
    raise ValueError("<method> must be 'normal', 'shuffle', or 'boot'.")
  eig_rand = np.array(eig_rand)

  # comparison
  eig_diff = eig_orig - np.percentile(eig_rand, 100 * (1 - alpha), axis=0)
  idx_arr  = np.where(eig_diff < 0)[0]
  n_comp = idx_arr[0] if len(idx_arr) > 0 else len(eig_diff)

  if output_eig:
    return n_comp, eig_orig, eig_rand
  else:
    return n_comp


if __name__ == '__main__':
  x = random.randn(5, 500)
  n_comp, eig_orig, eig_rand = parallel_analysis(x, output_eig=True,
                                                 method='normal')
  fig, ax = plt.subplots()
  ax.plot(eig_orig[:-1], lw=5)
  ax.plot(np.percentile(eig_rand[:,:-1], 95, axis=0))
  ax.plot(np.percentile(eig_rand[:,:-1], 5, axis=0))
  fig.show()
  print(n_comp)
