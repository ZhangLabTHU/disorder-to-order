from ase.io import read
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# 读取数据
df = pd.read_csv('site_energy_ptcocu.csv')
# 创建子图
fig, axs = plt.subplots(3, 1, figsize=(4, 4))
colors = ['#D85558', '#276BB3', '#FF7F50']  # 保留直方图的颜色
plt.rc('font', family='Arial')

# 设置所有子图的刻度线样式
for ax in axs:
    ax.tick_params(axis='x', direction='in', length=6, labelsize=12)
    ax.tick_params(axis='y', direction='in', length=6, labelsize=12)

# 为每个种类绘制直方图和概率密度曲线
for i in [0,1,2]:
    # 筛选当前种类的数据
    energy_data = df[df['site'] == i]['energy']
    print(i,energy_data.mean())
    
    # 绘制直方图
    axs[i].hist(energy_data, bins=20, color=colors[i], alpha=0.6, density=True, label='Histogram')
    
    # 核密度估计
    kde = gaussian_kde(energy_data)
    x_vals = np.linspace(0, 2.5, 500)  # 生成 x 轴的密度点
    y_vals = kde(x_vals)
    
    # 绘制概率密度曲线
    axs[i].plot(x_vals, y_vals, color=colors[i], linestyle='--', linewidth=1.5, label='KDE')
    axs[i].axvline(x=energy_data.mean(), color=colors[i], linestyle='--') 
    print(energy_data.mean())
    
    # 设置子图参数
    axs[i].set_xlim([0, 2.5])
    axs[i].set_xticks([])
    # axs[i].set_yticks([])
    axs[i].set_ylabel('Density', fontsize=14)

# 设置 X 轴标签和刻度
axs[2].set_xlabel('Diffusion Barrier (eV)', fontsize=14)
axs[2].set_xticks([0, 0.5, 1, 1.5, 2, 2.5])

# 调整布局并保存
plt.tight_layout()
plt.savefig('ptco.png', bbox_inches='tight')
plt.show()


