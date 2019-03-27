Source data for data/plots shown in Sneeggen et al. 
A copy of this directory is deposited at GitHub: https://github.com/koschink/Sneeggen_et_al

- Data is organized in subfolders by Figure and Subfigure. 
- Plain data is deposited as Excel or CSV file and can be plotted directly
- Proteome data used to generate the volcano plot in Figure 4a is deposited as Excel sheet, columns labelled S1 and S2 represent "Control" and "GFP-WDFY2" conditions. 
- All other data is deposited as CSV file with an associated Python file
    - the python file automatically gathers and processes raw file(s), performs - where applicable - normalizations or calculations of experimental means and produces plots using Seaborn. 


Requirements:

Python 3 (3.7)
Pandas (0.23.4)
MatplotLib (3.0.2)
Seaborn 0.9 (install latest version via PIP)
Scipy-Stats (1.1.0)
