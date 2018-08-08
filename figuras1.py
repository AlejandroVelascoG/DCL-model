print "loading packages..."
import pandas as pd
import matplotlib.pyplot as plt

# Opens the file with data from DCL experiment into a Pandas DataFrame
print "Reading data..."

data_archivo = 'sim_dat.csv'

data = pd.read_csv(data_archivo, index_col=False)
print "Data read!"

# --------------------------------------------------
# Working only with trials with "Unicorn_Absent"
# --------------------------------------------------
# data = pd.DataFrame(data.groupby('Is_there').get_group('Unicorn_Absent')).reset_index()
print "Getting only Unicorn_Absent"
data = pd.DataFrame(data.groupby('Is_there').get_group('Unicorn_Absent'))


# Finds the size of focal splits for each experiment
FP = list(data.Exp.unique())
print FP
# estilos = ['-', '--', '--', '-', '-']
# colores = ["0", "0.2", "0.4", "0.6", "0.8"]
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
fig5.savefig('average_DLIndex.png')
print "Figure saved as average_DLIndex.png"

print "Done!"
