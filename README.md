# dnb-tsod

This repository provides source codes used in the following work:

* K. Koizumi, M. Oku, S. Hayashi, A. Inujima, N. Shibahara, L. Chen, Y. Igarashi, K. Tobe, S. Saito, M. Kadowaki, and K. Aihara: Identifying pre-disease signals before metabolic syndrome in mice by dynamical network biomarkers, Scientific Reports, 9:8767 (2019). https://doi.org/10.1038/s41598-019-45119-w

## Requirements

The source codes are written in Python 3. In addition, NumPy, SciPy, pandas, Matplotlib, scikit-learn, and seaborn packages are required. All of them are included in Anaconda.

A gene expression data set GSE112653 is analyzed. Because the data size is large, the data set is excluded in this repository. Therefore, in order to run the source codes locally, please download the data set from [Gene Expression omnibus (GEO)](https://www.ncbi.nlm.nih.gov/geo/) database and put them into the *data* directory.
