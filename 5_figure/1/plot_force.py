
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.metrics import mean_absolute_error
from matplotlib.ticker import MaxNLocator

# 加载数据
data = np.load("force.npy")

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

# 提取数据
f_x_true = data[:,0]
f_y_true = data[:,1]
f_z_true = data[:,2]
f_x_pred = data[:,3]
f_y_pred = data[:,4]
f_z_pred = data[:,5]

# 计算力的大小
y_true = [np.linalg.norm([i,j,k]) for (i,j,k) in zip(f_x_true, f_y_true, f_z_true)]
y_pred = [np.linalg.norm([i,j,k]) for (i,j,k) in zip(f_x_pred, f_y_pred, f_z_pred)]

# 绘制散点图，增大标记的大小
ax_main.scatter(y_true[::50], y_pred[::50], s=40, color='#2A66A8')  # 增大标记尺寸为40

# 绘制45度参考线
min_value = min(y_true)
max_value = max(y_pred)
x_plot = np.linspace(min_value-0.02, max_value+0.02, 100)
ax_main.plot(x_plot, x_plot, color='gray', linestyle='--', linewidth=1)

# 设置X和Y轴标签
ax_main.set_xlabel('DFT Force (eV/Å)', fontsize=16)
ax_main.set_ylabel('ML Force (eV/Å)', fontsize=16)

# 设置坐标轴刻度
ax_main.tick_params(labelsize=14, which='major', length=6)
ax_main.tick_params(axis='both', direction='in')

# 设置坐标轴刻度格式为小数点后两位
ax_main.xaxis.set_major_locator(MaxNLocator(integer=False))
ax_main.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))
ax_main.yaxis.set_major_locator(MaxNLocator(integer=False))
ax_main.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))
ax_main.set_xticks([0,1,2,3,4])
ax_main.set_yticks([0,1,2,3,4])

# 绘制X轴的频率分布直方图
ax_hist_x.hist(y_true, bins=30, color='#2A66A8', alpha=0.6)
ax_hist_x.set_ylabel('Frequency', fontsize=14)
ax_hist_x.tick_params(axis='x', labelsize=0)  # 去掉X轴标签

# 绘制Y轴的频率分布直方图
ax_hist_y.hist(y_pred, bins=30, color='#2A66A8', alpha=0.6, orientation='horizontal')
ax_hist_y.set_xlabel('Frequency', fontsize=14)
ax_hist_y.tick_params(axis='y', labelsize=0)  # 去掉Y轴标签

# 计算并打印MAE
mae = mean_absolute_error(y_true, y_pred)
print("Mean Absolute Error (MAE):", mae)

# 保存和显示图形
plt.tight_layout()
plt.savefig('Force_with_histograms.eps', bbox_inches='tight')
plt.show()


