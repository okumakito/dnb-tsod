import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import os, sys
import subprocess
from scipy import stats
from scipy.cluster.hierarchy import distance, linkage, fcluster
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from utils import parallel_analysis, calculate_deg

# short functions ----------------------------------------

def in_ipython():
  return 'TerminalIPythonApp' in get_ipython().config

def corr_inter(X, Y):
  # X (n x p1), Y (n x p2)
  X_normed = (X - X.mean(axis=0)) / X.std(axis=0, ddof=0)
  Y_normed = (Y - Y.mean(axis=0)) / Y.std(axis=0, ddof=0)
  return np.dot(X_normed.T, Y_normed) / X.shape[0]

def plot_gene(gene_name):
  long_form_df = data_df.loc[gene_name].reset_index()
  fig, ax = plt.subplots()
  sns.swarmplot(data=long_form_df, x='week', y=gene_name,
                hue='condition', dodge=True)

def correlation_adjust():
  p1 = 10**4
  p2 = 10**3
  for n in [3,4,5]:
    res = np.abs(corr_inter(np.random.randn(n, p1), np.random.randn(n, p2)))
    print('n={}, correlation strength = {:.4f} +- {:.4f}'.
          format(n, np.mean(res), stats.sem(res, axis=None)))
