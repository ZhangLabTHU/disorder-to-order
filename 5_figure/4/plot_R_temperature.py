from ase.io import read
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# 读取数据

# 创建子图
fig, axs = plt.subplots(1, 3, figsize=(10, 3))
colors = ['#D85558', '#276BB3', '#FF7F50']  # 保留直方图的颜色
plt.rc('font', family='Arial')

# 设置所有子图的刻度线样式
for ax in axs:
    ax.tick_params(axis='x', direction='in', length=6, labelsize=10)
    ax.tick_params(axis='y', direction='in', length=6, labelsize=10)

Temperature = [400, 800, 3000]
# 为每个种类绘制直方图和概率密度曲线
for i in [0,1,2]:
    # 筛选当前种类的数据
    energy_data = np.loadtxt(str(Temperature[i]) + '.csv', delimiter=',')

    # 计算直方图（不使用 density=True）
    counts, bins, patches = axs[i].hist(energy_data, bins=15, color=colors[i], alpha=0.6, label='Histogram')

    # 归一化 counts，使其总和为 1
    counts = counts / counts.sum()

    # 更新直方图的高度
    for patch, new_height in zip(patches, counts):
        patch.set_height(new_height)

    # 设置子图参数
    axs[i].set_xlim([0, 0.8])
    axs[i].set_ylim([0, max(counts) * 1.1])  # y 轴范围略大于最大值，避免图像紧贴上边界
    axs[i].set_ylabel('Probability', fontsize=12)
    axs[i].set_xlabel('Diffusion randomness R', fontsize=12)


# 设置 X 轴标签和刻度
# axs[2].set_xlabel('Diffusion Barrier (eV)', fontsize=14)
# axs[2].set_xticks([0, 0.5, 1, 1.5, 2, 2.5])

# 调整布局并保存
plt.tight_layout()
plt.savefig('R_distribution.png', bbox_inches='tight')
plt.show()


