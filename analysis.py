print "Importing pandas..."
import pandas as pd
import matplotlib.pyplot as plt

# data_archivo = 'sim_dat_1.csv'
data_archivo = 'sim_dat.csv'

data = pd.read_csv(data_archivo, index_col=False)
print "Data read!"

print data[:3]

# fig, axes = plt.subplots()
#
# data['DLIndex'].groupby(['Exp']).plot()

FP = list(data.Exp.unique())

print "Los valores del parametro son: ", FP

estilos = ['-', '--', '-.', ':', '-', '--', '-.', ':']
colores = ["0", "0", "0", "0", "0.5", "0.5", "0.5", "0.5"]
LW = 1.5 # linewidth for plot

print "Preparing plot for average DLIndex per round..."
fig5, axes5 = plt.subplots()
axes5.set_xlabel('Rounds', fontsize = 20)
axes5.set_ylabel('Average DLIndex', fontsize = 20)
axes5.set_ylim([-0.01, 1.01])

print "Creating plot"
for key, grp in data.groupby(['Exp']):
	grp[['Round','DLIndex']].groupby('Round').mean().plot(ax=axes5,\
	color=colores[FP.index(key)],\
	style=estilos[FP.index(key)], linewidth = LW)

axes5.legend(FP, loc='best', fontsize = 20)

plt.show()

# for gr, key in data.groupby('Exp'):
#
# 	gr.groupby('Round').mean().plot(ax=axes)
