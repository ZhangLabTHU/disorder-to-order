import matplotlib.pyplot as plt
import numpy as np

# 加载数据
temperature = np.loadtxt('temperature.csv', delimiter=',')
sro_ptcomn = np.loadtxt('sro_ptcomn.csv', delimiter=',')
sro_ptcofe = np.loadtxt('sro_ptcofe.csv', delimiter=',')


# 创建 2 个子图，按 2 行 1 列排列
fig, axs = plt.subplots(2, 1, figsize=(4, 4))  # 设置图表大小
plt.rc('font', family='Arial')  # 设置字体为 Arial

# 设置 y 轴范围为 -0.4 到 0
y_min, y_max = -0.40, 0.10

# 设置所有子图的刻度线朝内，长度为6，并且刻度标签字体大小为 14
for ax in axs:
    ax.tick_params(axis='x', direction='in', length=6, labelsize=14)  # 设置x轴刻度线朝内，长度为6，字体大小为14
    ax.tick_params(axis='y', direction='in', length=6, labelsize=14)  # 设置y轴刻度线朝内，长度为6，字体大小为14

# 绘制第一个子图 (PtCoMn)
axs[0].plot(temperature, sro_ptcomn, marker='o', markersize=3, color='#276BB3')
axs[0].set_ylabel('SRO')
axs[0].set_ylim(y_min, y_max)
axs[0].set_yticks([-0.33, -0.22, -0.11,0])
axs[0].set_xticks([])
axs[0].legend([r'$\rm Pt_2CoMn$'], frameon=False, loc=2, fontsize=14)

# 绘制第二个子图 (PtCoFe)
axs[1].plot(temperature, sro_ptcofe, marker='o', markersize=3, color='#276BB3')
axs[1].set_ylabel('SRO')
axs[1].set_ylim(y_min, y_max)
axs[1].set_yticks([-0.33, -0.22, -0.11,0])
axs[1].legend([r'$\rm Pt_2CoFe$'], frameon=False, loc=2, fontsize=14)
axs[1].set_xlabel('Temperature (K)', fontsize=16)

#  调整子图之间的间隙为 0
plt.subplots_adjust(hspace=0)  # 设置子图之间的垂直间隙为 0

plt.savefig('sro_1x2.eps', bbox_inches='tight')
# 显示图形
plt.show()
