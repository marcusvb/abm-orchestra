import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot')

output = pd.read_csv('Logs/OFAT_param_agent_weight')

# output = pd.read_csv('OFAT_param_random_walker_probability')
# output = pd.read_csv('OFAT_param_toilet_probability')


cols = ['id','Zuid Count', 'Noord ValidationCount', 'Champage ValidationCount', 'Noord Density','Zuid Density', 'Garderobe Density']
output.columns = cols

mu = output.groupby('id', as_index=False)['Zuid Count'].mean()
var = output.groupby('id', as_index=False)['Zuid Count'].std()

x = [0.01, 0.05, 0.1, 0.2, 0.5, 0.8]

# plt.plot(x, mu['Zuid Count'])
# plt.show()

# x = [0.01, 0.05, 0.1, 0.2, 0.5, 0.8]
#
# mu = output.groupby('id', as_index=False)[cols[0]].mean()
# print(mu)
# var = output.groupby('id', as_index=False)[cols[0]].std()
# plt.title(cols[0])
# print(mu)
# plt.plot(x, mu[cols[0]])
# plt.show()

f, axs = plt.subplots(6, figsize=(5, 10), dpi=120, sharex=True)

for i, col in enumerate(cols[1:]):
    mu = output.groupby('id', as_index=False)[col].mean()
    var = output.groupby('id', as_index=False)[col].std()

    print(mu)

    err = 1.96 * var / np.sqrt(4)
    axs[i].plot(x, mu[col], c='k')
    axs[i].fill_between(x, mu[col] - err[col], mu[col] + err[col])

    axs[i].set_title(col)
    axs[i].set_xticks([0,0.5,1])
plt.tight_layout()
plt.show()

# for i in range(6):
#     print(i)