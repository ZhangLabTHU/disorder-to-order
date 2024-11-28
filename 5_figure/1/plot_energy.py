import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.metrics import mean_absolute_error

# 加载数据
data = np.load("energy.npy")

# 设置matplotlib全局字体
mpl.rcParams['font.family'] = 'Arial'

# 创建图形和网格布局
fig = plt.figure(figsize=(5, 4))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 0.1], height_ratios=[0.05, 1])  # 增加频率分布图的宽度

# 创建散点图的子区域
ax_main = fig.add_subplot(gs[1, 0])

# 创建直方图的子区域
ax_hist_x = fig.add_subplot(gs[0, 0], sharex=ax_main)
ax_hist_y = fig.add_subplot(gs[1, 1], sharey=ax_main)

# 绘制散点图，增大标记的大小
ax_main.scatter(data[:, 0], data[:, 1], s=40, color='#D85558')  # 增大标记尺寸为40
ax_main.plot(np.linspace(-7.5, -5.3, 100), np.linspace(-7.5, -5.3, 100), color='gray', linestyle='--', linewidth=1)

# 设置X和Y轴标签
ax_main.set_xlabel('DFT Energy (eV/Atom)', fontsize=16)
ax_main.set_ylabel('ML Energy (eV/Atom)', fontsize=16)

# 设置坐标轴刻度
ax_main.tick_params(labelsize=14, which='major', length=6)
ax_main.tick_params(axis='both', direction='in')

# 绘制X轴的频率分布直方图，增宽图形
ax_hist_x.hist(data[:, 0], bins=20, color='#D85558', alpha=0.6)
ax_hist_x.set_ylabel('Frequency', fontsize=14)
ax_hist_x.tick_params(axis='x', labelsize=0)  # 去掉X轴标签

# 绘制Y轴的频率分布直方图
ax_hist_y.hist(data[:, 1], bins=20, color='#D85558', alpha=0.6, orientation='horizontal')
ax_hist_y.set_xlabel('Frequency', fontsize=14)
ax_hist_y.tick_params(axis='y', labelsize=0)  # 去掉Y轴标签

# 计算并打印MAE
mae = mean_absolute_error(data[:, 0], data[:, 1])
print("Mean Absolute Error (MAE):", mae)

# 保存和显示图形
plt.tight_layout()
plt.savefig('energy_with_histograms.eps', bbox_inches='tight')
plt.show()
