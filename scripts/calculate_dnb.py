def calculate_dnb(expr_df, ctrl_df, theta1, theta2, theta3):
    
  # step 1: standard deviation ---------------------------------

  n1 = int(theta1 * len(expr_df))
  std_ratio_sr =  expr_df.std(axis=1) / ctrl_df.std(axis=1)
  idx1 = std_ratio_sr.sort_values(ascending=False).index[:n1]
  #print(std_ratio_sr.loc[idx1].min())
  
  # step 2: correlation ----------------------------------------

  n2 = int(theta2 * n1)
  corr_diff_sr = (expr_df.loc[idx1].T.corr().abs() \
                  - ctrl_df.loc[idx1].T.corr().abs()).sum()
  idx2 = corr_diff_sr.sort_values(ascending=False).index[:n2]
  
  # step 3: background correlation -----------------------------

  n3      = int(theta3 * n1)
  idx_bg  = np.setdiff1d(expr_df.index, idx1)
  bg_expr_arr = corr_inter(expr_df.loc[idx1].T, expr_df.loc[idx_bg].T)
  bg_ctrl_arr = corr_inter(ctrl_df.loc[idx1].T, ctrl_df.loc[idx_bg].T)
  bg_diff_sr  = pd.Series((np.abs(bg_expr_arr) -
                           np.abs(bg_ctrl_arr)).sum(axis=1), index=idx1)
  idx3 = bg_diff_sr.sort_values(ascending=True).index[:n3]
    
  return idx2 & idx3

def calculate_dnb_batch(data_df):
  theta1 = 0.1
  theta2 = 0.5
  theta3 = 0.2

  print('# main result (TSOD 5w vs. TSNO 5w)')
  dnb_idx = calculate_dnb(data_df[('TSOD','5')], data_df[('TSNO','5')],
                          theta1, theta2, theta3)
  print(len(dnb_idx), 'genes')


  print('\n# reproducibility check')
  overlap_list = []
  idx_arr = np.arange(data_df[('TSOD','5')].shape[1])
  for i in range(len(idx_arr)):
    # remove one sample
    expr_df = data_df[('TSOD','5')].iloc[:, np.delete(idx_arr, i)]
    dnb_idx3 = calculate_dnb(expr_df, data_df[('TSNO','5')],
                             theta1, theta2, theta3)
    #print(len(dnb_idx3), len(np.intersect1d(dnb_idx, dnb_idx3)))
    overlap_list.append(len(np.intersect1d(dnb_idx, dnb_idx3)))
  idx_arr = np.arange(data_df[('TSNO','5')].shape[1])
  for i in range(len(idx_arr)):
    # remove one sample
    ctrl_df = data_df[('TSNO','5')].iloc[:, np.delete(idx_arr, i)]
    dnb_idx3 = calculate_dnb(data_df[('TSOD','5')], ctrl_df,
                             theta1, theta2, theta3)
    #print(len(dnb_idx3), len(np.intersect1d(dnb_idx, dnb_idx3)))
    overlap_list.append(len(np.intersect1d(dnb_idx, dnb_idx3)))
  print('overlap (mean +/- sem) = {:.1f} +/- {:.1f}'.
        format(np.mean(overlap_list), stats.sem(overlap_list)))

  
  print('\n# Suppl. Fig S7 (TSOD 5w vs. TSOD 3w)')
  dnb_idx2 = calculate_dnb(data_df[('TSOD','5')], data_df[('TSOD','3')],
                           theta1=0.05, theta2=0.35, theta3=0.7)
  n_overlap = len(np.intersect1d(dnb_idx, dnb_idx2))
  p_val = stats.hypergeom.sf(n_overlap-1, len(data_df),
                             len(dnb_idx), len(dnb_idx2))
  print(len(dnb_idx2), 'genes')
  print('ovrelap =', n_overlap)
  print('p-val ={:.1e}'.format(p_val))

  pd.Series(dnb_idx.sort_values()).to_csv('tmp.txt', index=False)
  pd.Series(dnb_idx2.sort_values()).to_csv('tmp2.txt', index=False)
  return dnb_idx, dnb_idx2
  
if __name__ == '__main__':
  dnb_idx, dnb_idx2 = calculate_dnb_batch(data_df)
