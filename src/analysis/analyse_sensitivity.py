# We define our variables and bounds
problemf = {
    'num_vars': 3,
    'names': ['Agent Weight', 'Random walker probability', 'Toilet probability'],
    'bounds': [[0.01, 0.5], [0.01, 0.5], [0.01, 0.5]]
}


dataf = pd.read_csv('testdata_cg.csv')
dataf.columns=['Validation Zuid', 'Validation Noord', 'Validation Champagne', 'Density Zuid', 'Density Noord', 'Density Garderobe']

x = dataf['Validation Zuid'].as_matrix()[:8]
Si_Zuid_Density = sobol.analyze(problemf, x,  print_to_console=True)

plot_index(Si_Zuid_Density, problem['names'], 'T', 'First order sensitivity')
plt.show()