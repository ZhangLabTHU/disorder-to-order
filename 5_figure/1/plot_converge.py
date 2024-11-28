import matplotlib.pyplot as plt
import numpy as np


Colors = ['#264653','#2A9D8F','#E9C46A','#F4A261','#E76F51','#E63946']

data = np.genfromtxt("lcurve.out", names=True)
window_size = 20
name = data.dtype.names[3]
RMSE_e_test_val = data[name][:]
RMSE_e_test_val = np.convolve(RMSE_e_test_val, np.ones(window_size)/window_size, mode='valid')

name = data.dtype.names[4]
RMSE_e_test_trn = data[name][:]
RMSE_e_test_trn = np.convolve(RMSE_e_test_trn, np.ones(window_size)/window_size, mode='valid')


name = data.dtype.names[5]
RMSE_f_test_val = data[name][:]
RMSE_f_test_val = np.convolve(RMSE_f_test_val, np.ones(window_size)/window_size, mode='valid')

name = data.dtype.names[6]
RMSE_f_test_trn = data[name][:]
RMSE_f_test_trn = np.convolve(RMSE_f_test_trn, np.ones(window_size)/window_size, mode='valid')


fig,ax1=plt.subplots(figsize=(5,4))
plt.rc('font', family='Arial')

ax1.plot(RMSE_e_test_trn,linestyle='-',color=Colors[0],markersize=10)
ax1.plot(RMSE_e_test_val,linestyle='--',color=Colors[0],markersize=10)
ax1.set_xlabel('Training step ' +r'$\rm(x10^3)$',fontsize=16)
ax1.set_ylabel('RMSE of Energy (eV/Atom)',fontsize=16)
ax1.tick_params(direction='in',labelsize=14,which='major', length=6,)
ax1.set_xscale('log')
ax1.set_ylim([0,0.10])
ax1.legend(['train', 'valid'],frameon=False,fontsize=14,loc=(0.55, 0.3))

ax2 = ax1.twinx()
ax2.plot(RMSE_f_test_trn,linestyle='-',color=Colors[-1],markersize=10)
ax2.plot(RMSE_f_test_val,linestyle='--',color=Colors[-1],markersize=10)
ax2.set_ylabel('RMSE of Force (eV/Å)',fontsize=16)
ax2.tick_params(direction='in',labelsize=14,which='major', length=6,)
ax2.set_ylim([0,0.2])
ax2.legend(['train', 'valid'],frameon=False,fontsize=14,loc=(0.60, 0.6))

plt.savefig('converge.eps',bbox_inches='tight')
plt.show()
