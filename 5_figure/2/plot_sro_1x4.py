import matplotlib.pyplot as plt
import numpy as np

# 加载数据
temperature = np.loadtxt('temperature.csv', delimiter=',')
sro_ptcomn = np.loadtxt('sro_ptcomn.csv', delimiter=',')
sro_ptcofe = np.loadtxt('sro_ptcofe.csv', delimiter=',')
sro_ptco = np.loadtxt('sro_ptco.csv', delimiter=',')
sro_ptcoga = np.loadtxt('sro_ptcoga.csv', delimiter=',')
sro_ptconi = np.loadtxt('sro_ptconi.csv', delimiter=',')
sro_ptcocu = np.loadtxt('sro_ptcocu.csv', delimiter=',')

# 创建 4 个子图，按 4 行 1 列排列
fig, axs = plt.subplots(4, 1, figsize=(4, 8))  # 设置图表大小
plt.rc('font', family='Arial')  # 设置字体为 Arial

# 设置 y 轴范围为 -0.4 到 0
y_min, y_max = -0.40, -0.08

# 设置所有子图的刻度线朝内，长度为6，并且刻度标签字体大小为 14
for ax in axs:
    ax.tick_params(axis='x', direction='in', length=6, labelsize=14)  # 设置x轴刻度线朝内，长度为6，字体大小为14
    ax.tick_params(axis='y', direction='in', length=6, labelsize=14)  # 设置y轴刻度线朝内，长度为6，字体大小为14

# 绘制第一个子图 (PtCo)
axs[0].plot(temperature, sro_ptco, marker='o', markersize=3, color='#D85558')
axs[0].set_ylabel('SRO')
axs[0].set_ylim(y_min, y_max)
axs[0].set_yticks([-0.33, -0.22, -0.11,])
axs[0].set_xticks([])
axs[0].legend([r'$\rm PtCo$'], frameon=False, loc=2, fontsize=14)

# 绘制第二个子图 (PtCoGa)
axs[1].plot(temperature, sro_ptcoga, marker='o', markersize=3, color='#D85558')
axs[1].set_ylabel('SRO')
axs[1].set_ylim(y_min, y_max)
axs[1].set_yticks([-0.33, -0.22, -0.11,])
axs[1].set_xticks([])
axs[1].legend([r'$\rm Pt_2CoGa$'], frameon=False, loc=2, fontsize=14)

# 绘制第三个子图 (PtCoNi)
axs[2].plot(temperature, sro_ptconi, marker='o', markersize=3, color='#D85558')
axs[2].set_ylabel('SRO')
axs[2].set_ylim(y_min, y_max)
axs[2].set_yticks([-0.33, -0.22, -0.11,])
axs[2].set_xticks([])
axs[2].legend([r'$\rm Pt_2CoNi$'], frameon=False, loc=2, fontsize=14)

# 绘制第四个子图 (PtCoCu)
axs[3].plot(temperature, sro_ptcocu, marker='o', markersize=3, color='#D85558')
axs[3].set_xlabel('Temperature (K)', fontsize=16)
axs[3].set_ylabel('SRO')
axs[3].set_ylim(y_min, y_max)
axs[3].set_yticks([-0.33, -0.22, -0.11,])
axs[3].legend([r'$\rm Pt_2CoCu$'], frameon=False, loc=2, fontsize=14)

# 调整子图之间的间隙为 0
plt.subplots_adjust(hspace=0)  # 设置子图之间的垂直间隙为 0

plt.savefig('sro.eps', bbox_inches='tight')
# 显示图形
plt.show()
