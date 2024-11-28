import numpy as np
import matplotlib.pyplot as plt

Temperature = [i for i in range(100, 3000, 50)]
R_PtCo = np.loadtxt('R_PtCo.csv', delimiter=',')
R_PtCoCu = np.loadtxt('R_PtCoCu.csv', delimiter=',')

# 设置字体和坐标轴
fig,axs = plt.subplots(figsize=(4.5,4))
plt.rcParams['font.family'] = 'Arial'
# 设置刻度线朝内
axs.tick_params(axis='x', direction='in', length=6, labelsize=14)
axs.tick_params(axis='y', direction='in', length=6, labelsize=14)

plt.plot(Temperature, R_PtCo, label='o', marker='o',markersize=3,color='#D85558')
plt.plot(Temperature, R_PtCoCu, label='o', marker='o',markersize=3,color='#276BB3')
plt.legend(['PtCo','PtCoCu'],frameon=False,fontsize=14)
plt.xlabel('Temperature (K)', fontsize=16)
plt.ylabel('Diffusion multiplicity Var(R)', fontsize=16)
plt.yticks([0,0.01,0.02,0.03,0.04])
plt.tick_params(labelsize=14)
plt.savefig('VarR_temp.eps', dpi=300, bbox_inches='tight')
plt.show()
